# Generated by Django 5.0 on 2023-12-06 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eventi', '0005_alter_evento_stripe_price_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participante1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_participant1', to=settings.AUTH_USER_MODEL)),
                ('participante2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_participant2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eventi.evento')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatroom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
