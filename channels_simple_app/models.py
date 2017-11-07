"""Django Models"""
from channels.binding.websockets import WebsocketBinding
from django.db import models


class Card(models.Model):
    """Card for cardgame"""

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['name']
        verbose_name_plural = "cards"

    def __str__(self):
        return str(self.name)


class ChatMessage(models.Model):
    """Chat Message"""

    message = models.CharField(max_length=255)
    room = models.CharField(max_length=255, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['message']
        verbose_name_plural = "chat messages"

    def __str__(self):
        return str(self.room + self.message)


class IntegerValue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(default=0)
