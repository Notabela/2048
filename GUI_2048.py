import pygame

#Height and width of tiles, DO NOT MODIFY
HEIGHT = 100
WIDTH = 100

#Begining Height and Width of tile
HEIGHT_BEG = 5
WIDTH_BEG = 5

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

#COLORS, DO NOT MODIFY
WHITE = (255, 255, 255)
GRAY = (40, 37, 34)
BLACK = (60, 58, 50)

#background color
BACKG_GRAY = (187, 173, 160)

#color of boxes in background
BOX_GRAY = (201, 186, 173)

#tiles color
COLOR_2 = (236, 225, 216)
COLOR_4 = (237, 224, 200)
COLOR_8 = (242, 177, 121)
COLOR_16 = (245, 149, 99)
COLOR_32 = (246, 124, 95)
COLOR_64 = (246, 94, 59)
COLOR_128 = (237, 207, 114)
COLOR_256 = (237, 204, 97)
COLOR_512 = (237, 200, 80)
COLOR_1024 = (237, 197, 63)
COLOR_2048 = (237, 194, 46)

"""
2048 GUI Game Class
"""


class GUITwentyFortyEight:
    #gameclock
    _clock = pygame.time.Clock()

    #tile color and font sizes
    _font_size_dict = {1: 100, 2: 90, 3: 75, 4: 50, 5: 40, 6: 35}

    _tile_color_dict = {2: COLOR_2, 4: COLOR_4, 8: COLOR_8, 16: COLOR_16, 32: COLOR_32, 64: COLOR_64, 128: COLOR_128,
                        256: COLOR_256, 512: COLOR_512, 1024: COLOR_1024, 2048: COLOR_2048}

    def __init__(self, game_class, x_dimension, y_dimension):

        #set game dimensions and window dimensions
        self._GAME_X = x_dimension
        self._GAME_Y = y_dimension
        self._GAME_HEIGHT = (x_dimension + 1) * 10 + x_dimension * WIDTH
        self._GAME_WIDTH = (y_dimension + 1) * 10 + y_dimension * HEIGHT

        #instance of 2048
        self._game_instance = game_class(x_dimension, y_dimension)

        #saved_game_instance
        self.game_class = game_class

        #init pygame
        pygame.init()

        #dynamic font for new tiles
        self.dynamic_font_size = 0

        #game screen
        self.screen = pygame.display.set_mode((self._GAME_WIDTH, self._GAME_HEIGHT))

        #game font
        self.font = pygame.font.Font(None, 100)

        #done Boolean
        self.done = False

        #indexes
        self.indexes, self.group_indexes = self.create_indexes()

    def create_indexes(self):
        """
        builds up all the indexes using x and y dimension of game
        :return: built indexes and grouped indexes
        """

        #Find the indexes of all boxes
        box_index = []
        for i in range(0, self._GAME_X):
            for j in range(0, self._GAME_Y):
                y_cor = i * WIDTH + (i + 1) * 10
                x_cor = j * HEIGHT + (j + 1) * 10
                box_index.append((x_cor, y_cor))

        #Group the indexes into a 2d list
        grouped_indexes = [[]]
        index = 0
        for _ in range(self._GAME_X):
            temp_list = []
            for _ in range(self._GAME_Y):
                temp_list.append(box_index[index])
                index += 1
            grouped_indexes.append(temp_list)

        grouped_indexes.remove([])

        return box_index, grouped_indexes

    def draw_background(self):
        """
        Fills background with gray color
        :return: None
        """
        self.screen.fill(BACKG_GRAY)

    def prepare_tiles(self):
        """
        Takes the gameinstance of the a TwentyFortyEight game class and packs tiles to be drawn
        :return:  array of tiles to be drawn
        """
        #reset vars
        rects_arr = [dict()]
        self.dynamic_font_size = 0

        grid = self._game_instance.grid

        for i, row in enumerate(grid):
            for j, col in enumerate(row):

                #array containing the boxes to draw
                draw_info = {}

                #if tile is not an empty tile
                if grid[i][j] != 0:
                    global font
                    #the value of the tile 2,4,8 etc
                    int_value = grid[i][j]
                    str_value = str(int_value)

                    #text_len = len(value)
                    font_size = self._font_size_dict.get(len(str_value), 20)
                    font = pygame.font.Font(None, font_size)

                    #map tile from TwentyFortyEight class to tile in GUI class
                    tile_index = self.group_indexes[i][j]

                    #format text_y and text_x so they're drawn exactly in the middle of the tile
                    text_width, text_height = font.size(str_value)
                    text_y = HEIGHT / 2 + tile_index[1] - text_height / 2
                    text_x = WIDTH / 2 + tile_index[0] - text_width / 2

                    #only draw tile if index is within our game board - here for extra security(should always be true)
                    if (0 <= i < self._GAME_X) and (0 <= j < self._GAME_Y):

                        text_color = GRAY if int_value <= 4 else WHITE
                        tile_color = self._tile_color_dict.get(int_value, BLACK)

                        label = font.render(str_value, True, text_color)

                        #if this tile is a new tile added to game, mark it as an animate tile_color
                        #set its width, height to zero so it can be animated to its full size
                        if (i, j) in self._game_instance.new_tiles:
                            new_width = 0
                            new_height = 0
                            new_xcor = WIDTH / 2 + tile_index[0]
                            new_ycor = HEIGHT / 2 + tile_index[1]

                            box_rect = pygame.Rect(new_xcor, new_ycor, new_width, new_height)

                            #pack tiles up nicely for drawing
                            draw_info = {"rect": [box_rect, tile_color, (tile_index[0], tile_index[1])],
                                         "label": [label, (text_x, text_y), str_value],
                                         "animation": ["transform", None]}
                        else:
                            box_rect = pygame.Rect(tile_index[0], tile_index[1], WIDTH, HEIGHT)

                            #pack tiles up nicely for drawing
                            draw_info = {"rect": [box_rect, tile_color, (tile_index[0], tile_index[1])],
                                         "label": [label, (text_x, text_y), str_value],
                                         "animation": ["translate", (None, None)]}

                        rects_arr.append(draw_info)

                else:
                    tile_index = self.group_indexes[i][j]
                    box_rect = pygame.Rect(tile_index[0], tile_index[1], WIDTH, HEIGHT)

                    #pack empty files up nicely for drawing
                    draw_info = {"rect": [box_rect, BOX_GRAY, (tile_index[0], tile_index[1])],
                                 "label": [None, None, None],
                                 "animation": ["None", ()], "identity": None}

                    #add onto the tiles to be drawn
                    rects_arr.append(draw_info)

        #reset the array that keeps track of new tiles added to the board
        self._game_instance.new_tiles = []

        #first element of rects_arr is always an empty dict, its removed here
        rects_arr.remove({})
        return rects_arr

    def draw_tiles(self, rects_arr):
        """
        Takes array of tiles and draw them as needed, includes some animations
        :return: None
        """
        for index, draw_info in enumerate(rects_arr):

            #parse arr_dict and pick out values
            box_rect = draw_info["rect"][0]
            color = draw_info["rect"][1]
            rect_cor = draw_info["rect"][2]
            label = draw_info["label"][0]
            label_cor = draw_info["label"][1]
            label_value = draw_info["label"][2]
            anim_type = draw_info["animation"][0]
            anim_cor = draw_info["animation"][1] if anim_type == "translate" else None

            pygame.draw.rect(self.screen, color, box_rect)

            if anim_type == "transform":
                width, height = box_rect.size

                #scale animation
                if width < 100:
                    box_rect.inflate_ip(10, 10)

                    if label is not None:
                        self.dynamic_font_size += 10

                        #Font size shouldn't exceed 100
                        self.dynamic_font_size %= 101

                        new_font = pygame.font.Font(None, self.dynamic_font_size)

                        new_label = new_font.render(label_value, True, GRAY)

                        text_width, text_height = new_font.size(label_value)

                        new_text_y = HEIGHT / 2 + rect_cor[1] - text_height / 2
                        new_text_x = WIDTH / 2 + rect_cor[0] - text_width / 2

                        self.screen.blit(new_label, (new_text_x, new_text_y))

                else:
                    if label is not None:
                        self.screen.blit(label, label_cor)

            #no other animations are implemented for tiles
            else:
                if label is not None:
                    self.screen.blit(label, label_cor)


    def mainloop(self):
        """
        Game's Mainloop
        :return: None
        """
        #prepare tiles
        rects_arr = self.prepare_tiles()

        while not self.done:
            #get quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                #Get key press events
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self._game_instance.move(UP)
                    elif event.key == pygame.K_DOWN:
                        self._game_instance.move(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self._game_instance.move(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self._game_instance.move(RIGHT)

                    rects_arr = self.prepare_tiles()

            self.draw_background()
            self.draw_tiles(rects_arr)

            pygame.display.flip()
            self._clock.tick(60)
