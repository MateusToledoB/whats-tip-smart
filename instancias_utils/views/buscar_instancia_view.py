from rest_framework.views import APIView
from rest_framework.response import Response
from instancias_utils.services import MainService
from rest_framework import status
from instancias.models import AuthUsuarios, InstanciaAtiva , InstanciaEncerrada

class BuscaInstancia(APIView):
    def post(self, request):
        id_user = request.data.get('id_user')

        if not id_user:
            return Response({"erro": "id_user não enviado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            instancias = MainService.buscar_instancias_por_usuario(id_user)
            return Response(instancias, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "erro": "Erro na requisição",
                "detalhes": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
