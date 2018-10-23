# Generated by Django 2.0.5 on 2018-07-30 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='cc_id_load',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flow_cc_id_load', related_query_name='flow_fissure_id', to='app.Contact'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='cc_id_pub',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flow_cc_id_pub', related_query_name='flow_fissure_id', to='app.Contact'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='fissure_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flow_fissure_id', related_query_name='flow_fissure_id', to='app.Fissure'),
        ),
    ]