# Generated by Django 2.2.2 on 2020-11-26 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201126_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='role',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='1. Admin, 2. Doctor, 3. Lab Attendent, 4. Patient', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.Role'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=4, help_text='1. Admin, 2. Doctor, 3. Lab Attendent, 4. Patient', on_delete=django.db.models.deletion.CASCADE, to='api.Role'),
            preserve_default=False,
        ),
    ]
