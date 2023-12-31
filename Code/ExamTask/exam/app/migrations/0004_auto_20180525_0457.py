# Generated by Django 2.0.5 on 2018-05-25 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_question_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='Course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Course'),
        ),
        migrations.AlterField(
            model_name='question',
            name='Difficulty',
            field=models.CharField(choices=[('Simple', 'Simple'), ('Difficult', 'Difficult')], max_length=20, verbose_name='Difficulty'),
        ),
        migrations.AlterField(
            model_name='question',
            name='Objective',
            field=models.CharField(choices=[('Reminding', 'Reminding'), ('Understanding', 'Understanding'), ('Creativity', 'Creativity')], max_length=20, verbose_name='Objective'),
        ),
    ]
