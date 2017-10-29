# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skosxl', '0006_auto_20171019_1546'),
        ('eras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EraSource',
            fields=[
                ('importedconceptscheme_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='skosxl.ImportedConceptScheme')),
                ('startTimeProperty', models.CharField(blank=True, help_text='RDF property path for era start time. prefixes must be registered in RDF_IO.namespaces', max_length=200, null=True)),
                ('startTimeUncertProperty', models.CharField(blank=True, help_text='RDF property path for era start time uncertainty measure. prefixes must be registered in RDF_IO.namespaces', max_length=200, null=True)),
                ('endTimeProperty', models.CharField(blank=True, help_text='RDF property path for era end time. prefixes must be registered in RDF_IO.namespaces', max_length=200, null=True)),
                ('endTimeUncertProperty', models.CharField(blank=True, help_text='RDF property path for era end time uncertainty measure. prefixes must be registered in RDF_IO.namespaces', max_length=200, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eras.EraFrame')),
            ],
            bases=('skosxl.importedconceptscheme',),
        ),
    ]
