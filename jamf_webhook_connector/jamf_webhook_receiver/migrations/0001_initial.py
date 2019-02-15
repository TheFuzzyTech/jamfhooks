# Generated by Django 2.1.5 on 2019-01-14 18:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_processed', models.DateTimeField(default=django.utils.timezone.now)),
                ('host_address', models.GenericIPAddressField()),
                ('institution', models.CharField(max_length=250)),
                ('is_cluster_master', models.BooleanField()),
                ('jss_url', models.URLField(max_length=250)),
                ('web_application_path', models.FilePathField()),
            ],
        ),
    ]
