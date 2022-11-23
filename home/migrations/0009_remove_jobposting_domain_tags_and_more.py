# Generated by Django 4.1.2 on 2022-11-23 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_feedback_comments_alter_feedback_ratingfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobposting',
            name='domain_tags',
        ),
        migrations.RemoveField(
            model_name='jobposting',
            name='requirement_tags',
        ),
        migrations.AddField(
            model_name='jobposting',
            name='domain_skills',
            field=models.ManyToManyField(related_name='jobposting_domain_skills', to='home.skill'),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='requirement_skills',
            field=models.ManyToManyField(related_name='jobposting_requirement_skills', to='home.skill'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='ratingfield',
            field=models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Resume', 'Resume'), ('Coursera Certificates', 'Coursera Certificates'), ('Profile', 'Profile'), ('Skills', 'Skills')], default='profile', max_length=30),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
