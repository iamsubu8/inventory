# Generated by Django 5.0.2 on 2024-02-15 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_inventoryapproval_role_userprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='product_Name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
