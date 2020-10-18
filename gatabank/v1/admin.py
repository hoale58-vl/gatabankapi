from django.contrib import admin
from .models import (
    City, District, Village,
    BankDiscount, BankFee, BankRequirement, Bank,
    Card, CardBasic, CardBenefit, CardDiscount, CardFee, CardRequirement,
    User
)
from django import forms

class AbstractModelAdmin():
    exclude = ('status','created_at', 'updated_at',)

@admin.register(City, District, Village)
class AreaAdmin(AbstractModelAdmin, admin.ModelAdmin):
    pass

class BankDiscountInline(AbstractModelAdmin, admin.TabularInline):
    model = BankDiscount

class BankFeeInline(AbstractModelAdmin, admin.TabularInline):
    model = BankFee

class BankRequirementInline(AbstractModelAdmin, admin.TabularInline):
    model = BankRequirement

@admin.register(Bank)
class BankAdmin(AbstractModelAdmin, admin.ModelAdmin):
    inlines = [
        BankDiscountInline, BankFeeInline, BankRequirementInline
    ]

class CardBasicInline(AbstractModelAdmin, admin.TabularInline):
    model = CardBasic

class CardBenefitInline(AbstractModelAdmin, admin.TabularInline):
    model = CardBenefit

class CardDiscountInline(AbstractModelAdmin, admin.TabularInline):
    model = CardDiscount

class CardFeeInline(AbstractModelAdmin, admin.TabularInline):
    model = CardFee

class CardRequirementInline(AbstractModelAdmin, admin.TabularInline):
    model = CardRequirement

@admin.register(Card)
class CardAdmin(AbstractModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'image_tag',]
    inlines = [
        CardBasicInline, CardBenefitInline, CardDiscountInline, CardFeeInline, CardRequirementInline
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('is_staff', 'is_superuser')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)

    def add_view(self, request, extra_context=None):       
        self.exclude = ('last_login', 'is_staff', 'updated_at', 'created_at', 'is_superuser', 'status', )
        return super(UserAdmin, self).add_view(request, extra_context)

    def change_view(self, request, object_id, extra_context=None):       
        self.exclude = ('last_login', 'is_staff', 'updated_at', 'created_at', 'is_superuser', 'status', )
        return super(UserAdmin, self).change_view(request, object_id, extra_context)

class Collaborator(User):
    class Meta:
        proxy = True

@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    exclude = ('is_staff', 'is_superuser')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)

    def save_model(self, request, obj, form, change):
        obj.is_staff = False
        super().save_model(request, obj, form, change)
    
    def add_view(self, request, extra_context=None):       
        self.exclude = ('last_login', 'is_staff', 'updated_at', 'created_at', 'is_superuser', 'status', )
        return super(CollaboratorAdmin, self).add_view(request, extra_context)

    def change_view(self, request, object_id, extra_context=None):       
        self.exclude = ('last_login', 'is_staff', 'updated_at', 'created_at', 'is_superuser', 'status', )
        return super(CollaboratorAdmin, self).change_view(request, object_id, extra_context)