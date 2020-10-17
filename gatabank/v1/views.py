from rest_framework import viewsets
from v1.models import Bank, Card
from v1.serializers import BankSerializer, CardSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer

class BankViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer