# Generated by Django 3.1.1 on 2021-03-24 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('event_type', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_approved', models.BooleanField(default=False)),
                ('upvotes_count', models.IntegerField(default=0)),
                ('street', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('province', models.CharField(blank=True, default='', max_length=128, null=True)),
            ],
            options={
                'db_table': 'Event',
            },
        ),
        migrations.CreateModel(
            name='RegularUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_organizer', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('user_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('user_type', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='app.event')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senders', to='app.regularuser')),
            ],
            options={
                'db_table': 'Request',
            },
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
