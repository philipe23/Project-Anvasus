# Generated by Django 4.1 on 2022-08-22 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_professor_termos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topico',
            name='descricao',
            field=models.TextField(max_length=500),
        ),
    ]
