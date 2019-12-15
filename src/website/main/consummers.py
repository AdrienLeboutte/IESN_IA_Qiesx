from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
from . import models
logger = logging.getLogger(__name__)

class GameConsummer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("A game consummer was created and connected")
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_id = 'game_%s' % self.game_id
        self.user = self.scope["user"]
        logger.info(self.scope["user"])
        logger.info("Game : " + self.game_id + " - User : " + str(self.user.id))

        await self.channel_layer.group_add(
            self.game_group_id,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_group_id,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info("Messaged received from a websocket")
        text_data_json = json.loads(text_data)
        direction = text_data_json["direction"]
        logger.info(direction)
        
        game = models.Game.objects.get(id=self.game_id)
        game.send_direction(direction, self.user)
        player_positions = game.get_player_position()
        board = game.get_board()
        logger.info("Board is : %s" % board)
        await self.channel_layer.group_send(
            self.game_group_id, 
            {
                'type':'game.update',
                'board':board,
                'player_positions': player_positions
            }
        )
        

    async def game_update(self, event):
        logger.info("A game update was sent")
        board = event['board']
        player_positions = event['player_positions']

        await self.send(text_data=json.dumps({
            'board':board,
            'player_positions':player_positions
        }))

    