# Generated by Django 3.2.13 on 2023-04-17 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0011_alter_issue_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.IntegerField(choices=[(3, 'High'), (2, 'Medium'), (1, 'Low')], default='Low'),
        ),
    ]
