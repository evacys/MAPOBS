# Generated by Django 2.0.5 on 2018-07-31 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180731_0444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flow',
            old_name='fissure_id',
            new_name='fissure',
        ),
    ]
