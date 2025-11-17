from django import db
from instancias.models import AuthUsuarios, InstanciaAtiva , InstanciaEncerrada
from instancias_utils.services import (
    EvolutionService,
    UtilsService,
    DBService
)

class MainService():
    @classmethod
    def loop_envio(cls, df_base, mensagem, instancia_name, instancia_id, user_id, numero_instancia, arquivo_bytes, mediatype, fileName, mimetype, base64_encoded):
        try:
            instancia_obj = InstanciaAtiva.objects.get(id_instancia=instancia_id)
        except InstanciaAtiva.DoesNotExist:
            usuario = AuthUsuarios.objects.get(id_user=user_id)
            instancia_obj = InstanciaAtiva.objects.create(
                user_id=usuario,
                mensagem_instancia=mensagem,
                envios_sucesso=0,
                envios_erro=0,
                status="Enviando",
                id_instancia=instancia_id
            )

        instancia_encerrada = False  # flag de controle

        try:
            for _, row in df_base.iterrows():
                db.close_old_connections()
                
                numero = row.get('Numero')
                numero_formatado = f'55{numero}'
                verificacao_numero = EvolutionService.verifica_numero_valido(instancia_name, numero_formatado)

                if verificacao_numero == 'erro' and not instancia_encerrada:
                    if mensagem_personalizada is not None:
                        mensagem_historico = mensagem_personalizada
                    else:
                        mensagem_historico = fileName

                    InstanciaEncerrada.encerrar_instancia(
                        instancia_obj, 
                        numero_instancia, 
                        instancia_name,
                        status_final="Conexão interrompida", 
                        mensagem = mensagem_historico
                    )
                    instancia_encerrada = True
                    break

                elif verificacao_numero is False:
                    instancia_obj.envios_erro += 1
                    instancia_obj.save()
                    continue

                elif verificacao_numero is True:
                    delay = int(float(row.get('TempoDelay', 0)) * 1000)

                    response_msg = None
                    response_arquivo = None
                    mensagem_personalizada = UtilsService.substituir_variaveis(mensagem, row) if mensagem else None

                    match (bool(mensagem), bool(arquivo_bytes)):
                        case (True, False):
                            response_msg = EvolutionService.envia_mensagem(mensagem_personalizada, numero_formatado, instancia_name, delay)
                            if response_msg and getattr(response_msg, 'status_code', None) == 201:
                                DBService.salvar_envio_com_status(instancia_obj, response_msg)
                            elif not instancia_encerrada:
                                if mensagem_personalizada is not None:
                                    mensagem_historico = mensagem_personalizada
                                else:
                                    mensagem_historico = fileName

                                InstanciaEncerrada.encerrar_instancia(
                                    instancia_obj, 
                                    numero_instancia, 
                                    instancia_name,
                                    status_final="Conexão interrompida", 
                                    mensagem = mensagem_historico
                                )
                                instancia_encerrada = True
                                break

                        case (True, True):
                            response_msg = EvolutionService.envia_mensagem(mensagem_personalizada, numero_formatado, instancia_name, delay)
                            if response_msg and getattr(response_msg, 'status_code', None) == 201:
                                response_arquivo = EvolutionService.envia_arquivo_e_mensagem(
                                    instancia_name, numero_formatado, mediatype,
                                    fileName, base64_encoded, mimetype, 5000)
                                if response_arquivo and getattr(response_arquivo, 'status_code', None) == 201:
                                    DBService.salvar_envio_com_status(instancia_obj, response_arquivo)
                                elif not instancia_encerrada:
                                    if mensagem_personalizada is not None:
                                        mensagem_historico = mensagem_personalizada
                                    else:
                                        mensagem_historico = fileName

                                    InstanciaEncerrada.encerrar_instancia(
                                        instancia_obj, 
                                        numero_instancia, 
                                        instancia_name,
                                        status_final="Conexão interrompida", 
                                        mensagem = mensagem_historico
                                    )
                                    instancia_encerrada = True
                                    break
                            elif not instancia_encerrada:
                                if mensagem_personalizada is not None:
                                    mensagem_historico = mensagem_personalizada
                                else:
                                    mensagem_historico = fileName

                                InstanciaEncerrada.encerrar_instancia(
                                    instancia_obj, 
                                    numero_instancia, 
                                    instancia_name,
                                    status_final="Conexão interrompida", 
                                    mensagem = mensagem_historico
                                )
                                instancia_encerrada = True
                                break

                        case (False, True):
                            response_arquivo = EvolutionService.envia_arquivo_e_mensagem(
                                instancia_name, numero_formatado, mediatype,
                                fileName, base64_encoded, mimetype, delay)
                            if response_arquivo and getattr(response_arquivo, 'status_code', None) == 201:
                                DBService.salvar_envio_com_status(instancia_obj, response_arquivo)
                            elif not instancia_encerrada:
                                if mensagem_personalizada is not None:
                                    mensagem_historico = mensagem_personalizada
                                else:
                                    mensagem_historico = fileName

                                InstanciaEncerrada.encerrar_instancia(
                                    instancia_obj, 
                                    numero_instancia, 
                                    instancia_name,
                                    status_final="Conexão interrompida", 
                                    mensagem = mensagem_historico
                                )
                                instancia_encerrada = True
                                break

            # encerra só no final se ainda não foi encerrada
            if not instancia_encerrada:
                if mensagem_personalizada is not None:
                    mensagem_historico = mensagem_personalizada
                else:
                    mensagem_historico = fileName

                InstanciaEncerrada.encerrar_instancia(
                    instancia_obj, 
                    numero_instancia, 
                    instancia_name,
                    status_final="Encerrada com sucesso", 
                    mensagem = mensagem_historico
                )
                instancia_encerrada = True
        
        except Exception as e:
            print(e)
            if not instancia_encerrada:
                if mensagem_personalizada is not None:
                    mensagem_historico = mensagem_personalizada
                else:
                    mensagem_historico = fileName

                InstanciaEncerrada.encerrar_instancia(
                    instancia_obj, 
                    numero_instancia, 
                    instancia_name,
                    status_final="Conexão interrompida", 
                    mensagem = mensagem_historico
                )
                instancia_encerrada = True
    
    @classmethod
    def buscar_instancias_por_usuario(cls, id_user):
        response = EvolutionService.busca_instancias()
        response.raise_for_status()

        todas_instancias = response.json()
        termo_busca = f"id_user:{id_user}__ "

        instancias_filtradas = []

        for inst in todas_instancias:
            nome_completo = inst.get("name", "")
            if nome_completo.startswith(termo_busca):
                nome_limpo = nome_completo.replace(termo_busca, "")

                try:
                    instancia_ativa = InstanciaAtiva.objects.get(id_instancia=inst.get("id"))
                except InstanciaAtiva.DoesNotExist:
                    instancia_ativa = None

                if instancia_ativa:
                    envios_certos = instancia_ativa.envios_sucesso
                    envios_errados = instancia_ativa.envios_erro
                    mensagem = instancia_ativa.mensagem_instancia
                    connection_status = instancia_ativa.status
                else:
                    envios_certos = ""
                    envios_errados = ""
                    mensagem = ""
                    connection_status = inst.get("connectionStatus")

                instancias_filtradas.append({
                    "name": nome_limpo,
                    "number": inst.get("number"),
                    "connectionStatus": connection_status,
                    "id": inst.get("id"),
                    "envios_certos": envios_certos,
                    "envios_errados": envios_errados,
                    "mensagem": mensagem
                })
        return instancias_filtradas