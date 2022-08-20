from importlib.resources import path
from tarfile import PAX_FIELDS
import pygame
import numpy as np
import numpy.linalg as la
from util import CI_COLORS
from typing import List, Tuple
import random


class Agent:
    def __init__(self) -> None:
        self.pos = np.array((1.0, 1.0))
        self.color = CI_COLORS.BLUE.value
        self.radius = 10
        self.vel = np.array((1.0, 1.0))
        self.acc = np.array((0.0, 0.0))
        self.max_speed = 2
        self.max_force = 0.7
        self.block_path = []
        self.px_path = []

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.line(screen, CI_COLORS.GREEN.value, self.pos, self.pos + (self.vel * 10), width=3 )
        #pygame.draw.circle(screen, CI_COLORS.RED_DARK.value, self.pos, 1)

    def set_pos(self, pos: Tuple[float]) -> None:
        self.pos = pos
    
    def seek(self, target_pos: np.array) -> None:
        self.acc = (target_pos - self.pos) - self.vel
        self.update()
    
    def update(self) -> None:
        if np.linalg.norm(self.acc) > self.max_force: 
            self.acc = (self.acc / np.linalg.norm(self.acc)) * self.max_force
        self.vel += self.acc
        if np.linalg.norm(self.vel) > self.max_speed: 
            self.vel = (self.vel / np.linalg.norm(self.vel)) * self.max_speed
        self.pos += self.vel
        self.acc[0], self.acc[1] = 0.0, 0.0
        # hier raycasting
    
    def set_block_path(self, path):
        self.block_path = path.copy()
        self.px_path = [a.get_random_pos() for a in self.block_path]
    
    def follow_path(self):
        if self.block_path[0].is_within(self.pos) and len(self.block_path) >= 2:
            self.block_path.pop(0)
            self.px_path.pop(0)
        self.seek(self.px_path[0])


class Spot:
    def __init__(self, x: np.int8, y: np.int8, blocked: np.int8, map) -> None:
        self.x = x
        self.y = y
        self.blocked = blocked
        self.map = map
        self.left = x * map.grid_size + 1
        self.top = y * map.grid_size + 1
        self.right = self.left + map.grid_size - 1
        self.bottom = self.top + map.grid_size - 1
        self.r = pygame.Rect(self.left, self.top, map.grid_size-1, map.grid_size-1)

    def draw(self, color:CI_COLORS):
        pygame.draw.rect(self.map.screen, color=color.value, rect=self.r)
    
    def get_block(self):
        return self.x, self.y
    
    def get_center_pos(self):
        return self.left + (self.map.grid_size // 2), self.top + (self.map.grid_size // 2)
    
    def get_random_pos(self):
        return random.uniform(self.left, self.right), random.uniform(self.top, self.bottom)
    
    def is_within(self, pos) -> bool:
        x, y = pos
        if x > self.left and x < self.right and y > self.top and y < self.bottom:
            return True
        else:
            return False

class Map:
    # def __init__(self, shape = (50, 30), grid_size = 30) -> None: #TODO: Hier Screen ergänzen konstruktor und gridsize 
    #     self.max_x, self.max_y = shape
    #     self.grid_size = grid_size
    #     self.screen_max_x, self.screen_max_y = self.max_x*self.grid_size, self.max_y*self.grid_size
    #     self.screen = pygame.display.set_mode((self.screen_max_x, self.screen_max_y))

    #     self.grid = np.loadtxt("store.csv", delimiter=",").astype("int8").T
    #     # np.savetxt("store.csv", (self.grid.T), delimiter=",", fmt="%2i")
    #     self.spots = np.ndarray(shape, Spot)
    #     for x in range(self.max_x):
    #         for y in range(self.max_y):
    #             self.spots[x,y] = Spot(x=x, y=y, blocked=(int(self.grid[x, y])), map=self)

    def __init__(self, draw_area: pygame.Surface) -> None: #TODO: Hier Screen ergänzen konstruktor und gridsize 
        self.max_x, self.max_y = draw_area.get_size()
        self.grid_size = 30
        self.screen_max_x, self.screen_max_y = self.max_x, self.max_y
        self.screen = pygame.display.set_mode((self.screen_max_x, self.screen_max_y))

        self.grid = np.loadtxt("store.csv", delimiter=",").astype("int8").T
        # np.savetxt("store.csv", (self.grid.T), delimiter=",", fmt="%2i")
        self.spots = np.ndarray(draw_area.get_size(), Spot)
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.spots[x,y] = Spot(x=x, y=y, blocked=(int(self.grid[x, y])), map=self)
    
    def draw_grid(self, screen: pygame.Surface):
        width, height = screen.get_size()
        v_points = np.linspace(0, height, self.max_y+1)
        h_points = np.linspace(0, width,  self.max_x+1)
        for v in v_points:
            pygame.draw.line(screen, CI_COLORS.GREY_LIGHT.value, (0, v), (width, v))
        for h in h_points:
            pygame.draw.line(screen, CI_COLORS.GREY_LIGHT.value, (h, 0), (h, height))
        # print(v_points)

    def draw_spots(self, screen: pygame.Surface):
        for spot in self.spots.flatten():
            if spot.blocked == 0:
                pygame.draw.rect(screen, color=CI_COLORS.BLACK.value, rect=spot.r)

    def set_blocked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // self.grid_size
        grid_y = mouse_y // self.grid_size
        self.spots[grid_x, grid_y].blocked = 0
        self.grid[grid_x, grid_y] = 0
    
    def set_empty(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // self.grid_size
        grid_y = mouse_y // self.grid_size
        self.spots[grid_x, grid_y].blocked = 1
        self.grid[grid_x, grid_y] = 1


    def draw(self, screen: pygame.Surface) -> None:
        self.draw_grid(screen=screen)
        self.draw_spots(screen=screen)


