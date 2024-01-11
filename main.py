from game import  Game


game = Game(clean_terminal=True, wait_for=.5, up_depth=5, down_depth=8)

game.start_game()
