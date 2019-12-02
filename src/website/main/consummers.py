from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsummer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_id = 'game_%s' % self.game_id
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.game_group_id,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.game_group_id,
            self.channel_name
        )

    async def recieve(self, text_data):
        text_data_json = json.loads(text_data)
        direction = text_data_json["direction"]

        game = models.Game.objects.get(id=self.game_id)
        game.send_direction(direction, self.user)
        board = game.board

        await self.channel_layer.send(
            self.game_group_id,
            {
                'type':'game_update',
                'board':board
            }
        )

    async def game_update(self, event):
        board = event['board']

        await self.send(text_data=json.dumps({
            'board':board
        }))

    