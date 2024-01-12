from game import Game


game = Game(
    clean_terminal=True,
    wait_for=0.5,
    up_depth=1,
    down_depth=8,
    first_player=None
)

game.start_game()
