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

import tile_consts

TILE_HEIGHT = 17
TILE_WIDTH = 16
TILE_SIZE = 16
HALF_TILE_SIZE = TILE_SIZE // 2
QUARTER_TILE_SIZE = HALF_TILE_SIZE // 2

ATLAS_HEIGHT = 11
ATLAS_WIDTH = 11
NUM_TILE_TYPES = ATLAS_HEIGHT * ATLAS_WIDTH

SCREEN_DIMS = Vector2(240, 160)*2.0
WINDOW_DIMS = SCREEN_DIMS * 2.0

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

    paths = list(tile_consts.DIRT_PATHS.values()) + \
        list(tile_consts.HALF_DIRT_PATHS.values())

    # tiles = []
    # i = 0
    # for y in range(VIEWPORT_SIZE):
    #     row = []
    #     for x in range(VIEWPORT_SIZE):
    #         row.append(random.choice((paths)))
    #         # row.append(random.choice([0, 1, 11, 12]))
    #         # row.append(i)
    #         # row.append(1)
    #         # row.append(random.randint(0, 40))
    #         i += 1
    #     tiles.append(row)

    top_layer_block_ids = [tile_consts.NAME_TO_INDEX[n]
                           for n in ["GRASS", "HALF_GRASS", "DIRT", "HALF_DIRT"]]
    inner_blocks_ids = [tile_consts.NAME_TO_INDEX[n]
                        for n in ["STONE", "DIRT", "HALF_DIRT", "HALF_STONE"]]
    lower_blocks_ids = [tile_consts.NAME_TO_INDEX[n]
                        for n in ["STONE", "HALF_STONE", "LAVA", "HALF_LAVA"]]

    stone_brick_ids = [tile_consts.NAME_TO_INDEX[n]
                       for n in ["STONE_BRICK"]]

    blocks = []
    i = 0
    for z in range(VIEWPORT_SIZE):
        zrow = []
        for y in range(VIEWPORT_SIZE):
            row = []
            for x in range(VIEWPORT_SIZE):
                if (VIEWPORT_SIZE - 2) < z < VIEWPORT_SIZE:
                    tile = random.choice(top_layer_block_ids)
                elif (VIEWPORT_SIZE - 3) < z <= (VIEWPORT_SIZE - 1):
                    tile = random.choice(stone_brick_ids)
                elif 2 < z <= 7:
                    tile = random.choice(inner_blocks_ids)
                elif z <= 2:
                    tile = random.choice(lower_blocks_ids)
                elif (x == 0) or (x == VIEWPORT_SIZE - 1) or (y == 0):
                    tile = random.choice(stone_brick_ids)
                else:
                    tile = -1

                row.append(tile)
                # row.append(i)
                # row.append(random.choice(2))
                i += 1
            zrow.append(row)
        blocks.append(zrow)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
                running = False
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        # t = pygame.time.get_ticks()
        # flex_factor = 0.5
        # start_x, start_y = SCREEN_DIMS.x / 2, SCREEN_DIMS.y / 8
        # for y in range(VIEWPORT_SIZE):
        #     for x in range(VIEWPORT_SIZE):
        #         iso_coords = to_iso_coords(x, y)
        #         screen.blit(
        #             tiles_im, (
        #                 start_x + iso_coords[0],
        #                 start_y + iso_coords[1]
        #                 + (TILE_SIZE//1)
        #                 * -(math.sin(
        #                     x * flex_factor
        #                     + y * flex_factor // 8
        #                     + t*0.008
        #                 )/2.0 + 0.5)
        #                 * ((math.sin(2.0+t*0.004)/2.0 + 0.5)**2)
        #             ),
        #             get_tile_area(tiles[y][x])
        #         )

        t = pygame.time.get_ticks()
        flex_factor = 0.5
        start_x, start_y = (
            SCREEN_DIMS.x / 2,
            SCREEN_DIMS.y / 10 + (VIEWPORT_SIZE * TILE_SIZE) / 2)
        for z in range(VIEWPORT_SIZE):
            for y in range(VIEWPORT_SIZE):
                for x in range(VIEWPORT_SIZE):
                    iso_coords = to_iso_coords(x, y)
                    block = blocks[z][y][x]
                    if not block == -1:
                        screen.blit(
                            tiles_im, (
                                start_x + iso_coords[0],
                                start_y + iso_coords[1]
                                - z * TILE_SIZE // 2
                                + (TILE_SIZE//1)
                                * -(math.sin(
                                    x * flex_factor
                                    + y * flex_factor // 8
                                    + t*0.008
                                )/2.0 + 0.5)
                                * ((math.sin(2.0+t*0.004)/2.0 + 0.5)**2)
                            ),
                            get_tile_area(blocks[z][y][x])
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
