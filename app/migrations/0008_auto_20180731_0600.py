# Generated by Django 2.0.5 on 2018-07-31 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180731_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flow',
            name='cc_load',
        ),
        migrations.AddField(
            model_name='flow',
            name='cc_id_load',
            field=models.ForeignKey(db_column='cc_id_load', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flow_cc_id_load', to='app.Contact'),
        ),
    ]
