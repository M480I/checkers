from game import Game
from consts import LEVELS 


game = Game(
    clean_terminal=True,
    wait_for=0,
    up_depth=LEVELS["SMART"],
    down_depth=LEVELS["NORMAL"],
    first_player="down"
)

game.start_game()
