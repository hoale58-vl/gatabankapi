from rest_framework import serializers
from v1.models import (
    Bank, BankDiscount, BankFee, BankRequirement,
    Card, CardBasic, CardBenefit, CardDiscount, CardFee, CardRequirement
)

class AbstractSerializer(serializers.HyperlinkedModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(AbstractSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

## BANK
class BankFeeSerializer(AbstractSerializer):
    class Meta:
        model = BankFee
        fields = '__all__'

class BankRequirementSerializer(AbstractSerializer):
    class Meta:
        model = BankRequirement
        fields = '__all__'

class BankDiscountSerializer(AbstractSerializer):
    class Meta:
        model = BankDiscount
        fields = '__all__'

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
        fields = '__all__'

class CardBenefitSerializer(AbstractSerializer):
    class Meta:
        model = CardBenefit
        fields = '__all__'

class CardDiscountSerializer(AbstractSerializer):
    class Meta:
        model = CardDiscount
        fields = '__all__'

class CardFeeSerializer(AbstractSerializer):
    class Meta:
        model = CardFee
        fields = '__all__'

class CardRequirementSerializer(AbstractSerializer):
    class Meta:
        model = CardRequirement
        fields = '__all__'

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