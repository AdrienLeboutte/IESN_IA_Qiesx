"""
In order to use the game logic written on a seperate source we must import the module
It is stored in the constant "PATH_TO_GAME_LOGIC"
This obviously varies to where you have installed your archive
"""
PATH_TO_GAME_LOGIC = "H:\\GitHub\\mp_qix_iesn\\src\\"
#Importing essentials
from django.db import models
from django.contrib.auth.models import User
import uuid
import sys
#Importing game logic
sys.path.append(PATH_TO_GAME_LOGIC)
from game_logic.game import Game as Logic_Game
from game_logic.player import Player

#Setting up loggers
import logging
logger = logging.getLogger(__name__)

game_servers = {}

# Create your models here.


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.CharField(default="", max_length=2500)
    size_x = models.IntegerField(default=4)
    size_y = models.IntegerField(default=4)
    game_state = models.IntegerField(default=0)
    player_1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_1")
    player_2 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_2")
    
    def start_game(self):
        if self.player_2 == None:
            return -1
        """
        TODO:
        - Make sure ID is unique when adding to the DB
        - Reload the games that crashed when server is restarted
        """
        game_servers[self.id] = Logic_Game(self.size_x, self.size_y, [Player(str(1),0,0), Player(str(2),self.size_x-1, self.size_y-1)])
        game_servers[self.id].start_game()
        logger.info("A game was started - UUID : %s", self.id)
        self.board = game_servers[self.id].game_board
        self.game_state = "1"
        self.save()
        return 0
    def send_direction(self, action, user):
        if not (self.id in game_servers):
            return 5001
        player_turn = game_servers[self.id]._turn
        if (player_turn == 0 and user.id == self.player_1.id) or (player_turn == 1 and user.id == self.player_2.id):
            game_servers[self.id].player_turn(action)
            self.board = game_servers[self.id].game_board
            if self.game_state != self.get_status():
                self.game_state = self.get_status()
            self.save()
            logger.info("Direction were sent - UUID : %s", self.id)
            return 0

    def get_board(self):
        if not (self.id in game_servers):
            return 0;
        return game_servers[self.id].game_board

    def get_player_position(self):
        if not (self.id in game_servers):
            return ((0,0),(self.size_x - 1, self.size_y - 1))
        player_1, player_2 = game_servers[self.id].players
        return player_1.xy, player_2.xy
    def get_status(self):
        if not (self.id in game_servers):
            return str(0)
        else:
            return str(game_servers[self.id].game_state)

    def get_winner(self):
        if self.get_status() == "2":
            winner = str(game_servers[self.id].get_winner())
            logger.info("Models winner : %s" % winner )
            return winner


class GameIA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.CharField(default="", max_length=2500)
    size_x = models.IntegerField(default=4)
    size_y = models.IntegerField(default=4)
    game_state = models.IntegerField(default=0)
    player_1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="player_1")


