class Game:

    def __init__(self, size_x, size_y):
        self._size_x = size_x
        self._size_y = size_y
        self._init_board()
        self._player_turn = 0
        self._game_state = "going"

    @property
    def size_x(self):
        return self._size_x
    
    @property
    def size_y(self):
        return self._size_y

    def _init_board(self):
        self._board = {}
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                self._board[(x,y)] = 0

    def get_case(self, xy):
        return self._board.get(xy, -1)

    def update_case(self, xy, id):
        self._board[xy] = id

    def print_board(self):
        for y in range (0, self.size_y):
            for x in range(0, self.size_x):
                print(self.get_case((x, y)), end=" . ")
            print("\n")
            
        