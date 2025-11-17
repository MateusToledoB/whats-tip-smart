import requests
import os
from dotenv import load_dotenv
load_dotenv()

class EvolutionService():

    base_url = str(os.getenv('URL_EVOLUTION'))
    api_key = str(os.getenv('SENHA_EVOLUTION'))

    @classmethod
    def criar_instancia(cls, name_instancia, numero_instancia):
        url = f"https://{cls.base_url}/instance/create"
        
        payload = {
            "instanceName": name_instancia,
            "qrcode": True,
            "number": numero_instancia,
            "integration": "WHATSAPP-BAILEYS"
        }
        headers = {
            "apikey": cls.api_key,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return response
    
    @classmethod
    def logout(cls, name_instancia):
        url = f"https://{cls.base_url}/instance/logout/{name_instancia}"
        headers = {
            "apikey": cls.api_key
            }
        response = requests.post(url, headers=headers, verify=False)
        return response

    @classmethod
    def restart_instancia(cls, name_instancia):
        url = f"https://{cls.base_url}/instance/restart/{name_instancia}"
        headers = {
            "apikey": cls.api_key
            }
        response = requests.put(url, headers=headers, verify=False)
        return response


    @classmethod
    def deleta_instancia(cls, name_instancia):
        url = f"https://{cls.base_url}/instance/delete/{name_instancia}"
        headers = {
            "apikey": cls.api_key
            }
        response = requests.delete(url, headers=headers, verify=False)
        return response
    
    @classmethod
    def verifica_numero_valido(cls, instancia_name, numero_formatado):
        if not instancia_name or not numero_formatado:
            raise ValueError("instancia_name ou numero não enviados")

        headers = {
            "apikey": cls.api_key,
            "Content-Type": "application/json"
        }
        payload = {"numbers": [numero_formatado]}
        url = f"https://{cls.base_url}/chat/whatsappNumbers/{instancia_name}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()  # transforma o retorno em Python
                # data pode ser uma lista com um dict dentro
                if isinstance(data, list) and len(data) > 0:
                    existe = data[0].get('exists', False)  # pega o valor de 'exists', padrão False
                    if existe == True:
                        return True
                    else:
                        return False
                else:
                    return 'erro'
            else:
                return 'erro'
        except:
            return 'erro'
        
    @classmethod
    def envia_mensagem(cls, mensagem, numero, instancia_name, delay):
        url = f"https://{cls.base_url}/message/sendText/{instancia_name}"
        headers = {
                "apikey": cls.api_key,
                "Content-Type": "application/json"
            }
        payload = {
            "number": numero,
            "text": mensagem,
            "delay": delay,
            "linkPreview": True,
            "mentionsEveryOne": False
        }
        response = requests.post(url, json=payload, headers=headers)
        return response
    
    @classmethod
    def envia_arquivo_e_mensagem(cls, instancia_name, numero, mediatype, fileName, media, mimetype, delay):
        url = f"https://{cls.base_url}/message/sendMedia/{instancia_name}"
       
        payload = {
            "number": numero,
            "mediatype": mediatype,
            "fileName": fileName,
            "media": media,
            "caption": "",
            "mimetype": mimetype,
            "delay": delay,
            "linkPreview": True
        }

        headers = {
            "apikey": cls.api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response
    
    @classmethod
    def gera_qr_code(cls, name_instancia):
        url = f"https://{cls.base_url}/instance/connect/{name_instancia}"
        headers = {"apikey": cls.api_key}
        response = requests.get(url, headers=headers, verify=True)
        return response
    
    @classmethod
    def busca_instancias(cls):
        headers = {"apikey": cls.api_key}
        url = f"https://{cls.base_url}/instance/fetchInstances"
        response = requests.get(url, headers=headers)
        return response