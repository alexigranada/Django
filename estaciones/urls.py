from django.urls import path, include 
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .api import EstacionViewSet
from .api import NieblaViewSet

router = routers.DefaultRouter()

router.register(r'estaciones', EstacionViewSet, 'estaciones')
router.register(r'niebla', NieblaViewSet, 'niebla')

urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='Estaciones API'))
]

#