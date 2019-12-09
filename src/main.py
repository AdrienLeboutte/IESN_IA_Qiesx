from game_logic.game import Game
from game_logic.game import Player
from game_logic.AI import IA
import pickle

BOARD_SIZE_X = 4
BOARD_SIZE_Y = 4

players_g1 = [IA("1", 0,0), IA("2",BOARD_SIZE_X - 1,BOARD_SIZE_Y - 1)]
game = Game(BOARD_SIZE_X,BOARD_SIZE_Y, players_g1)


def play_game(game, train=True):
    """
    Function to make a game, to play and to train both of players if they are trainable
    """
    game.reset()
    game.start_game() #Place players on the board
    turn = 0
    players = game.players

    state = game.state
    while(game.game_state != 2):
        action = None
        if not isinstance(players[turn%2], IA):
            game.print_board()
            action = players[turn%2].play()
        else:
            action = players[turn%2].play(game)
        players = game.players
        n_state, reward = game.player_turn(action)

        if(turn != 0): 
            if isinstance(players[(turn + 1)%2], IA):
                s, sp, r = players[(turn + 1)%2].get_transition()
                players[(turn + 1)%2].update_transition((s, n_state, reward * -1))
        if isinstance(players[turn%2], IA):
            players[turn%2].add_transition((state, None, reward))

        #game.print_board()
        #print("\n")
        turn += 1
        state = n_state
    #print(players[turn%2]._history)
    if isinstance(players[turn%2], IA):
        players[turn%2].train()
    if isinstance(players[(turn + 1 )%2], IA):
        players[(turn + 1)%2].train()

for i in range(10000):
    if i % 1000 == 0:
        print(i)

    if(i % 10 == 0):
        players_g1[0]._eps = max(players_g1[0]._eps * 0.996, 0.05)
        players_g1[1]._eps = max(players_g1[1]._eps * 0.996, 0.05)
    play_game(game)
    
print(players_g1[0]._V)
