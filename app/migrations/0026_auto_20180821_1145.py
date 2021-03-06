# Generated by Django 2.0.5 on 2018-08-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20180816_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eruption',
            name='ed_climax',
            field=models.DateTimeField(null=True, verbose_name='Onset of climax'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_climax_bc',
            field=models.IntegerField(null=True, verbose_name='Year of climax time before Christ'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_climax_unc',
            field=models.DateTimeField(null=True, verbose_name='Onset of climax uncertainty'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_code',
            field=models.CharField(max_length=30, null=True, verbose_name='EruptionCode'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_com',
            field=models.CharField(max_length=255, null=True, verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_etime',
            field=models.DateTimeField(null=True, verbose_name='End time'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_etime_bc',
            field=models.IntegerField(null=True, verbose_name='Year of end time before Christ'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_etime_unc',
            field=models.DateTimeField(null=True, verbose_name='End time uncertainty'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_loaddate',
            field=models.DateTimeField(null=True, verbose_name='Load date, the date the data was entered (in UTC)'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_name',
            field=models.CharField(max_length=60, null=True, verbose_name='EruptionName'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_nar',
            field=models.CharField(max_length=255, null=True, verbose_name='Narrative'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_pubdate',
            field=models.DateTimeField(null=True, verbose_name='Publish date, the date the data become public'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_stime',
            field=models.DateTimeField(null=True, verbose_name='Start time'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_stime_bc',
            field=models.IntegerField(null=True, verbose_name='Year of start time before Christ'),
        ),
        migrations.AlterField(
            model_name='eruption',
            name='ed_stime_unc',
            field=models.DateTimeField(null=True, verbose_name='Start time uncertainty'),
        ),
    ]
