# Generated by Django 3.2.15 on 2025-06-24 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genefamily', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genefamily',
            name='gene_list',
        ),
    ]
