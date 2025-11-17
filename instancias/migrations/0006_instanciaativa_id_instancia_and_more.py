import uuid
from django.db import migrations, models


def gerar_uuids(apps, schema_editor):
    InstanciaAtiva = apps.get_model('instancias', 'InstanciaAtiva')
    for instancia in InstanciaAtiva.objects.filter(id_instancia__isnull=True):
        instancia.id_instancia = uuid.uuid4()
        instancia.save()


class Migration(migrations.Migration):

    dependencies = [
        ('instancias', '0005_instanciaativa_numero_instancia'),
    ]

    operations = [
        # 1. Cria campo id_instancia sem unique e permitindo null
        migrations.AddField(
            model_name='instanciaativa',
            name='id_instancia',
            field=models.UUIDField(null=True, editable=False),
        ),

        # 2. Preenche os valores únicos para cada registro existente
        migrations.RunPython(gerar_uuids),

        # 3. Altera campo para unique=True e null=False
        migrations.AlterField(
            model_name='instanciaativa',
            name='id_instancia',
            field=models.UUIDField(unique=True, editable=False, null=False),
        ),

        migrations.AlterField(
            model_name='instanciaativa',
            name='status',
            field=models.CharField(
                choices=[('desconectada', 'Desconectada'),
                         ('conectada', 'Conectada'),
                         ('enviando', 'Enviando mensagens')],
                default='inativa',
                max_length=50,
            ),
        ),
    ]
