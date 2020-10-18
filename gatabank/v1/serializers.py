from rest_framework import serializers
from v1.models import (
    Bank, BankDiscount, BankFee, BankRequirement,
    Card, CardBasic, CardBenefit, CardDiscount, CardFee, CardRequirement,
    City, District, Village,
    User
)

class AbstractSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(AbstractSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

## USER
class UserSerializer(AbstractSerializer):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser']

## CITY
class CitySerializer(AbstractSerializer):
    class Meta:
        model = City
        fields = '__all__'

## DISTRICT
class DistrictSerializer(AbstractSerializer):
    class Meta:
        model = District
        fields = '__all__'

## VILLAGE
class VillageSerializer(AbstractSerializer):
    class Meta:
        model = Village
        fields = '__all__'

## BANK
class BankFeeSerializer(AbstractSerializer):
    class Meta:
        model = BankFee
        exclude = ['created_at','updated_at', 'id', 'bank']

class BankRequirementSerializer(AbstractSerializer):
    class Meta:
        model = BankRequirement
        exclude = ['created_at','updated_at', 'id', 'bank']

class BankDiscountSerializer(AbstractSerializer):
    class Meta:
        model = BankDiscount
        exclude = ['created_at','updated_at', 'id', 'bank']

class BankSerializer(AbstractSerializer):
    bankFees = BankFeeSerializer(source='card_basic_set', many=True)
    bankRequirements = BankRequirementSerializer(source='card_benefit_set', many=True)
    bankDiscounts = BankDiscountSerializer(source='card_discount_set', many=True)

    class Meta:
        model = Bank
        fields = '__all__'
        extra_fields = ['bankFees', 'bankRequirements', 'bankDiscounts']

## CARD
class CardBasicSerializer(AbstractSerializer):
    class Meta:
        model = CardBasic
        exclude = ['created_at','updated_at', 'id', 'card']

class CardBenefitSerializer(AbstractSerializer):
    class Meta:
        model = CardBenefit
        exclude = ['created_at','updated_at', 'id', 'card']

class CardDiscountSerializer(AbstractSerializer):
    class Meta:
        model = CardDiscount
        exclude = ['created_at','updated_at', 'id', 'card']

class CardFeeSerializer(AbstractSerializer):
    class Meta:
        model = CardFee
        exclude = ['created_at','updated_at', 'id', 'card']

class CardRequirementSerializer(AbstractSerializer):
    class Meta:
        model = CardRequirement
        exclude = ['created_at','updated_at', 'id', 'card']

class CardSerializer(AbstractSerializer):
    cardBasics = CardBasicSerializer(source='card_basic_set', many=True)
    cardBenefits = CardBenefitSerializer(source='card_benefit_set', many=True)
    cardDiscounts = CardDiscountSerializer(source='card_discount_set', many=True)
    cardFees = CardFeeSerializer(source='card_fee_set', many=True)
    cardRequirements = CardRequirementSerializer(source='card_requirement_set', many=True)

    class Meta:
        model = Card
        fields = '__all__'
        extra_fields = ['cardBasics', 'cardBenefits', 'cardDiscounts', 'cardFees', 'cardRequirements']