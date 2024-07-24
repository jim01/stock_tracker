from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Security
from channels.db import database_sync_to_async

"""
Websocket API for sending Stock Updates
"""

class WatchListConsumer(AsyncWebsocketConsumer):

    # accepts new websock connection
    # subscribes to updates from user's stocks
    # sends list of current stock prices
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        print("Connect from user " + user_id)

        # get user securities and send list
        tickers = await self.get_user_security_list(user_id)

        await self.accept()

        for ticker in tickers:
            # add them to the groups
            print("ticker_%s" % ticker)
            await self.channel_layer.group_add(
                "ticker_%s" % ticker,
                self.channel_name
            )

        await self.send(text_data=json.dumps(tickers))

    # Removes / Adds individual stocks from group updates
    async def receive(self, *, text_data):
        print("WatchList recieved: %s" % text_data)
        data = json.loads(text_data)
        if data["command"] == "sub":
            print("watching: %s " % data['ticker'])
            await self.channel_layer.group_add("ticker_%s" % data["ticker"], self.channel_name)

        if data["command"] == "unsub":
            print("remove from watch: %s " % data['ticker'])
            await self.channel_layer.group_discard("ticker_%s" % data["ticker"], self.channel_name)

    async def disconnect(self, close_code):
        print("WatchList disconnect")
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        """

    # pushes price update to user when stocks update
    async def send_ticker_update(self, event):
        print("WatchList sending update: %s" % event)
        await self.send(text_data=event['message'])

    @database_sync_to_async
    def get_user_security_list(self, user_id):
        map = {}
        results = Security.objects.filter(users=user_id)
        for item in results:
            map[item.ticker] = str(item.last_price)
        return map
