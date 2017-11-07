from channels.routing import route_class

from channels_simple_app.consumers import MyConsumer, MyJsonConsumer, MyDemultiplexer, IntegerValueDemultiplexer

channel_routing = [
    route_class(MyConsumer, path=r"^/game/(?P<id>\d+)/"),
    route_class(MyJsonConsumer, path=r"^/gamej/(?P<id>\d+)/"),
    route_class(MyDemultiplexer, path=r"^/gamem/(?P<id>\d+)/"),
    route_class(IntegerValueDemultiplexer, path="^/integer/"),
]
