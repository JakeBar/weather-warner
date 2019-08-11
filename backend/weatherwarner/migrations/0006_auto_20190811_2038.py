# Generated by Django 2.2 on 2019-08-11 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weatherwarner', '0005_auto_20190811_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='postcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='weatherwarner.PostCode'),
        ),
    ]
