from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from instancias_utils.services import EvolutionService
import requests
from instancias.models import AuthUsuarios, InstanciaAtiva , InstanciaEncerrada

class GerarQrCodeInstancia(APIView):
    def post(self, request):
        data           = request.data
        id_user        = data.get("id_user")
        name_instancia = data.get("name_instancia")
        name_instancia = f"id_user:{id_user}__ {name_instancia}"

        try:
            # 1. Limpa sessão antiga
            EvolutionService.logout(name_instancia)

            # 2. Gera QR Code
            response = EvolutionService.gera_qr_code(name_instancia)

            response.raise_for_status()

            data_response = response.json()

            return Response({
                "base64": data_response.get("base64")
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            if e.response is not None:
                print("ERRO RESPONSE:", e.response.text)
            return Response({
                "error": "Erro ao gerar QR code",
                "details": str(e),
                "response": getattr(e.response, "text", None)
            }, status=status.HTTP_400_BAD_REQUEST)

