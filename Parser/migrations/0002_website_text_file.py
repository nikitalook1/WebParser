# Generated by Django 4.2.11 on 2024-04-18 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='text_file',
            field=models.FileField(blank=True, null=True, upload_to='texts/'),
        ),
    ]