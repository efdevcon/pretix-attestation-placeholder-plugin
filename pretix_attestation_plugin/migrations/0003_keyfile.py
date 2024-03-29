# Generated by Django 3.0.11 on 2021-06-22 12:22

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0174_merge_20201222_1031'),
        ('pretix_attestation_plugin', '0002_attestationlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyFile',
            fields=[
                ('upload', models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to='pretix_attestation_plugin/keyfiles/')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pretixbase.Event')),
            ],
        ),
    ]
