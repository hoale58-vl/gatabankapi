from django.urls import path, include
from v1.views import (
    BankViewSet, CardViewSet,
    CityViewList, DistrictViewList, VillageViewList,
    UserViewSet, CollaboratorViewSet
)

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'banks', BankViewSet)
router.register(r'cards', CardViewSet)
router.register(r'users', UserViewSet)
router.register(r'collaborators', CollaboratorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cities/', CityViewList.as_view()),
    path('districts/<city_id>', DistrictViewList.as_view()),
    path('villages/<district_id>', VillageViewList.as_view()),
]