# Generated by Django 3.1.6 on 2021-02-09 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_date', models.DateField(null=True)),
                ('deadline', models.DateField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('pushed_on_portal', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'NEW'), (1, 'IN_PROGRESS'), (2, 'READY_TO_REVIEW'), (3, 'APPROVED'), (4, 'REJECTED'), (4, 'READY_TO_UPLOAD'), (5, 'CANCELLED'), (6, 'UPLOADED')], default=0)),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='given_by', to=settings.AUTH_USER_MODEL)),
                ('given_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='given_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=200)),
                ('reg_price', models.FloatField(blank=True, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('curr_price', models.FloatField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'NOT_REVIEWED'), (1, 'APPROVED'), (2, 'REJECTED'), (3, 'UPLOADED')], default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('last_mod_onsite', models.DateTimeField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
    ]
