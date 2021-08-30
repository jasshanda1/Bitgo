# Generated by Django 2.2 on 2021-08-27 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210826_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='role',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='1. Admin, 2. Sub Admin, 3. Student, 4. Administrator 5. Teachers, 6. AID, 7. Others', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.Role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, help_text='1. Admin, 2. Sub Admin, 3. Student, 4. Administrator 5. Teachers, 6. AID, 7. Others', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Role'),
        ),
        migrations.CreateModel(
            name='UserSectionDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=True)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ClassSection')),
                ('user_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_sections', to='api.UserClassDetails')),
            ],
            options={
                'db_table': 'user_section_details',
            },
        ),
        migrations.CreateModel(
            name='HistoricalUserSectionDetails',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
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
                ('section', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.ClassSection')),
                ('user_class', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.UserClassDetails')),
            ],
            options={
                'verbose_name': 'historical user section details',
                'db_table': 'user_section_details_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddIndex(
            model_name='usersectiondetails',
            index=models.Index(fields=['id'], name='user_sectio_id_3ef184_idx'),
        ),
    ]
