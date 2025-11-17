
class DBService():
    @classmethod
    def salvar_envio_com_status(cls, instancia_obj, response):
        if response.status_code == 201:
            instancia_obj.envios_sucesso += 1
        else:
            instancia_obj.envios_erro += 1
        instancia_obj.save()

