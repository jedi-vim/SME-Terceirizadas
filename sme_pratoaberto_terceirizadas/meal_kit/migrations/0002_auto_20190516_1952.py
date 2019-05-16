# Generated by Django 2.0.13 on 2019-05-16 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meal_kit', '0001_initial'),
        ('school', '0001_initial'),
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermealkit',
            name='schools',
            field=models.ManyToManyField(to='school.School'),
        ),
        migrations.AddField(
            model_name='mealkit',
            name='meals',
            field=models.ManyToManyField(to='food.Meal'),
        ),
    ]
