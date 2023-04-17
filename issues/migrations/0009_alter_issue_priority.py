# Generated by Django 3.2.13 on 2023-04-17 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0008_alter_issue_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[(3, 'ddododod'), (2, 'Medium'), (1, 'Low')], default=1, max_length=8),
        ),
    ]
