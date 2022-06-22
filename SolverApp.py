import sys
import pygame as pg
import Solver
from Button import Button
import asyncio

# init game window
pg.init()
pg.display.set_caption('Sudoku - Piotr Grygoruk')
screen_size = 1200, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)
picked_square = (-1, -1, False)     # global variable to store square to put number in
events = [(-1, -1, -1, -1)]         # events that happened row, column, event (1 - number added on grid, 2 - number erased - 3 hint put), optional value - if erased
initialized = False                 # is game initialized

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# load image
erase_img = pg.image.load('images/erase.png').convert_alpha()
clear_img = pg.image.load('images/clear.png').convert_alpha()
solve_img = pg.image.load('images/solve.png').convert_alpha()
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
clear_button = Button(800, 30, clear_img, 1)
solve_button = Button(800, 100, solve_img, 1)
erase_button = Button(930, 185, erase_img, 1)
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
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, i * 80 + 15), pg.Vector2(730, i * 80 + 15), line_width)
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
    clear_button.draw(screen)
    solve_button.draw(screen)

    erase_button.draw(screen)

    one_button.draw(screen)
    two_button.draw(screen)
    three_button.draw(screen)

    four_button.draw(screen)
    five_button.draw(screen)
    six_button.draw(screen)

    seven_button.draw(screen)
    eight_button.draw(screen)
    nine_button.draw(screen)


def draw_picked_square(row, column):
    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2(column * 80 + 15, row * 80 + 15),
                 pg.Vector2(column * 80 + 15, (row + 1) * 80 + 15), 5)
    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2((column + 1) * 80 + 15, row * 80 + 15),
                 pg.Vector2((column + 1) * 80 + 15, (row + 1) * 80 + 15), 5)
    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2(column * 80 + 15, row * 80 + 15),
                 pg.Vector2((column + 1) * 80 + 15, row * 80 + 15), 5)
    pg.draw.line(screen, pg.Color(120, 122, 204), pg.Vector2(column * 80 + 15, (row + 1) * 80 + 15),
                 pg.Vector2((column + 1) * 80 + 15, (row + 1) * 80 + 15), 5)


def draw_wrong():
    pg.draw.rect(screen, pg.Color("red"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        line_width = 3 if i % 3 > 0 else 7
        pg.draw.line(screen, pg.Color("red"), pg.Vector2(i * 80 + 15, 15), pg.Vector2(i * 80 + 15, 730),
                     line_width)
        pg.draw.line(screen, pg.Color("red"), pg.Vector2(15, i * 80 + 15), pg.Vector2(735, i * 80 + 15),
                     line_width)
        i += 1


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
                    draw_picked_square(row, column)

                    global picked_square
                    picked_square = row, column, True
            column += 1
        row += 1


def set_number(row, col, numb):
    # we can't change number from generated grid
    global grid
    grid[row][col] = numb
    draw_background()
    draw_picked_square(row, col)
    draw_numbers()


def action_after_picked(row, col, is_picked):
    drawn = True
    if one_button.draw(screen):
        set_number(row, col, 1)
    elif two_button.draw(screen):
        set_number(row, col, 2)
    elif three_button.draw(screen):
        set_number(row, col, 3)
    elif four_button.draw(screen):
        set_number(row, col, 4)
    elif five_button.draw(screen):
        set_number(row, col, 5)
    elif six_button.draw(screen):
        set_number(row, col, 6)
    elif seven_button.draw(screen):
        set_number(row, col, 7)
    elif eight_button.draw(screen):
        set_number(row, col, 8)
    elif nine_button.draw(screen):
        set_number(row, col, 9)
    else:
        drawn = False
    if drawn:  # if user put number on grid and it didn't exist, it's stored in drawn_numbers
        if not (row, col, 1, -1) in events:
            events.append((row, col, 1, -1))

    if erase_button.draw(screen):
        events.append((row, col, 2, grid[row][col]))
        if (row, col, 1, -1) in events:
            events.remove((row, col, 1, -1))
        set_number(row, col, 0)  # setting number to 0 - it doesn't display = erased


def new():
    if clear_button.draw(screen):
        global grid
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        draw_background()
        draw_menu()
        draw_numbers()

def solve():
    if solve_button.draw(screen):
        if not Solver.solve(grid, 0, 0):
            draw_wrong()
        else:
            draw_background()
            draw_numbers()


def loop_one_step():
    pg.display.flip()
    new()
    pick_square()
    row, col, is_picked = picked_square

    if is_picked:
        action_after_picked(row, col, is_picked)

    solve()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()


async def game_loop():
    draw_background()
    draw_numbers()
    draw_menu()
    while True:
        loop_one_step()
        await asyncio.sleep(0)
