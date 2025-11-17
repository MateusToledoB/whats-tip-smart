from django.urls import path, include
from .views import CriarInstancia, GerarQrCodeInstancia, DeleteInstancia, BuscaInstancia, EnvioMensagem

urlpatterns = [
    path('criar/', CriarInstancia.as_view(), name='criar-instancia'),
    path('gerar_qr_code/', GerarQrCodeInstancia.as_view(), name='gerar_qr_code'),
    path('delete/', DeleteInstancia.as_view(), name='delte'),
    path('buscar/', BuscaInstancia.as_view(), name='buscar'),
    path('loop_envio/', EnvioMensagem.as_view(), name='loop_envio'),
]
