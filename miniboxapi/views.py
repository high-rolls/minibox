from django.db.models import Value as V
from django.db.models.functions import Concat
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from miniboxapi.models import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from miniboxapi.serializers import *
from miniboxapi.permissions import *
import unidecode


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # API endpoint that allows users to be viewed or edited
    serializer_class = UserSerializer
    permission_classes = [IsCompanyAdministrator | permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(profile__company=user.profile.company)


class GroupViewSet(viewsets.ModelViewSet):
    # API endpoint that allows groups to be viewed or edited
    # TODO allow companies to create its own groups
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [permissions.IsAdminUser]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCompanyAdministrator | permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        queryset = Profile.objects.all()
        if not user.is_staff:
            queryset = queryset.filter(company=user.profile.company)

        request_q = self.request.query_params.get('q', None)
        if request_q is not None:
            # unidecode removes accents
            request_q = unidecode.unidecode(
                request_q).lower()
            queryset = queryset.annotate(full_name=Concat(
                'user__first_name', V(' '), 'user__last_name'))
            qnames = queryset.filter(
                full_name__istartswith=request_q)
            qcpf = queryset.filter(cpf__startswith=request_q)
            queryset = qnames.union(qcpf)
        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProfileSerializer
        return CompanyAdminProfileSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(company=self.request.user.profile.company)
        else:
            serializer.save()

    @action(detail=True)
    def files(self, request, pk=None):
        file_permissions = UserFilePermission.objects.filter(
            user=self.get_object().user).order_by('file__path', 'file__name')
        files = []
        for file_permission in file_permissions:
            file = FileSerializer(file_permission.file, context={
                                  'request': request}).data
            files.append(file)
        return Response(files)

    @action(detail=True)
    def file_permissions(self, request, pk=None):
        file_permissions = UserFilePermission.objects.filter(
            user=self.get_object().user)
        objects = []
        context = {'request': request}
        for fp in file_permissions:
            ufp = UserFilePermissionSerializer(fp, context=context).data
            objects.append(ufp)
        return Response(objects)


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = File.objects.all()
        if user.is_staff:
            company = self.request.query_params.get('company', None)
            if company is not None:
                queryset = queryset.filter(company=company)
        else:
            queryset = queryset.filter(
                company=self.request.user.profile.company)

        path = self.request.query_params.get('path', None)
        if path is not None:
            queryset = queryset.filter(path=path)
        return queryset.order_by('company', '-is_directory', 'path', 'name')

    def get_serializer_class(self):
        u = self.request.user
        if u.is_staff:
            return FileSerializer
        return CompanyFileSerializer

    def perform_create(self, serializer):
        u = self.request.user
        if u.is_staff:
            serializer.save()
        else:  # company admin or regular user
            serializer.save(company=u.profile.company)

    @action(detail=True)
    def permissions(self, request, pk=None):
        queryset = UserFilePermission.objects.filter(file=self.get_object(
        )).order_by('user__first_name', 'user__last_name', 'permission__name')
        objects = []
        for item in queryset:
            ufp = UserFilePermissionSerializer(
                item, context={'request': request}).data
            objects.append(ufp)
        return Response(objects)


class FilePermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.filter(
        content_type__app_label='minibox', content_type__model='file')
    serializer_class = FilePermissionSerializer
    permission_classes = [permissions.IsAdminUser | IsCompanyAdministrator]


class UserFilePermissionViewSet(viewsets.ModelViewSet):
    queryset = UserFilePermission.objects.all()
    serializer_class = UserFilePermissionSerializer
    permission_classes = [permissions.IsAdminUser | IsCompanyAdministrator]
