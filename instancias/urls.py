from django.urls import path, include
from rest_framework import routers
from .views import InstanciaEncerradaViewSet

router = routers.DefaultRouter()
router.register(r'', InstanciaEncerradaViewSet, basename='instancias')

urlpatterns = [
    path('', include(router.urls)),
]
