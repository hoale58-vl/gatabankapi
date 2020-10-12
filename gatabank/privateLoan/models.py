from django.db import models
from interfaces.models import  AbstractEntity

class BankRequirement(AbstractEntity, models.Model):
    bank = models.ForeignKey('creditCard.Bank', null=True, default=None, on_delete=models.CASCADE, db_column='bank_id')
    age = models.CharField(max_length=512, blank=True, null=True)
    personalIdentifier = models.CharField(max_length=512, blank=True, null=True)
    incomeIdentifier = models.CharField(max_length=512, blank=True, null=True)
    homeIdentifier = models.CharField(max_length=512, blank=True, null=True)
    other = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'bank_requirements'

class BankFee(AbstractEntity, models.Model):
    bank = models.ForeignKey('creditCard.Bank', null=True, default=None, on_delete=models.CASCADE, db_column='bank_id')
    penaltyFee = models.CharField(max_length=512, blank=True, null=True)
    penaltyInterest = models.CharField(max_length=512, blank=True, null=True)
    earlierPaymentFee = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'bank_fees'

class BankDiscount(AbstractEntity, models.Model):
    bank = models.ForeignKey('creditCard.Bank', null=True, default=None, on_delete=models.CASCADE, db_column='bank_id')
    label = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'bank_discounts'

class Bank(AbstractEntity, models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    image = models.CharField(max_length=512, blank=True, null=True)
    minLoanAmount = models.IntegerField(blank=True, null=True)
    maxLoanAmount = models.IntegerField(max_length=512, blank=True, null=True)
    interestPercentage = models.IntegerField(max_length=512, blank=True, null=True)
    interestType = models.CharField(max_length=512, blank=True, null=True)
    minIncome = models.IntegerField(max_length=512, blank=True, null=True)
    minLoanTerm = models.CharField(max_length=512, blank=True, null=True)
    maxLoanTerm = models.CharField(max_length=512, blank=True, null=True)
    verifiedIn = models.CharField(max_length=512, blank=True, null=True)
    interestCalMethod = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'banks'