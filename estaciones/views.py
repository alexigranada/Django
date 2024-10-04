from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EstacionSerializer
from .models import Estacion

from .serializers import NieblaSerializer
from .models import Niebla

# Create your views here.
class EstacionView (viewsets.ModelViewSet):
    serializer_class = EstacionSerializer
    queryset = Estacion.objects.all()

class NieblaView (viewsets.ModelViewSet):
    serializer_class = NieblaSerializer
    queryset = Niebla.objects.all()