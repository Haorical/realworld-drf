# Generated by Django 4.0.6 on 2022-07-20 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('favorites', models.ManyToManyField(related_name='favorited_by', to='articles.article')),
                ('follows', models.ManyToManyField(related_name='followed_by', to='profiles.profile')),
            ],
        ),
    ]
