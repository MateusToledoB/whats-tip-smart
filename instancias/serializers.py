from rest_framework import serializers
from urllib.parse import unquote
from .models import InstanciaEncerrada

class InstanciaEncerradaSerializer(serializers.ModelSerializer):
    nome_instancia = serializers.SerializerMethodField()

    class Meta:
        model = InstanciaEncerrada
        fields = '__all__'

    def get_nome_instancia(self, obj):
        # Remove o prefixo id_user:1__ se existir, e decode espaços (%20)
        nome = obj.nome_instancia or ""

        # Se o nome começar com algo tipo 'id_user:X__ ', remove essa parte:
        import re
        nome = re.sub(r'^id_user:\d+__\s*', '', nome)

        # Decodifica caracteres URL (%20 -> espaço)
        nome = unquote(nome)

        return nome
