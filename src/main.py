from game_logic.game import Game

game = Game(8,8)
game.start_game()
turn = 0
players = game.players
game.print_board()

while(game.game_state != 2):
    player = players[turn%2]
    move = input("Player {} >>> ".format(player.id))
    game.player_turn(move, player)
    game.print_board()
    turn += 1
