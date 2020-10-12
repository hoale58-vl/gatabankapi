from django.db import models
import uuid
import datetime
from django.core.exceptions import ObjectDoesNotExist, FieldError
from .enum import Status
from django.utils import timezone
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import BaseUserManager

class AbstractEntity(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('created_at', default=datetime.datetime.now)
    updated_at = models.DateTimeField('updated_at', default=datetime.datetime.now)
    status = models.CharField(max_length=300, choices=Status.choices(), blank=True, null=False,
                            default=Status.ACTIVE.name)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(AbstractEntity, self).save(*args, **kwargs)

    @classmethod
    def get_object_by_id(cls, pk):
        try:
            obj = cls.objects.get(pk=pk)
            return obj
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_active_object_by_id(cls, pk):
        return cls.objects.filter(pk=pk, status=Status.ACTIVE.name).first()

class User(AbstractEntity, models.Model):
    phone_number = models.CharField(max_length=300, blank=True, null=False)
    password = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)

    state = models.ForeignKey('interfaces.State', null=True, default=None, on_delete=models.CASCADE, db_column='state_id')
    district = models.ForeignKey('interfaces.District', null=True, default=None, on_delete=models.CASCADE, db_column='district_id')
    city = models.ForeignKey('interfaces.City', null=True, default=None, on_delete=models.CASCADE, db_column='city_id')
    village = models.ForeignKey('interfaces.Village', null=True, default=None, on_delete=models.CASCADE, db_column='village_id')
    address = models.CharField(max_length=500, blank=True, null=True)

    date_of_birth = models.DateField('date_of_birth', null=True)
    last_login = models.DateTimeField('last_login', default=timezone.now)
    is_staff = models.BooleanField(null=False, default=False)
    is_superuser = models.BooleanField(null=False, default=False)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


    username = ""
    objects = BaseUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone', 'name']

    def get_by_natural_key(self):
        return self.phone

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, raw_password):
        if not self.password:
            raise exceptions.AuthenticationFailed(
                _('You have not set a password. Please check your email first or click Forgot Password to set your password'),
                'password_empty',
            )
        return check_password(raw_password, self.password)

    @classmethod
    def get_by_phone_number(cls, phone_number):
        try:
            record = cls.objects.filter(phone_number=phone_number.lower(), status=Status.ACTIVE.name)
            return record.first()
        except Exception as e:
            print(e)
            return None

    class Meta:
        db_table = 'users'
        