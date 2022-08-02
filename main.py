from enum import Enum, auto
from functools import lru_cache
import os

import math
from pprint import pprint

import pygame
from pygame import Vector2
from pygame.locals import (
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

TILE_SIZE = 16
SCREEN_DIMS = Vector2(240, 160)
WINDOW_DIMS = SCREEN_DIMS * 4


def get_tile_area(i):
    # ATLAS_HEIGHT = 11
    ATLAS_WIDTH = 11
    y = math.floor(i / ATLAS_WIDTH)
    py = y * TILE_SIZE
    py_end = y + TILE_SIZE

    x = i % ATLAS_WIDTH
    px = x * TILE_SIZE
    px_end = px + TILE_SIZE

    return (px, py, px_end, py_end)


def main():
    pygame.init()

    screen = pygame.Surface(SCREEN_DIMS)
    window = pygame.display.set_mode(WINDOW_DIMS)

    tiles_im = pygame.image.load('./tiles.png')  # .convert_alpha()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
                running = False
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        mt = pygame.mouse.get_pos()
        m = (Vector2(mt[0], mt[1]).elementwise() /
             WINDOW_DIMS).elementwise() * SCREEN_DIMS
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(m.x-4, m.y-4, 8, 8))

        for y in range(8):
            for x in range(8):
                screen.blit(tiles_im, (x*TILE_SIZE, y *
                            TILE_SIZE), get_tile_area(2))

        blit = pygame.transform.scale(screen, window.get_size())
        window.blit(blit, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
