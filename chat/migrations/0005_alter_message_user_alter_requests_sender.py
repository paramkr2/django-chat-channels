# Generated by Django 4.0 on 2023-04-22 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('chat', '0004_remove_message_user1_remove_message_user2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_msg', to='users.user'),
        ),
        migrations.AlterField(
            model_name='requests',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_sender', to='users.user'),
        ),
    ]