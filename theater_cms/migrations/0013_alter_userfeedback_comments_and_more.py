# Generated by Django 5.1.4 on 2025-05-09 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater_cms', '0012_alter_sitesettings_display_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfeedback',
            name='comments',
            field=models.TextField(max_length=500, verbose_name='User Feedback'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, '1 Star'), (2, '2 Star'), (3, '3 Star'), (4, '4 Star'), (5, '5 Star')], null=True, verbose_name='User Rating'),
        ),
    ]
