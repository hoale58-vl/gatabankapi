from rest_framework import viewsets
from v1.models import (
    Bank, Card,
    City, District, Village,
)
from rest_framework.generics import ListAPIView
from v1.serializers import (
    BankSerializer, CardSerializer, 
    CitySerializer, DistrictSerializer, VillageSerializer,
)
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer

class CityViewList(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DistrictViewList(ListAPIView):
    serializer_class = DistrictSerializer
    def get_queryset(self):
        return District.objects.filter(city_id = self.kwargs['city_id'])

class VillageViewList(ListAPIView):
    serializer_class = VillageSerializer
    def get_queryset(self):
        return Village.objects.filter(district_id = self.kwargs['district_id'])

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer