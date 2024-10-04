from django.urls import path
from .views import TemperatureDataView, PrecipitationDataView

urlpatterns = [
    path('temperature/', TemperatureDataView.as_view(), name='temperature-data'),
    path('precipitation/', PrecipitationDataView.as_view(), name='precipitation-data'),
]