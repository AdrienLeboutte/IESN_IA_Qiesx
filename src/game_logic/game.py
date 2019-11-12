import random
from .player import Player


class Game:

    def __init__(self, size_x, size_y, players):
        self._size_x = size_x
        self._size_y = size_y
        self._players = players
        self._board = ""
        self._case_left = size_x * size_y
        self._turn = 0 #id of the player who is currently playing
        self._game_state = 0 #0 if the game is not running, 1 if the game is running, 2 if the game is over

        self._init_board()

    '''Properties'''
    @property
    def game_state(self):
        return self._game_state

    @property
    def game_board(self):
        return self._board 

    @property
    def players(self):
        return self._players

    @property
    def state(self):
        return self._board 

    '''Methods'''
    def _init_board(self):
        '''
            Method used to initlalize the game board with 0, meaning no cases have been claimed
            0 = neutral
            1 = player one's
            2 = player two's
        '''
        self._board += "0" * (self._size_x * self._size_y)
    
    def get_case(self, xy):
        #Return 0, 1 or 2 if in the limits of the game_board, -1 if out of bound
        index = self.get_case_index(xy)
        if index != -1:
            return self._board[index]
        return -1

    def get_case_index(self, xy):
        x, y = xy
        if x >= 0 and x < self._size_x and y >= 0 and y < self._size_y:
            return x + y * self._size_y
        return -1

    def update_case(self, xy, player):
        changing_case = self.get_case_index(xy)
        self._board = self._board[:changing_case] + player.id + self._board[changing_case + 1:]
        player.case_claimed += 1
        self._case_left -= 1

    def validate(self, xy, player):
        case_value = self.get_case(xy)
        if case_value != player.id and case_value != "0":
            return False
        if case_value == "0":
            self.update_case(xy, player)
            self._zone_finding(xy, player)

        return True

    """
    Method That find a zone to fill if there is one
    Args :
        - xy : coord where the player want to go
        - player : the player who is curently playing
    """
    def _zone_finding(self, xy, player):
        x,y = xy
        zone_right = set()
        zone_left = set()
        delta = (x - player.x, y - player.y)

        if abs(delta[0]) == 1:
            #Border_close is a boolean indicating that there is a border close to the player
            border_close = any([True for row in range(-1,2) if self.get_case((x + delta[0], y + row)) == player.id or x == 0 or x == self._size_x - 1])
            if(border_close):
                zone_right = self._get_zone((x, y - 1), player.id, set())
                zone_left = self._get_zone((x, y + 1), player.id, set())
        elif abs(delta[1]) == 1:
            border_close = any([True for column in range(-1,2) if self.get_case((x + column, y + delta[1])) == player.id or y == 0 or y == self._size_y - 1])
            if(border_close):
                zone_right = self._get_zone((x + 1, y), player.id, set())
                zone_left = self._get_zone((x - 1, y), player.id, set())

        if zone_left != -1:
            self._fill_zone(zone_left, player)
        if zone_right != -1:
            self._fill_zone(zone_right, player)

    def start_game(self):
        self.update_case((0,0), self._players[0])
        self.update_case((self._size_x - 1, self._size_y - 1), self._players[1])
        self._game_state = 1

    def get_winner(self):
        if self._players[0].case_claimed > self._players[1].case_claimed:
            return self._players[0].id
        return self._players[1].id
        
    """
    Method that allow the player to make his move
    Args :
        - move : the direction in which the player want to go
        - player : the player who is requesting to move
    Return :
        0 if the game is not currently running (eg : game_over)
        1 if the players has finished playing
    """
    def player_turn(self):
        if self._game_state != 1:
            return 0

        player = self._players[self._turn]
        reward = 0
        p_xy = player.move()
        if self.validate(p_xy, player):
            player.xy = p_xy
        if self._case_left <= 0:
            self._game_state = 2
            id_winner = self.get_winner()
            reward = 1 if id_winner == self._turn else -1

        self._turn = (self._turn + 1)%2
        return (self._board, reward)

    def print_board(self):
        for y in range (0, self._size_y):
            for x in range(0, self._size_x):
                case = self.get_case((x,y))
                if case == "0":
                    print(" □ ", end="")
                elif case == "1":
                    print(" ◙ ", end="")
                elif case == "2":
                    print(" ■ ", end="")
            print("\n")

    """
    Method that check if a zone is accessible by an other player
    Args :
        - xy : coord where the player want to go
        - id : id of the player curently playing
    Return :
        - A list of cases that can be claimed by the player, -1 otherwise
    """
    def _get_zone(self, xy, id, commun_zone):
        #Check if it is necessary to check that direction in the first place
        id_case = self.get_case(xy)
        if id_case != "0":
            return -1
        
        #Core
        x, y = xy
        commun_zone.add(xy)
        zone = set()
        delta = -1
        for _ in range(0,2):
            # Y check
            if (x, y+delta) not in commun_zone:
                id_case = self.get_case((x,y + delta))
                if id_case != -1 and id_case != "0" and id_case != id:
                    return -1
                if id_case == "0":
                    commun_zone.add((x, y + delta))
                    zone.add((x, y + delta))
            # X check
            if (x + delta, y) not in commun_zone:
                id_case = self.get_case((x + delta,y))
                if id_case != -1 and id_case != "0" and id_case != id:
                    return -1
                if id_case == "0":
                    commun_zone.add((x + delta, y))
                    zone.add((x + delta, y))
            delta = -delta

        for case in zone:
            commun_zone = self._get_zone(case, id, commun_zone)
            if commun_zone == -1 :
                return -1
        return commun_zone

    """
    Method that fill all coords from zone
    Args:
        - zone : list of tuples containing coord of the board that can be claimed by a player
        - player : The player who can claimed the case
    """
    def _fill_zone(self, zone, player):
        for case in zone:
            self.update_case(case, player)


    def reset(self):
        self._board = ""
        self._case_left = self._size_x * self._size_y
        self._turn = 0 #id of the player who is currently playing
        self._game_state = 0 #0 if the game is not running, 1 if the game is running, 2 if the game is over