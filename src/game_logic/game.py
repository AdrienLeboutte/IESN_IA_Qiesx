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

    def update_case(self, xy, id):
        self._board[xy] = id

    def validate(self, xy, id):
        case_value = self.get_case(xy)
        if case_value != id and case_value != 0:
            return False
        if case_value == 0:
            self.update_case(xy, id)
        return True

    def start_game(self):
        if self.validate((0,0), 1) and self.validate((7,7), 2):
            self.players = Player(1, 0, 0), Player(2, 7, 7)
        else:
            return -1
        self.game_state = 1
        while self.game_state == 1:
            #Player 1's turn
            p1_xy = self.players[0].move(input("Player 1's move : "))
            if self.validate(p1_xy, 1):
                self.players[0].xy = p1_xy
            #Player 2's turn
            p2_xy = self.players[1].move(input("Player 2's move : "))
            if self.validate(p2_xy, 2):
                self.players[1].xy = p2_xy
            self.print_board()

    def print_board(self):
        for y in range (0, self.size_y):
            for x in range(0, self.size_x):
                print(self.get_case((x, y)), end=" . ")
            print("\n")