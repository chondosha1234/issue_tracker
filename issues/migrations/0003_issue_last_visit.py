# Generated by Django 3.2.13 on 2023-03-23 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_alter_issue_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='last_visit',
            field=models.DateField(auto_now=True),
        ),
    ]
