from django.urls import path, include
from v1.views import BankViewSet, CardViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'banks', BankViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]