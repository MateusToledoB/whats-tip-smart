import pandas as pd

class UtilsService():
    @classmethod
    def substituir_variaveis(cls, mensagem, dados_destinatario):
        mensagem_formatada = mensagem

        for chave, valor in dados_destinatario.items():
            placeholder = f"{{{{{chave}}}}}"  # transforma em {{chave}}, como {{nome}}
            mensagem_formatada = mensagem_formatada.replace(placeholder, str(valor))

        return mensagem_formatada
    
    @classmethod
    def get_media_type(cls, filename):
        ext = filename.lower().split('.')[-1]

        imagens = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        videos = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']
        audios = ['mp3', 'wav', 'ogg', 'm4a', 'flac']
        documentos = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt']

        if ext in imagens:
            return "image"
        elif ext in videos:
            return "video"
        elif ext in audios:
            return "audio"
        elif ext in documentos:
            return "document"
        else:
            return "document"  # padrão para extensões desconhecidas