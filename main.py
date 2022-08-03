from enum import Enum, auto
from functools import lru_cache
import os

import math
from pprint import pprint
import random

import pygame
from pygame import Vector2
from pygame.locals import (
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

TILE_HEIGHT = 17
TILE_WIDTH = 16
TILE_SIZE = 16
HALF_TILE_SIZE = TILE_SIZE // 2
QUARTER_TILE_SIZE = HALF_TILE_SIZE // 2

ATLAS_HEIGHT = 11
ATLAS_WIDTH = 11
NUM_TILE_TYPES = ATLAS_HEIGHT * ATLAS_WIDTH

SCREEN_DIMS = Vector2(240, 160)*1.2
WINDOW_DIMS = SCREEN_DIMS * 3.0

VIEWPORT_SIZE = 16


def get_tile_area(i):
    i = i % (ATLAS_HEIGHT * ATLAS_WIDTH)

    y = math.floor(i / ATLAS_WIDTH)
    py = y * TILE_HEIGHT
    x = i % ATLAS_WIDTH
    px = x * TILE_SIZE
    return (px, py, TILE_SIZE, TILE_HEIGHT)


def to_iso_coords(x, y):
    return (
        x * HALF_TILE_SIZE - (y * HALF_TILE_SIZE),
        y * QUARTER_TILE_SIZE + (x * QUARTER_TILE_SIZE))


def main():
    pygame.init()

    screen = pygame.Surface(SCREEN_DIMS)
    window = pygame.display.set_mode(WINDOW_DIMS)
    # window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    tiles_im = pygame.image.load('./tiles.png')  # .convert_alpha()

    clock = pygame.time.Clock()
    running = True

    tiles = []
    i = 0
    for y in range(VIEWPORT_SIZE):
        row = []
        for x in range(VIEWPORT_SIZE):
            row.append(random.choice([0, 1, 11, 12]))
            # row.append(i)
            # row.append(1)
            # row.append(random.randint(0, 40))
            i += 1
        tiles.append(row)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
                running = False
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        t = pygame.time.get_ticks()
        flex_factor = 0.5
        start_x, start_y = SCREEN_DIMS.x / 2, SCREEN_DIMS.y / 8
        for y in range(VIEWPORT_SIZE):
            for x in range(VIEWPORT_SIZE):
                iso_coords = to_iso_coords(x, y)
                screen.blit(
                    tiles_im, (
                        start_x + iso_coords[0],
                        start_y + iso_coords[1]
                        + (TILE_SIZE//1)
                        * -(math.sin(
                            x * flex_factor
                            + y * flex_factor // 8
                            + t*0.008
                        )/2.0 + 0.5)
                        * ((math.sin(2.0+t*0.004)/2.0 + 0.5)**2)
                    ),
                    get_tile_area(tiles[y][x])
                )
        # mt = pygame.mouse.get_pos()
        # m = (Vector2(mt[0], mt[1]).elementwise() /
        #      WINDOW_DIMS).elementwise() * SCREEN_DIMS
        # pygame.draw.rect(screen, (255, 255, 255),
        #                  pygame.Rect(m.x-4, m.y-4, 8, 8))

        blit = pygame.transform.scale(screen, window.get_size())
        window.blit(blit, (0, 0))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
