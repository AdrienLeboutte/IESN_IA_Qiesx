from game_logic.game import Game
from game_logic.player import Player

game = Game(8,8)
game.print_board()
player1 = Player(game, 1)
player2 = Player(game, 2)

while 1:
    print("-----------------------------")
    game.print_board()
    player1.move(input("Player 1 - input : "))
    game.print_board()
    player2.move(input("Player 2 - input : "))
    
