# Generated by Django 2.0 on 2018-01-11 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('f1better', '0005_auto_20180111_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='f1better.Race'),
        ),
    ]