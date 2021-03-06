#from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from miniboxapi.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'first_name',
                  'last_name', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'content_type', 'codename']


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = ['app_label', 'model']


class PhoneNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['country_code', 'area_code', 'local_number']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['cnpj', 'trade_name', 'phone_number', 'email']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=True)
    phone_number = PhoneNumberSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['url', 'user', 'company', 'cpf', 'phone_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        company_data = validated_data.pop('company')
        cpf = validated_data.pop('cpf')
        phone_number_data = validated_data.pop('phone_number')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        phone_number = PhoneNumberSerializer.create(
            PhoneNumberSerializer(), validated_data=phone_number_data)
        profile, created = Profile.objects.update_or_create(
            user=user, company=company_data, cpf=cpf, phone_number=phone_number)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        company_data = validated_data.pop('company')
        cpf_data = validated_data.pop('cpf')
        phone_number_data = validated_data.pop('phone_number')
        user = UserSerializer.update(UserSerializer(), user_data)
        phone_number = PhoneNumberSerializer.update_or_create(
            PhoneNumberSerializer(), validated_data=phone_number_data)
        profile, updated = Profile.objects.update(
            user=user, company=company_data, cpf=cpf_data, phone_number=phone_number)
        return profile


class CompanyAdminProfileSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = ['url', 'user', 'cpf', 'phone_number']


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['url', 'company', 'name', 'path', 'is_directory']

    def validate(self, data):
        # check for unique trio
        if File.objects.filter(
            company=data['company'],
            name=data['name'],
            path=data['path']
        ).exists():
            raise serializers.ValidationError(
                "File with the same full path already exists in this company.")


class CompanyFileSerializer(FileSerializer):
    class Meta:
        model = File
        fields = ['url', 'name', 'path', 'is_directory']

    def validate(self, data):
        if File.objects.filter(
            name=data['name'],
            path=data['path']
        ).exists():
            raise serializers.ValidationError(
                "File with the same full name already exists!")


class FilePermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['url', 'name', 'content_type']


class UserFilePermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFilePermission
        fields = ['url', 'user', 'file', 'permission']
