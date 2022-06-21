import sys
import pygame as pg
import Solver
import copy
from Button import Button


#init game window
pg.init()
pg.display.set_caption('Sudoku - Piotr Grygoruk')

screen_size = 1200, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)

# grid from Solver class
grid = Solver.generate()
basic_grid = copy.deepcopy(grid)

#load image
undo_img = pg.image.load('images/undo.png').convert_alpha()
hint_img = pg.image.load('images/hint.png').convert_alpha()
erase_img = pg.image.load('images/erase.png').convert_alpha()
newgame_img = pg.image.load('images/newgame.png').convert_alpha()
one_img = pg.image.load('images/1.png').convert_alpha()
two_img = pg.image.load('images/2.png').convert_alpha()
three_img = pg.image.load('images/3.png').convert_alpha()
four_img = pg.image.load('images/4.png').convert_alpha()
five_img = pg.image.load('images/5.png').convert_alpha()
six_img = pg.image.load('images/6.png').convert_alpha()
seven_img = pg.image.load('images/7.png').convert_alpha()
eight_img = pg.image.load('images/8.png').convert_alpha()
nine_img = pg.image.load('images/9.png').convert_alpha()

# initializing menu buttons
newgame_button = Button(800, 50, newgame_img, 1)

undo_button = Button(850, 150, undo_img, 1)
erase_button = Button(930, 150, erase_img, 1)
hint_button = Button(1010, 150, hint_img, 1)

one_button = Button(815, 300, one_img, 0.85)
two_button = Button(915, 300, two_img, 0.85)
three_button = Button(1015, 300, three_img, 0.85)

four_button = Button(815, 415, four_img, 0.85)
five_button = Button(915, 415, five_img, 0.85)
six_button = Button(1015, 415, six_img, 0.85)

seven_button = Button(815, 530, seven_img, 0.85)
eight_button = Button(915, 530, eight_img, 0.85)
nine_button = Button(1015, 530, nine_img, 0.85)


def draw_background():
    screen.fill(pg.Color(204, 204, 204))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        line_width = 3 if i % 3 > 0 else 7
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(i * 80 + 15, 15), pg.Vector2(i * 80 + 15, 730), line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, i * 80 + 15), pg.Vector2(735, i * 80 + 15), line_width)
        i += 1


def draw_numbers():
    row = 0
    offset = 35
    while row < 9:
        column = 0
        while column < 9:
            if grid[row][column] != 0:
                output = grid[row][column]
                n_text = font.render(str(output), True, pg.Color(0, 122, 204))
                screen.blit(n_text, pg.Vector2(column * 80 + offset + 5, row * 80 + offset - 2))
            column += 1
        row += 1


def draw_menu():
    # drawing menu on screen
    newgame_button.draw(screen)

    undo_button.draw(screen)
    erase_button.draw(screen)
    hint_button.draw(screen)

    one_button.draw(screen)
    two_button.draw(screen)
    three_button.draw(screen)

    four_button.draw(screen)
    five_button.draw(screen)
    six_button.draw(screen)

    seven_button.draw(screen)
    eight_button.draw(screen)
    nine_button.draw(screen)


picked_square = (-1, -1, False)


def pick_square():
    row = 0
    while row < 9:
        column = 0
        while column < 9:
            if pg.Rect(15 + column * 80, 15 + row * 80, 80, 80).collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] == 1:
                    draw_background()
                    draw_numbers()
                    draw_menu()

                    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2(column * 80 + 15, row*80 + 15), pg.Vector2(column * 80 + 15, (row+1) * 80 + 15), 5)
                    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2((column + 1) * 80 + 15, row*80 + 15), pg.Vector2((column + 1) * 80 + 15, (row+1) * 80 + 15), 5)
                    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2(column*80 + 15, row * 80 + 15), pg.Vector2((column+1) * 80 + 15, row * 80 + 15), 5)
                    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2(column*80 + 15, (row + 1) * 80 + 15), pg.Vector2((column+1) * 80 + 15, (row + 1) * 80 + 15), 5)

                    global picked_square
                    picked_square = row, column, True
            column += 1
        row += 1


def pick_number(row, col, numb):
    # we can't change number from generated grid
    if basic_grid[row][col] == 0:
        global grid
        grid[row][col] = numb
        draw_background()
        draw_numbers()


draw_background()
draw_numbers()
draw_menu()


def game_loop():
    pg.display.flip()
    pick_square()

    if newgame_button.draw(screen):
        global grid
        global basic_grid
        grid = copy.deepcopy(Solver.generate())
        basic_grid = copy.deepcopy(grid)
        draw_background()
        draw_menu()
        draw_numbers()

    if undo_button.draw(screen):
        print("undo clicked")

    if erase_button.draw(screen):
        print("erase clicked")

    if hint_button.draw(screen):
        print("hint clicked")

    row, col, is_picked = picked_square

    if is_picked:
        if one_button.draw(screen):
            pick_number(row, col, 1)
        if two_button.draw(screen):
            pick_number(row, col, 2)
        if three_button.draw(screen):
            pick_number(row, col, 3)
        if four_button.draw(screen):
            pick_number(row, col, 4)
        if five_button.draw(screen):
            pick_number(row, col, 5)
        if six_button.draw(screen):
            pick_number(row, col, 6)
        if seven_button.draw(screen):
            pick_number(row, col, 7)
        if eight_button.draw(screen):
            pick_number(row, col, 8)
        if nine_button.draw(screen):
            pick_number(row, col, 9)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()




while 1:
    game_loop()

