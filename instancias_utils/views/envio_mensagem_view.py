import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from datetime import datetime, time, timedelta
import random
import threading
from instancias_utils.services import (
    UtilsService, 
    MainService
)
from instancias.models import AuthUsuarios, InstanciaAtiva , InstanciaEncerrada
import base64

class EnvioMensagem(APIView):
    def post(self, request):
        base_numeros     = request.FILES.get('baseNumeros')
        mensagem         = request.data.get('mensagem')
        arquivo_envio    = request.FILES.get('arquivoEnvio')
        instancia_name   = request.data.get('instanciaName')
        instancia_id     = request.data.get('instanciaID')
        numero_instancia = request.data.get('numeroInstancia') 
        user_id          = request.data.get('id_user')

        if not instancia_name or not instancia_id or not user_id:
            return Response({'erro': 'Requisição mal feita.'}, status=400)

        try:
            df_base = pd.read_excel(base_numeros, engine='openpyxl', dtype={'Numero': str})
            df_base['Numero'] = df_base['Numero'].str.replace(r'\.0$', '', regex=True).str.strip()
            total_linhas = len(df_base)
        except Exception as e:
            return Response({'erro': f'Erro ao ler a planilha: {str(e)}, por favor Verifique o arquivo.'}, status=400)

        if total_linhas == 0:
            return Response({'erro': 'Planilha vazia.'}, status=400)

        agora_dt = datetime.now()
        delays = []

        limite_envio_inicio = 8  # 8h começa o limite
        limite_envio_fim = 18    # 18h é o limite para envio

        max_envios_inicio = 600
        decremento_por_bloco = 50

        if agora_dt.time() >= time(limite_envio_fim, 0):
            return Response({'erro': 'Erro: envio só permitido até as 18h'}, status=400)

        hora_atual = agora_dt.hour

        if hora_atual < limite_envio_inicio:
            limite_atual = max_envios_inicio
        elif hora_atual >= limite_envio_fim:
            limite_atual = 0
        else:
            blocos_passados = hora_atual - limite_envio_inicio
            limite_atual = max_envios_inicio - decremento_por_bloco * blocos_passados
            if limite_atual < 0:
                limite_atual = 0

        if total_linhas > limite_atual:
            return Response({'erro': f'Erro: limite atual é {limite_atual} números, você pediu {total_linhas}'}, status=400)

        if total_linhas <= 100:
            delays = [random.randint(17, 145) for _ in range(total_linhas)]
        else:
            alvo_dt = agora_dt.replace(hour=19, minute=0, second=0, microsecond=0)
            if alvo_dt < agora_dt:
                alvo_dt += timedelta(days=1)

            total_segundos_restantes = int((alvo_dt - agora_dt).total_seconds())
            segundos_restantes = total_segundos_restantes

            for i in range(total_linhas - 1):
                max_delay = int(segundos_restantes / (total_linhas - i) * 2)
                delay = random.randint(10, max(15, max_delay))

                if arquivo_envio:
                    delay = max(5, delay - 5) 

                delays.append(delay)
                segundos_restantes -= delay

            delays.append(segundos_restantes)
            random.shuffle(delays)

        df_base['TempoDelay'] = delays

        if arquivo_envio:
                arquivo_bytes = arquivo_envio.read()
                mediatype = UtilsService.get_media_type(arquivo_envio.name)
                fileName = arquivo_envio.name
                mimetype = arquivo_envio.content_type
                base64_encoded = base64.b64encode(arquivo_bytes).decode('utf-8')
                
        else:
            arquivo_bytes = None
            mediatype = None
            fileName = None
            mimetype = None
            base64_encoded = None
            

        # 1. Envia a resposta imediatamente ao fetch
        response_data = {"sucesso": "O envio vai ser iniciado."}
        response = Response(response_data, status=200)

        # 2. Define função de envio
        def executar_envio():
            MainService.loop_envio(df_base, mensagem, instancia_name, instancia_id, user_id, numero_instancia, arquivo_bytes, mediatype, fileName, mimetype, base64_encoded)

        # 3. Dispara thread
        threading.Thread(target=executar_envio).start()

        # 4. Retorna resposta antes do envio começar
        return response