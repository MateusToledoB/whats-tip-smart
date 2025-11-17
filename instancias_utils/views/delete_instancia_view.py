from rest_framework.views import APIView
from rest_framework.response import Response
from instancias_utils.services import EvolutionService
from rest_framework import status
from instancias.models import AuthUsuarios, InstanciaAtiva , InstanciaEncerrada

class DeleteInstancia(APIView):
    def post(self, request):
        data = request.data
        id_user = data.get("id_user")
        id_instancia = data.get("id_instancia")
        nome_puro = data.get("name_instancia")

        # Reconstrói o nome salvo no backend para fazer a exclusão corretamente
        name_instancia_completo = f"id_user:{id_user}__ {nome_puro}"

        response = EvolutionService.deleta_instancia(name_instancia_completo)

        if response.status_code == 200:
            try:
                instancia = InstanciaAtiva.objects.get(id_instancia=id_instancia)
                instancia.delete()
                return Response(status=status.HTTP_200_OK)
            except InstanciaAtiva.DoesNotExist:
                return Response({
                    "warning": "Instância não encontrada no banco, mas foi removida na API externa."
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Falha ao deletar a instância.",
                "status_code": response.status_code,
                "detalhes": response.text
            }, status=status.HTTP_502_BAD_GATEWAY)