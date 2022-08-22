# Generated by Django 4.1 on 2022-08-22 00:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_curso_avaliacao_curso_ementa_alter_curso_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='avaliacao',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='curso',
            name='ementa',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='curso',
            name='objetivo',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='curso',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='curso',
            name='status',
            field=models.CharField(choices=[('Aprovado', 'Aprovado'), ('Pendente', 'Pendente'), ('Recusado', 'Recusado')], default='Pendente', max_length=120),
        ),
        migrations.AlterField(
            model_name='curso',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.tema'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='termos',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='topico',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.curso'),
        ),
        migrations.AlterField(
            model_name='topico',
            name='descricao',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]