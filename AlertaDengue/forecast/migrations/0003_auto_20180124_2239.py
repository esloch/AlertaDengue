# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-24 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0002_create_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastcases',
            name='cid10',
            field=models.ForeignKey(db_column='cid10', help_text='Doença', on_delete=django.db.models.deletion.DO_NOTHING, to='dados.CID10'),
        ),
        migrations.AlterField(
            model_name='forecastcases',
            name='city',
            field=models.ForeignKey(db_column='geocode', help_text='Cidade', on_delete=django.db.models.deletion.DO_NOTHING, to='dados.City'),
        ),
        migrations.AlterField(
            model_name='forecastcases',
            name='forecast_model',
            field=models.ForeignKey(db_column='forecast_model_id', help_text='Modelo de Previsão', on_delete=django.db.models.deletion.DO_NOTHING, to='forecast.ForecastModel'),
        ),
        migrations.AlterField(
            model_name='forecastcity',
            name='city',
            field=models.ForeignKey(db_column='geocode', help_text='Código do Município', on_delete=django.db.models.deletion.DO_NOTHING, to='dados.City'),
        ),
        migrations.AlterField(
            model_name='forecastcity',
            name='forecast_model',
            field=models.ForeignKey(db_column='forecast_model_id', help_text='Modelo de Previsão', on_delete=django.db.models.deletion.DO_NOTHING, to='forecast.ForecastModel'),
        ),
    ]