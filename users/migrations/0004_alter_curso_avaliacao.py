# Generated by Django 4.1 on 2022-08-22 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_curso_avaliacao_alter_curso_ementa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='avaliacao',
            field=models.TextField(choices=[('Prova', 'Prova'), ('Trabalho', 'Trabalho'), ('Projeto', 'Projeto')], max_length=500),
        ),
    ]
