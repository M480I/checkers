from game import Game


game = Game(
    clean_terminal=False,
    wait_for=0,
    up_depth=1,
    down_depth=8,
    first_player="up"
)

game.start_game()
