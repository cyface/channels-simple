from channels.test import ChannelTestCase, WSClient, Client


class MyTests(ChannelTestCase):
    def test_websockets_consumer_handlers(self):
        #  Create a channels test client
        client = Client()

        #  Send a websocket.connect message, passing in the path so it maps to the right consumer via the routing in routing.py
        #  Consume portion maps that message to a consumer and runs and returns an instance of the consumer
        connect_consumer = client.send_and_consume('websocket.connect', {'path': '/game/123/'})
        connect_reply = client.receive()
        self.assertEqual(connect_reply, {'accept': True})  # websocket.connect should return acceptance of connection

        receive_consumer = client.send_and_consume('websocket.receive', {'path': '/game/123/', 'text': 'text'})
        connect_reply = client.receive()  # receive() grabs the content of the next message off of the client's reply_channel
        self.assertEqual(connect_reply, {'text': 'textreply'})

        receive_consumer.group_send('123', text='grouptext')  # This sends a message out to a group - shortcut off of the Websocket Consumer
        group_reply = client.receive()
        self.assertEqual(group_reply, {'text': 'grouptext'})

        disconnect_consumer = client.send_and_consume('websocket.disconnect', {'path': '/game/123/'})

    def test_json_websockets_consumer_handlers(self):
        client = WSClient()

        try:
            client.send_and_consume('websocket.connect', path='/gamej/321/')
        except AssertionError:  # WS Client automatically checks that connection is accepted
            self.fail("Connection Rejected!")

        receive_consumer = client.send_and_consume('websocket.receive', path='/gamej/321/', text={'text': 'text'})  # Text arg is JSON as if it came from browser
        connect_reply = client.receive()  # receive() grabs the content of the next message off of the client's reply_channel
        self.assertEqual(connect_reply, {'text': 'textreply'})

        group_content = {'key1': 'value', 'key2': 2}
        receive_consumer.group_send('321', content=group_content)
        group_reply = client.receive()
        self.assertEqual(group_reply, group_content)

        disconnect_consumer = client.send_and_consume('websocket.disconnect', path='/gamej/321/')
