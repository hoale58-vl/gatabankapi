from django.db import models
import uuid
import datetime
from django.core.exceptions import ObjectDoesNotExist, FieldError
from .enum import Status
from django.utils import timezone
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.html import mark_safe

class AbstractEntity(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('created_at', default=datetime.datetime.now)
    updated_at = models.DateTimeField('updated_at', default=datetime.datetime.now)
    status = models.CharField(max_length=300, choices=Status.choices(), blank=True, null=False,
                            default=Status.ACTIVE.name)

    class Meta:
        abstract = True
        ordering = ['-updated_at']

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

class City(AbstractEntity, models.Model):
    name = models.CharField(max_length=300, blank=True, null=False)
    type = models.CharField(max_length=300, blank=True, null=False)

    class Meta:
        db_table = 'cities'

class District(AbstractEntity, models.Model):
    name = models.CharField(max_length=300, blank=True, null=False)
    type = models.CharField(max_length=300, blank=True, null=False)
    city = models.ForeignKey('v1.City', null=True, default=None, on_delete=models.CASCADE, db_column='city_id')

    class Meta:
        db_table = 'districts'

class Village(AbstractEntity, models.Model):
    name = models.CharField(max_length=300, blank=True, null=False)
    type = models.CharField(max_length=300, blank=True, null=False)
    district = models.ForeignKey('v1.District', null=True, default=None, on_delete=models.CASCADE, db_column='district_id')

    class Meta:
        db_table = 'villages'


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, phone_number, password, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractEntity, AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(null=False, unique=True)
    district = models.ForeignKey('v1.District', null=True, default=None, on_delete=models.CASCADE, db_column='district_id')
    city = models.ForeignKey('v1.City', null=True, default=None, on_delete=models.CASCADE, db_column='city_id')
    village = models.ForeignKey('v1.Village', null=True, default=None, on_delete=models.CASCADE, db_column='village_id')
    address = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField('date_of_birth', null=True)
    last_login = models.DateTimeField('last_login', null=True)
    is_staff = models.BooleanField(null=False, default=False)

    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    class Meta:
        db_table = 'users'

class BankRequirement(AbstractEntity, models.Model):
    bank = models.ForeignKey('v1.Bank', null=True, default=None, on_delete=models.CASCADE, db_column='bank_id')
    age = models.CharField(max_length=512, blank=True, null=True)
    personalIdentifier = models.CharField(max_length=512, blank=True, null=True)
    incomeIdentifier = models.CharField(max_length=512, blank=True, null=True)
    homeIdentifier = models.CharField(max_length=512, blank=True, null=True)
    other = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'bank_requirements'

class BankFee(AbstractEntity, models.Model):
    bank = models.ForeignKey('v1.Bank', null=True, default=None, on_delete=models.CASCADE, db_column='bank_id')
    penaltyFee = models.CharField(max_length=512, blank=True, null=True)
    penaltyInterest = models.CharField(max_length=512, blank=True, null=True)
    earlierPaymentFee = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'bank_fees'

class BankDiscount(AbstractEntity, models.Model):
    bank = models.ForeignKey('v1.Bank', null=True, default=None, on_delete=models.CASCADE, db_column='bank_id')
    label = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'bank_discounts'

class Bank(AbstractEntity, models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    image = models.ImageField(upload_to='media/image/banks', blank=True, null=True)
    minLoanAmount = models.IntegerField(blank=True, null=True)
    maxLoanAmount = models.IntegerField(blank=True, null=True)
    interestPercentage = models.IntegerField(blank=True, null=True)
    interestType = models.CharField(max_length=512, blank=True, null=True)
    minIncome = models.IntegerField(blank=True, null=True)
    minLoanTerm = models.CharField(max_length=512, blank=True, null=True)
    maxLoanTerm = models.CharField(max_length=512, blank=True, null=True)
    verifiedIn = models.CharField(max_length=512, blank=True, null=True)
    interestCalMethod = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'banks'
    
    def image_tag(self):
        return mark_safe('<img src="/%s" width="150" height="100" />' % (self.image))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name

class CardDiscount(AbstractEntity, models.Model):
    card = models.ForeignKey('v1.Card', null=True, default=None, on_delete=models.CASCADE, db_column='card_id')
    label = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'card_discounts'

class CardBenefit(AbstractEntity, models.Model):
    card = models.ForeignKey('v1.Card', null=True, default=None, on_delete=models.CASCADE, db_column='card_id')
    label = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'card_benefits'

class CardRequirement(AbstractEntity, models.Model):
    card = models.ForeignKey('v1.Card', null=True, default=None, on_delete=models.CASCADE, db_column='card_id')
    age = models.IntegerField(null=True)
    personalIdentifier = models.CharField(max_length=512, blank=True, null=True)
    incomeRequirement = models.IntegerField(null=True)
    homeIdentifier = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'card_requirements'

class CardFee(AbstractEntity, models.Model):
    card = models.ForeignKey('v1.Card', null=True, default=None, on_delete=models.CASCADE, db_column='card_id')
    cashAdvance = models.CharField(max_length=512, blank=True, null=True)
    latePayment = models.CharField(max_length=512, blank=True, null=True)
    foreignTransaction = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'card_fees'

class CardBasic(AbstractEntity, models.Model):
    card = models.ForeignKey('v1.Card', null=True, default=None, on_delete=models.CASCADE, db_column='card_id')
    freeAirportLounge = models.IntegerField(null=True)
    yearlyFee = models.IntegerField(null=True)
    averageRefund = models.IntegerField(null=True)
    maxRefund = models.IntegerField(null=True)
    cardOrg = models.CharField(max_length=512, blank=True, null=True)
    interest = models.IntegerField(null=True)
    issueFee = models.IntegerField(null=True)
    interestFreeDay = models.IntegerField(null=True)
    paymentEachMonth = models.IntegerField(null=True)

    class Meta:
        db_table = 'card_basics'

class Card(AbstractEntity, models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    sponsor = models.CharField(max_length=512, blank=True, null=True)
    subtitle = models.CharField(max_length=512, blank=True, null=True)
    rating = models.FloatField(null=True)
    image = models.ImageField(upload_to='media/image/cards', blank=True, null=True)
    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="/%s" width="150" height="100" />' % (self.image))

    image_tag.short_description = 'Image'

    class Meta:
        db_table = 'cards'