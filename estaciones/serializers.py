from rest_framework import serializers
from .models import Estacion
from .models import Niebla

class EstacionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Estacion
        fields = ('id', 'nombre', 'municipio', 'altura')
        read_only_fields = ('id',)

class NieblaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Niebla
        fields = ('id', 'fecha', 'temperatura', 'niebla', 'estacion')
        read_only_fields = ('id',)