from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from miniboxapi.models import *
from rest_framework import viewsets
from rest_framework import permissions
from miniboxapi.serializers import *
from miniboxapi.permissions import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # API endpoint that allows users to be viewed or edited
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrCompanyAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all().order_by('-date_joined')
        else:
            return User.objects.filter(profile__company=user.profile.company)


class GroupViewSet(viewsets.ModelViewSet):
    # API endpoint that allows users to be viewed or edited
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrCompanyAdmin]

    def get_queryset(self):
        u = self.request.user
        if u.is_superuser:
            return Profile.objects.all()
        return Profile.objects.filter(company=u.profile.company)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProfileSerializer
        return CompanyAdminProfileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserFilePermissionViewSet(viewsets.ModelViewSet):
    queryset = UserFilePermission.objects.all()
    serializer_class = UserFilePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
