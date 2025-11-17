from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AuthUsuarios(models.Model):
    id_user = models.AutoField(primary_key=True)  # int auto_increment e PK
    user_login = models.CharField(max_length=30, unique=True)  # varchar(30) e unique
    user_password = models.CharField(max_length=255)  # varchar(255)
    setor = models.CharField(max_length=30, blank=True, null=True)  # varchar(30), pode ser NULL

    class Meta:
        db_table = 'auth_usuarios'  # força o nome da tabela igual ao do banco

    def __str__(self):
        return self.user_login
