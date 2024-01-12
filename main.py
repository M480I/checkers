from game import Game


game = Game(
    clean_terminal=True,
    wait_for=.5,
    up_depth=1,
    down_depth=6,
    first_player="up"
)

game.start_game()
