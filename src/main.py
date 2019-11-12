from game_logic.game import Game
from game_logic.game import Player

BOARD_SIZE_X = 8
BOARD_SIZE_Y = 8


players_g1 = [Player("1",0,0, False, False), Player("2",BOARD_SIZE_X - 1,BOARD_SIZE_Y - 1, False, False)]
game = Game(BOARD_SIZE_X,BOARD_SIZE_Y, players_g1)
game.start_game()
turn = 0
players = game.players
game.print_board()

state = game.state
while(game.game_state != 2):
    players = game.players
    n_state, reward = game.player_turn()

    if(turn != 0):
        s, sp, r = players[(turn + 1)%2].get_transition(-1)
        players[(turn + 1)%2].update_transition((s, state, reward * -1), -1)

    players[turn%2].add_transition((state, None, reward))

    print()
    game.print_board()
    turn += 1
    state = n_state

print(turn)
print(game._case_left)

print(players[0].get_transition(-1))
print(players[1].get_transition(-1))
