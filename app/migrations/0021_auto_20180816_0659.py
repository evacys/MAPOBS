# Generated by Django 2.0.5 on 2018-08-16 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20180816_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='cb_ids',
            field=models.ManyToManyField(to='app.Bibliographic'),
        ),
        migrations.AlterField(
            model_name='mntortho',
            name='cb_ids',
            field=models.ManyToManyField(to='app.Bibliographic'),
        ),
        migrations.AlterField(
            model_name='mntortho',
            name='flow_ids',
            field=models.ManyToManyField(to='app.Flow'),
        ),
    ]
