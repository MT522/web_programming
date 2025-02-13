# Generated by Django 5.1.1 on 2024-10-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0002_judge_contestant_score_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='content',
            field=models.FileField(null=True, upload_to='content'),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='exceeded_time',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='resume',
            field=models.FileField(null=True, upload_to='resumes'),
        ),
    ]
