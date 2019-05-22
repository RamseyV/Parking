# Generated by Django 2.1.7 on 2019-04-04 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkingspot',
            old_name='bottom',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='parkingspot',
            old_name='left',
            new_name='y',
        ),
        migrations.RemoveField(
            model_name='parkingspot',
            name='right',
        ),
        migrations.RemoveField(
            model_name='parkingspot',
            name='top',
        ),
        migrations.AddField(
            model_name='parkingspot',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='parkingspot',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True),
        ),
    ]