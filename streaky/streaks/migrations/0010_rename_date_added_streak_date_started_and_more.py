# Generated by Django 5.1.3 on 2024-12-08 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaks', '0009_remove_streak_has_ended'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streak',
            old_name='date_added',
            new_name='date_started',
        ),
        migrations.RemoveField(
            model_name='streak',
            name='date_ended',
        ),
        migrations.AlterField(
            model_name='streak',
            name='description',
            field=models.TextField(default='Streak short description...'),
        ),
        migrations.AlterField(
            model_name='streak',
            name='title',
            field=models.CharField(default='Streak title...', max_length=100),
        ),
    ]
