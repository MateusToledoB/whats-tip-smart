from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from instancias_utils.services import (
    MainService,
    EvolutionService
)
import requests
from instancias.models import AuthUsuarios, InstanciaAtiva , InstanciaEncerrada

class CriarInstancia(APIView):
    def post(self, request):
        data                     = request.data
        name_instancia           = data.get("nome_instancia")
        name_instancia           = name_instancia.strip()
        numero_instancia         = data.get("numero_instancia")
        id_user                  = data.get("id_user")
        name_instancia_formatado = f"id_user:{id_user}__ {name_instancia}"
        
        
        instancias = MainService.buscar_instancias_por_usuario(id_user)

        
        for instancia in instancias:
            
            instancia_existente = instancia["name"].strip()
            numero_existente = instancia["number"]
            if instancia_existente == name_instancia or numero_existente == numero_instancia:
                return Response(
                    {"erro": "Já existe uma instância com esse nome ou número."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        try:
            response = EvolutionService.criar_instancia(name_instancia_formatado, numero_instancia)
            response.raise_for_status()

            if response.status_code == 201:
                return Response(response.json(), status=status.HTTP_201_CREATED)
            else:
                return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)