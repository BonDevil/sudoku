import sys
import pygame as pg
import Solver
from Button import Button

# display window
pg.init()
pg.display.set_caption('Sudoku - Piotr Grygoruk')

screen_size = 1200, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)

# start grid from Solver class
grid = Solver.generate()

# load button images
undo_img = pg.image.load('images/undo.png').convert_alpha()
hint_img = pg.image.load('images/hint.png').convert_alpha()
erase_img = pg.image.load('images/erase.png').convert_alpha()
one_img = pg.image.load('images/1.png').convert_alpha()
two_img = pg.image.load('images/2.png').convert_alpha()
three_img = pg.image.load('images/3.png').convert_alpha()


def draw_background():
    screen.fill(pg.Color(204, 204, 204))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        line_width = 3 if i % 3 > 0 else 10
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
                n_text = font.render(str(output), True, pg.Color('black'))
                screen.blit(n_text, pg.Vector2(column * 80 + offset + 5, row * 80 + offset - 2))
            column += 1
        row += 1


def draw_menu():
    undo_button = Button(500, 200, undo_img, 1)
    undo_button.draw(screen)


def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    draw_background()
    draw_numbers()
    draw_menu()
    pg.display.flip()

while 1:
    game_loop()
