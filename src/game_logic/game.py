from .player import Player
class Game:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self._init_board()

    def _init_board(self):
        '''
            Method used to initlalize the game board with 0, meaning no cases have been claimed
            0 = neutral
            1 = player one's
            2 = player two's
        '''
        self._board = {}
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                self._board[(x,y)] = 0

    
    def get_case(self, xy):
        #Return 0, 1 or 2 if in the limits of the game_board, -1 if out of bound
        return self._board.get(xy, -1)

    def update_case(self, xy, player):
        self._board[xy] = player.id

    def validate(self, xy, player):
        case_value = self.get_case(xy)
        if case_value != player.id and case_value != 0:
            return False
        if case_value == 0:
            self.update_case(xy, player)
        x,y = xy
        zone_right = set()
        zone_left = set()
        delta = (x - player.x, y - player.y)
        if(x == 0 or x == 7 or self.get_case((x + delta[0], y + delta[1])) == player.id):
            zone_right = self.get_zone((x, y - 1), player.id, set((x,y)))
            zone_left = self.get_zone((x, y + 1), player.id, set((x,y)))
        elif(y == 0 or y == 7 or self.get_case((x + delta[0], y + delta[1])) == player.id):
            zone_right = self.get_zone((x + 1, y), player.id, set((x,y)))
            zone_left = self.get_zone((x - 1, y), player.id, set((x,y)))
        if zone_left != -1:
            self.fill_zone(zone_left, player)
        if zone_right != -1:
            self.fill_zone(zone_right, player)
        return True

    def start_game(self):
        self.players = Player(1, 0, 0), Player(2, 7, 7)

        #I removed starting location validation, we can assume that we are not going to put the player on any comprise case
        self.update_case((0,0), self.players[0])
        self.update_case((self.size_x - 1, self.size_y - 1), self.players[1])
        self.players[0].xy = (0,0)
        self.players[1].xy = (self.size_x - 1, self.size_y - 1)
       
        self.game_state = 1
        while self.game_state == 1:
            #Player 1's turn
            self.player_turn(self.players[0])
            self.print_board()
            self.player_turn(self.players[1])
            self.print_board()
            

    def player_turn(self, player):
        p_xy = player.move(input("Player {}'s move : ".format(player.id)))
        if self.validate(xy=p_xy, player=player):
            player.xy = p_xy

    def print_board(self):
        for y in range (0, self.size_y):
            for x in range(0, self.size_x):
                case = self.get_case((x,y))
                if case == 0:
                    print(" □ ", end="")
                elif case == 1:
                    print(" ◙ ", end="")
                elif case == 2:
                    print(" ■ ", end="")
            print("\n")

    """
    Method that check if a zone is accessible by an other player
    Args :
        - xy : coord xy of the player
        - id : id of the player
    Return :
        - A list of cases that can be claimed by the player, -1 otherwise
    """
    def get_zone(self, xy, id, zone_commune):
        x_start, y_start = xy
        zone = set()
        for y in range(y_start - 1, y_start + 2):
            for x in range(x_start - 1, x_start + 2):
                if (x,y) not in zone_commune:
                    id_case = self.get_case((x,y))
                    if id_case != id and id_case != 0 and id_case != -1:
                        return -1
                    if id_case == 0:
                        zone.add((x,y))
                        zone_commune.add((x,y))

        for case in zone:
            zone_commune = self.get_zone(case, id, zone_commune)
            if zone_commune == -1 :
                return -1
        return zone_commune

    """
    Method that fill all coord from zone
    Args:
        - zone : list of tuples containing coord of the board that can be claimed by a player
        - player : The player who can claimed the case
    """
    def fill_zone(self, zone, player):
        for case in zone:
            self.update_case(case, player)