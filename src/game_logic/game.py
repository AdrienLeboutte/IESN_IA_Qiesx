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

        return True

    def start_game(self):
        self.players = Player(1, 0, 0), Player(2, 7, 7)
        if self.validate((0,0), self.players[0]) and self.validate((self.size_x - 1,self.size_y - 1), self.players[1]):
            self.players[0].xy = (0,0)
            self.players[1].xy = (self.size_x - 1, self.size_y - 1)
        else:
            return -1
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