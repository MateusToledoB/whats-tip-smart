from rest_framework import viewsets, permissions
from .models import InstanciaEncerrada
from .serializers import InstanciaEncerradaSerializer

class InstanciaEncerradaViewSet(viewsets.ModelViewSet):
    serializer_class = InstanciaEncerradaSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('id_user')
        if user_id:
            return (
                InstanciaEncerrada.objects
                .filter(user_id=user_id)
                .order_by('-encerrada_em')[:50]
            )
        return InstanciaEncerrada.objects.none()


