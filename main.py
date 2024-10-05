import pygame as py
from random import randint, choice
from Board import Board

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

app = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = py.time.Clock()


size = 60
rows = SCREEN_WIDTH // size
cols = SCREEN_HEIGHT // size
# cols = 5

board = Board(rows, cols, size)

generate = False
pause = False
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                exit()
            if event.key == py.K_SPACE:
                pause = True if not pause else False
            if event.key == py.K_n:
                board.next_step()
            if event.key == py.K_r:
                board.reset()
                generate = False
            if event.key == py.K_g:
                generate = True if not generate else False

    if pause:
        continue

    app.fill(120)
    clock.tick(60)

    if generate:
        board.generate()

    board.draw(app)

    py.display.flip()
