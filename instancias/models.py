from django.db import models
from users.models import AuthUsuarios  # ajuste o nome do app se necessário
from django.utils import timezone

class InstanciaAtiva(models.Model):
    user_id = models.ForeignKey(AuthUsuarios, on_delete=models.CASCADE, related_name='instancias_criadas', db_column='user_id')
    mensagem_instancia = models.TextField()
    envios_sucesso = models.PositiveIntegerField(default=0)
    envios_erro = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100)
    criada_em = models.DateTimeField(auto_now_add=True)
    id_instancia = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Instância {self.id_instancia} de Usuário {self.user_id_id}"

class InstanciaEncerrada(models.Model):
    user_id = models.ForeignKey(AuthUsuarios, on_delete=models.CASCADE, related_name='instancias_encerradas', db_column='user_id')
    nome_instancia = models.CharField(max_length=300)
    mensagem_instancia = models.TextField()
    numero_instancia = models.CharField(max_length=30)
    envios_sucesso = models.PositiveIntegerField(default=0)
    envios_erro = models.PositiveIntegerField(default=0)
    total_envios = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100)
    criada_em = models.DateTimeField()
    encerrada_em = models.DateTimeField(default=timezone.now)
    id_instancia = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.nome_instancia} - {self.id_instancia}"

    @classmethod
    def encerrar_instancia(cls, instancia_ativa: 'InstanciaAtiva', numero: str, nome: str, status_final: str, mensagem: str = None):
        if mensagem is None:
            mensagem = instancia_ativa.mensagem_instancia
        encerrada =  cls.objects.create(
            user_id=instancia_ativa.user_id,
            nome_instancia=nome,
            numero_instancia=numero,
            mensagem_instancia=mensagem,
            envios_sucesso=instancia_ativa.envios_sucesso,
            envios_erro=instancia_ativa.envios_erro,
            total_envios=instancia_ativa.envios_sucesso + instancia_ativa.envios_erro,
            status=status_final,  # agora usa o status passado como argumento
            criada_em=instancia_ativa.criada_em,
            id_instancia=instancia_ativa.id_instancia
        )
        instancia_ativa.delete()
        return encerrada
