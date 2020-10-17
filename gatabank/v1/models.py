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

class User(AbstractEntity, models.Model):
    phone_number = models.CharField(max_length=300, blank=True, null=False)
    password = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)

    district = models.ForeignKey('v1.District', null=True, default=None, on_delete=models.CASCADE, db_column='district_id')
    city = models.ForeignKey('v1.City', null=True, default=None, on_delete=models.CASCADE, db_column='city_id')
    village = models.ForeignKey('v1.Village', null=True, default=None, on_delete=models.CASCADE, db_column='village_id')
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
    image = models.CharField(max_length=512, blank=True, null=True)
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

    class Meta:
        db_table = 'cards'