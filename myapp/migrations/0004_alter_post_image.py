# Generated by Django 5.1.4 on 2024-12-26 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.URLField(blank=True, default='', max_length=500, null=True),
        ),
    ]