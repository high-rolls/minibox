from django.db import models
from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver
from pycpfcnpj import cpf, cnpj


def validate_cnpj(value):
    if not cnpj.validate(value):
        raise ValidationError("%s is not a valid CNPJ number." % value)


def validate_cpf(value):
    if not cpf.validate(value):
        raise ValidationError("%s is not a valid CPF number." % value)


class PhoneNumber(models.Model):
    country_code = models.CharField(max_length=3)
    area_code = models.CharField(max_length=3, blank=True)
    local_number = models.CharField(max_length=15)

    def __str__(self):
        return "+%s (%s) %s" % (self.country_code, self.area_code, self.local_number)


class Company(models.Model):
    cnpj = models.CharField(max_length=14, validators=[validate_cnpj])
    trade_name = models.CharField(max_length=200)
    phone_number = models.OneToOneField(
        PhoneNumber, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return "%s" % self.trade_name


# Profile extends the default user model from Django using a one-to-one link (https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone)
# Fields declared in here can be accessed with user.profile.<field>
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cpf = models.CharField(unique=True, max_length=11,
                           validators=[validate_cpf])
    phone_number = models.OneToOneField(
        PhoneNumber, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "%s at %s" % (self.user.username, self.company.trade_name)


"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""


class File(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=4096, blank=True)
    is_directory = models.BooleanField()

    class Meta:
        constraints = [
            UniqueConstraint(
                name='file_unique_trio',
                fields=['company', 'name', 'path']
            )
        ]
        permissions = [('can_view', 'Can view file'),
                       ('can_download', 'Can download file')]

    def __str__(self):
        s = "%s/%s" % (self.path, self.name)
        if self.is_directory:
            s += '/'
        return s


class GroupFilePermission(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return "Group %s can %s %s" % (self.group, self.permission.lower(), self.file)


class UserFilePermission(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE)

    def __str__(self):
        return "%s can %s %s." % (self.user, str(self.permission).lower(), self.file)
