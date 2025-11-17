from rest_framework import serializers
from users.models import AuthUsuarios

class AuthUsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUsuarios
        fields = '__all__'  # ou lista os campos: ['id_user', 'user_login', 'user_password', 'setor']
