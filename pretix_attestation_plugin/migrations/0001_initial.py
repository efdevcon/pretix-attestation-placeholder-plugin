# Generated by Django 3.0.11 on 2021-01-30 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pretixbase', '0174_merge_20201222_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseURL',
            fields=[
                ('string_url', models.CharField(max_length=4096)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pretixbase.Event')),
            ],
        ),
    ]
