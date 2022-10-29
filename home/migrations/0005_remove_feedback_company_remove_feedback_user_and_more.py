# Generated by Django 4.1.2 on 2022-10-29 03:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_companyprofile_contact_num_companyprofile_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='company',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='user',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.FileField(upload_to='uploads/images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('reciever', models.ManyToManyField(related_name='notification_reciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ManyToManyField(related_name='notification_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='company',
            field=models.ManyToManyField(related_name='feedback_company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ManyToManyField(related_name='feedback_user', to=settings.AUTH_USER_MODEL),
        ),
    ]