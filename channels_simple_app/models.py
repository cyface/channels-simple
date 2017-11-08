"""Django Models"""
import logging

from channels.binding.websockets import WebsocketBinding
from django.db import models

LOGGER = logging.getLogger("channels_simple_app")


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


class IntegerValueBinding(WebsocketBinding):
    model = IntegerValue
    stream = "intval"
    fields = ["name", "value"]

    @classmethod
    def group_names(cls, instance):
        LOGGER.debug("IntegerValueBinding Group Names")
        return ["intval-updates"]

    def has_permission(self, user, action, pk):
        return True
