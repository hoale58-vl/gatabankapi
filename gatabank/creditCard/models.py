from django.db import models
from interfaces.models import  AbstractEntity

class CreditCard(AbstractEntity, models.Model):

    class Meta:
        db_table = 'users'