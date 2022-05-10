# Generated by Django 2.2 on 2022-05-10 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210827_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalUserBitgoWalletAddress',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('wallet_address', models.CharField(blank=True, max_length=120, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user bitgo wallet address',
                'db_table': 'user_bitgo_wallet_address_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='UserBitgoWalletAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wallet_address', models.CharField(blank=True, max_length=120, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bitgo_wallet_address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_bitgo_wallet_address',
            },
        ),
        migrations.RemoveField(
            model_name='classes',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='classsection',
            name='section_class',
        ),
        migrations.RemoveField(
            model_name='historicalbranch',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalclasses',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='historicalclasses',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalclasssection',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalclasssection',
            name='section_class',
        ),
        migrations.RemoveField(
            model_name='historicaluserclassdetails',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='historicaluserclassdetails',
            name='classes',
        ),
        migrations.RemoveField(
            model_name='historicaluserclassdetails',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluserclassdetails',
            name='user',
        ),
        migrations.RemoveField(
            model_name='historicalusersectiondetails',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalusersectiondetails',
            name='section',
        ),
        migrations.RemoveField(
            model_name='historicalusersectiondetails',
            name='user_class',
        ),
        migrations.RemoveField(
            model_name='historicalusersession',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalusersession',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userclassdetails',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='userclassdetails',
            name='classes',
        ),
        migrations.RemoveField(
            model_name='userclassdetails',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usersectiondetails',
            name='section',
        ),
        migrations.RemoveField(
            model_name='usersectiondetails',
            name='user_class',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='user',
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
        migrations.DeleteModel(
            name='Classes',
        ),
        migrations.DeleteModel(
            name='ClassSection',
        ),
        migrations.DeleteModel(
            name='HistoricalBranch',
        ),
        migrations.DeleteModel(
            name='HistoricalClasses',
        ),
        migrations.DeleteModel(
            name='HistoricalClassSection',
        ),
        migrations.DeleteModel(
            name='HistoricalUserClassDetails',
        ),
        migrations.DeleteModel(
            name='HistoricalUserSectionDetails',
        ),
        migrations.DeleteModel(
            name='HistoricalUserSession',
        ),
        migrations.DeleteModel(
            name='UserClassDetails',
        ),
        migrations.DeleteModel(
            name='UserSectionDetails',
        ),
        migrations.DeleteModel(
            name='UserSession',
        ),
        migrations.AddIndex(
            model_name='userbitgowalletaddress',
            index=models.Index(fields=['id', 'wallet_address'], name='user_bitgo__id_56d0be_idx'),
        ),
    ]
