import sys
import pygame as pg
import Solver

pg.init()
screen_size = 1200, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)
grid = Solver.generate()
pg.display.set_caption('Sudoku - Piotr Grygoruk')


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


def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    draw_background()
    draw_numbers()
    pg.display.flip()


while 1:
    game_loop()
