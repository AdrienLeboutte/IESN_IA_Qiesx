from game_logic.game import Game
from game_logic.game import Player

BOARD_SIZE_X = 8
BOARD_SIZE_Y = 8


players = [Player("1",0,0, False, False), Player("2",BOARD_SIZE_X - 1,BOARD_SIZE_Y - 1, False, False)]
game = Game(BOARD_SIZE_X,BOARD_SIZE_Y, players)
game.start_game()
turn = 0
players = game.players
game.print_board()

while(game.game_state != 2):
    player = players[turn%2]
    game.player_turn(player)
    print()
    game.print_board()
    turn += 1

print(turn)
print(game._case_left)
