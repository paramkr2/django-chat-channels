# Generated by Django 4.0 on 2023-04-22 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interest',
            name='name',
            field=models.CharField(choices=[('F', 'Footbal'), ('H', 'Hockey')], max_length=1),
        ),
    ]
