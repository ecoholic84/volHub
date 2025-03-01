# Generated by Django 5.1.5 on 2025-03-01 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0012_tbl_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_industry')),
            ],
        ),
    ]
