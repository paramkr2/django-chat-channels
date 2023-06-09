# Generated by Django 4.0 on 2023-04-21 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('chat', '0002_alter_message_options_remove_message_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='req_sender', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requests',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_user', to='auth.user'),
        ),
    ]
