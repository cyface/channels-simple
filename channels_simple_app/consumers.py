import logging

from channels.generic.websockets import WebsocketConsumer, WebsocketDemultiplexer, JsonWebsocketConsumer

from django.db import models
from channels.binding.websockets import WebsocketBinding

from channels_simple_app.models import IntegerValue

LOGGER = logging.getLogger("channels_simple_app")


class MyConsumer(WebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    # Set to True if you want it, else leave it out
    #    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        LOGGER.debug("GROUPS: {}".format(kwargs.get('id')))
        return [kwargs.get('id')]

    # def connect(self, message, **kwargs):
    #     """
    #     Perform things on connection start
    #     """
    #     # Accept the connection; this is done by default if you don't override
    #     # the connect function.
    #     self.message.reply_channel.send({"accept": True})
    #     LOGGER.debug("CONNECT")

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # Simple echo
        LOGGER.debug("DEBUG TEXT:{}".format(text))
        self.send(text=text + "reply", bytes=bytes)

        # def disconnect(self, message, **kwargs):
        #     """
        #     Perform things on connection close
        #     """
        #     pass


class MyJsonConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    # Set to True if you want it, else leave it out
    #    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        LOGGER.debug("JGROUPS: {}".format(kwargs.get('id')))
        return [kwargs.get('id')]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        # Accept the connection; this is done by default if you don't override
        # the connect function.
        self.message.reply_channel.send({"accept": True})
        LOGGER.debug("JCONNECT")

    def receive(self, text=None, **kwargs):
        """
        Called when a message is received with text filled out.
        """
        # Simple echo
        LOGGER.debug("JDEBUG TEXT:{}".format(text))
        self.send({'text': text.get('text') + "reply"})

        # def disconnect(self, message, **kwargs):
        #     """
        #     Perform things on connection close
        #     """
        #     pass


class MyJsonMultiplexConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    # Set to True if you want it, else leave it out
    #    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        LOGGER.debug("MGROUPS: {}".format(kwargs.get('id')))
        return [kwargs.get('id')]

    def connect(self, message, **kwargs):
        LOGGER.debug("Multiplex Connect: {}")
        super(JsonWebsocketConsumer, self).connect(message=message, **kwargs)

    # def disconnect(self, message, **kwargs):
    #     multiplexer = kwargs.get('multiplexer')
    #     print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, **kwargs):
        multiplexer = kwargs.get('multiplexer')
        LOGGER.debug("Multiplex Receive: {}".format(content))
        # Simple echo
        multiplexer.send({"original_message": content})


class MyOtherJsonMultiplexConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    # Set to True if you want it, else leave it out
    #    strict_ordering = False

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        LOGGER.debug("MOGROUPS: {}".format(kwargs.get('id')))
        return [kwargs.get('id')]

    def connect(self, message, **kwargs):
        LOGGER.debug("MO Multiplex Connect")
        super(JsonWebsocketConsumer, self).connect(message=message, **kwargs)

    # def disconnect(self, message, **kwargs):
    #     multiplexer = kwargs.get('multiplexer')
    #     print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, **kwargs):
        multiplexer = kwargs.get('multiplexer')
        LOGGER.debug("Multiplex Receive: {}".format(content))
        # Simple echo
        multiplexer.send({"original_message": content})


class MyDemultiplexer(WebsocketDemultiplexer):
    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "echo": MyJsonMultiplexConsumer,
        "other": MyOtherJsonMultiplexConsumer,
    }


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


class IntegerValueDemultiplexer(WebsocketDemultiplexer):

    consumers = {
        "intval": IntegerValueBinding.consumer,
    }

    def connection_groups(self):
        return ["intval-updates"]