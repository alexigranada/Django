from .models import Estacion
from .models import Niebla
from rest_framework import viewsets, permissions
from .serializers import EstacionSerializer, NieblaSerializer

class EstacionViewSet (viewsets.ModelViewSet):
    queryset = Estacion.objects.all()
    permissions_classes = [permissions.AllowAny]
    serializer_class = EstacionSerializer

class NieblaViewSet (viewsets.ModelViewSet):
    queryset = Niebla.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = NieblaSerializer