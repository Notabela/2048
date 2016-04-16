from Logic_2048 import TwentyFortyEight
from GUI_2048 import GUITwentyFortyEight

board_width = int(input("Enter board width: "))
board_height = int(input("Enter board height: "))

game = GUITwentyFortyEight(TwentyFortyEight, board_height, board_width)
game.mainloop()
