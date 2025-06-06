# Generated by Django 5.2.1 on 2025-05-22 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='URL изображения')),
                ('condition', models.CharField(choices=[('new', 'Новый'), ('used', 'Б/У')], max_length=10, verbose_name='Состояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='barter.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('accepted', 'Принята'), ('declined', 'Отклонена')], default='pending', max_length=10, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата предложения')),
                ('ad_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_proposals', to='barter.ad', verbose_name='Объявление получателя')),
                ('ad_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='barter.ad', verbose_name='Объявление отправителя')),
            ],
        ),
    ]
