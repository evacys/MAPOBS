# Generated by Django 2.0.5 on 2018-08-21 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20180821_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volcano',
            name='cc_id1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vd_cc_id1', to='app.Contact'),
        ),
    ]