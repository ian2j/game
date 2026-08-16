import numpy as np
import pygame

WALL = 1
FLOOR = 0


class TileMap:
    """A rectangular room bordered by a two-tile-thick wall, with optional
    extra interior wall blocks. Shared by the overworld and every minigame
    room so the grid/collision/draw logic isn't copy-pasted per screen."""

    def __init__(self, width, height, tile_size, wall_color, floor_color, extra_walls=()):
        self.tile_size = tile_size
        self.wall_color = wall_color
        self.floor_color = floor_color

        rows = int(height / tile_size)
        cols = int(width / tile_size)
        self.grid = np.zeros((rows, cols))
        self.grid[:, :2] = WALL
        self.grid[:, -2:] = WALL
        self.grid[:2, :] = WALL
        self.grid[-2:, :] = WALL
        for row_slice, col_slice in extra_walls:
            self.grid[row_slice, col_slice] = WALL

    def draw(self, screen):
        rows, cols = self.grid.shape
        for row in range(rows):
            for col in range(cols):
                x = col * self.tile_size
                y = row * self.tile_size
                color = self.wall_color if self.grid[row][col] == WALL else self.floor_color
                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))

    def can_move(self, x, y, width, height):
        """Can an actor with this bounding box (top-left x, y) occupy this
        position without overlapping a wall tile?"""
        rows, cols = self.grid.shape
        grid_x_left = min(max(int(x / self.tile_size), 0), cols - 1)
        grid_x_right = min(max(int((x + width) / self.tile_size), 0), cols - 1)
        grid_y_up = min(max(int(y / self.tile_size), 0), rows - 1)
        grid_y_down = min(max(int((y + height) / self.tile_size), 0), rows - 1)
        checksum = (
            self.grid[grid_y_up][grid_x_left]
            + self.grid[grid_y_up][grid_x_right]
            + self.grid[grid_y_down][grid_x_left]
            + self.grid[grid_y_down][grid_x_right]
        )
        return bool(checksum == 0)
