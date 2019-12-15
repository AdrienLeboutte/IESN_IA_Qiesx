from game_logic.game import Game
from game_logic.game import Player
from game_logic.AI import IA
import pickle
import os


BOARD_SIZE_X = 4
BOARD_SIZE_Y = 4


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
        if not isinstance(players[game.turn], IA):
            game.print_board()
            action = players[game.turn].play()
        else:
            action = players[game.turn].play(game)
        players = game.players
        n_state, reward = game.player_turn(action)

        if train:

            if(turn != 0): 
                if isinstance(players[(game.turn + 1)%2], IA):
                    s, sp, r = players[(game.turn + 1)%2].get_transition()
                    players[(game.turn + 1)%2].update_transition((s, n_state, reward*-1))


            if isinstance(players[game.turn], IA):
                players[game.turn].add_transition((state, None, reward))

    
        """
        game.print_board()
        print(reward)
        print("\n")
        if turn != 0 and (turn + 1)%2 == 0:
            print(players[0]._history[-1])
            print(players[1]._history[-1])
        print("\n")
        """

        turn += 1
        state = n_state

    if isinstance(players[turn%2], IA):
        players[turn%2].train()
    if isinstance(players[(turn + 1 )%2], IA):
        players[(turn + 1)%2].train()

def training(ai1_v = {}, ai2_v = {}, n = 10000):
    ai1 = IA("1", 0,0)
    ai2 = IA("2",BOARD_SIZE_X - 1,BOARD_SIZE_Y - 1)
    ai1.V = ai1_v
    ai2.V = ai2_v
    players_g1 = [ai1, ai2]
    game = Game(BOARD_SIZE_X,BOARD_SIZE_Y, players_g1)
    for i in range(n):
        if i % 1000 == 0:
            print(i)

        if(i % 10 == 0):
            players_g1[0]._eps = max(players_g1[0]._eps * 0.996, 0.05)
            players_g1[1]._eps = max(players_g1[1]._eps * 0.996, 0.05)
        
        play_game(game)
    
    return ai1.V

def play_human(ai_v = {}):   
    ai1 = IA("1", 0,0)
    ai1.V = ai_v
    p1 = Player("2", BOARD_SIZE_X - 1,BOARD_SIZE_Y - 1)
    players = [ai1, p1]
    game = Game(BOARD_SIZE_X,BOARD_SIZE_Y, players)
    while True:
        play_game(game, train=False)

if __name__ == "__main__":
    if os.path.exists("ai_v.dat"):
        ai_v = pickle.load(open("ai_v.dat", "rb"))
        training = input("train ? (y/n)") == 'y'
        if training:
            training(ai1_v = ai_v)
        else:
            play_human(ai_v = ai_v)
    else:
        ai = training(n = 5000)
        pickle.dump(ai, open("ai_v.dat", "wb"))
        play_human(ai)

