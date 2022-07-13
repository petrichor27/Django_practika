# Generated by Django 3.2.9 on 2022-07-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20220710_1738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rule',
            options={'verbose_name': 'Правило', 'verbose_name_plural': 'Список правил'},
        ),
        migrations.AlterField(
            model_name='rule',
            name='queue',
            field=models.CharField(choices=[('Очередь 1', 'Очередь 1'), ('Очередь 2', 'Очередь 2'), ('Очередь 3', 'Очередь 3'), ('Очередь 4', 'Очередь 4')], default='-', max_length=200, verbose_name='Очередь'),
        ),
        migrations.AlterField(
            model_name='task',
            name='attribute',
            field=models.CharField(choices=[('Тип задания 1', 'Тип задания 1'), ('Тип задания 2', 'Тип задания 2'), ('Тип задания 3', 'Тип задания 3'), ('Тип клиента', 'Тип клиента'), ('Признак запроса ОГВ', 'Признак запроса ОГВ'), ('Признак соответствия суммы критериям НС', 'Признак соответствия суммы критериям НС'), ('Статус', 'Статус'), ('Предпочитаемый способ связи', 'Предпочитаемый способ связи'), ('Тип действия', 'Тип действия'), ('Результат действия', 'Результат действия')], default='-', max_length=200, verbose_name='Атрибут'),
        ),
    ]