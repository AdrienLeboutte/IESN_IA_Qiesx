from django.db import models
from django.contrib.auth.models import User
import uuid
import sys
sys.path.append("../")
from game_logic.game import Game as Logic_Game
from game_logic.player import Player
import logging
logger = logging.getLogger(__name__)

game_servers = {}

# Create your models here.


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.CharField(max_length=50, default="")
    size_x = models.IntegerField(default=8)
    size_y = models.IntegerField(default=8)
    game_state = models.IntegerField(default=0)
    player_1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_1")
    player_2 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_2")
    
    def start_game(self):
        if self.player_2 == None:
            return -1
        game_servers[self.id] = Logic_Game(self.size_x, self.size_y, [Player(str(1),0,0), Player(str(2),self.size_x-1, self.size_y-1)])
        game_servers[self.id].start_game()
        logger.info("A game was started - UUID : %s", self.id)
        self.board = game_servers[self.id].game_board
        self.game_state = 1
        self.save()
        return 0
    def send_direction(self, action):
        
        game_servers[self.id].player_turn(action)
        game_servers[self.id].print_board()
        self.board = game_servers[self.id].game_board
        self.save()
        logger.info("Direction were sent - UUID : %s", self.id) 

