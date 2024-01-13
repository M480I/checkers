from game import Game


game = Game(
    clean_terminal=True,
    wait_for=.3,
    up_depth=8,
    down_depth=8,
    first_player="up"
)

game.start_game()
