from rest_framework import serializers

class WeatherDataSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    latitude = serializers.ListField(child=serializers.FloatField())
    longitude = serializers.ListField(child=serializers.FloatField())
    values = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))

    def to_representation(self, instance):
        # Asumiendo que 'instance' es un diccionario con los datos
        return {
            'time': instance['time'],
            'latitude': instance['latitude'],
            'longitude': instance['longitude'],
            'values': instance['values'],
        }

class TemperatureDataSerializer(WeatherDataSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['temperature'] = data.pop('values')  # Renombrar 'values' a 'temperature'
        return data

class PrecipitationDataSerializer(WeatherDataSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['precipitation'] = data.pop('values')  # Renombrar 'values' a 'precipitation'
        return data