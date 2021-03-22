# Generated by Django 3.1.1 on 2021-03-21 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regularuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='regularuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='regularuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='regularuser',
            name='password',
        ),
        migrations.AddField(
            model_name='regularuser',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='regularuser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='regularuser',
            name='user_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='regularuser',
            name='gender',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.CreateModel(
            name='OrganizerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('granted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('regular_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizers', to='app.regularuser')),
            ],
            options={
                'db_table': 'Organizer',
            },
        ),
        migrations.CreateModel(
            name='AdministratorUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('granted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('regular_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administrators', to='app.regularuser')),
            ],
            options={
                'db_table': 'Administrator',
            },
        ),
    ]