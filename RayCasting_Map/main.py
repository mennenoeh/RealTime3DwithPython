# Distancen mehr nutzen
 
# 

from curses import COLOR_BLACK, COLOR_BLUE
from tkinter import Spinbox
from util import CI_COLORS
from random import randint
import numpy as np  
import sys, pygame

from sim_kls import Agent, Map, Spot
from tcod import path
from wayfinding import get_path

pygame.init()

MAP_SIZE = width_cells, height_cells = 50, 30
CELL_SIZE_PX = 30
STATUS_BAR_HEIGHT_PX = 50

draw_area_size_px = width_px, height_px = width_cells * CELL_SIZE_PX, height_cells * CELL_SIZE_PX
window_size_px = width_px, height_px + STATUS_BAR_HEIGHT_PX
status_bar_size_px = width_px, STATUS_BAR_HEIGHT_PX

draw_area = pygame.surface.Surface(draw_area_size_px)
status_bar = pygame.surface.Surface(status_bar_size_px)
window = pygame.display.set_mode(window_size_px)


print(window.get_size())

agent_smith = Agent()
agent_smith.set_pos(np.array((float(randint(0,width_px)), float(randint(0,height_px))))) # hier nich set path


neo = Agent()

map = Map(MAP_SIZE)

start_pos = Spot(1, 25, 1, map)
end_pos   = Spot(1, 5, 1, map)

walk = get_path(map,start_pos, end_pos)

agent_smith.set_block_path(walk)

mode : str = ""

map.screen.fill(CI_COLORS.WHITE.value)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "b"
            elif event.key == pygame.K_s:
                mode = "s"
                np.savetxt("store.csv", (map.grid.T), delimiter=",", fmt="%2i")
            elif event.key == pygame.K_e:
                mode = "e"
        # event.type == pygame.MOUSEBUTTONDOWN

        if mode == "b":
            if pygame.mouse.get_pressed()[0] == 1:
                map.set_blocked()
                walk = get_path(map,start_pos, end_pos)
                print(len(walk))
                agent_smith.set_block_path(walk)
            if pygame.mouse.get_pressed()[2] == 1:
                map.set_empty()
                walk = get_path(map,start_pos, end_pos)
                print(len(walk))
                agent_smith.set_block_path(walk)
        
    window.blit(draw_area, (0, STATUS_BAR_HEIGHT_PX))
    map.screen.fill(CI_COLORS.WHITE.value)
    agent_smith.follow_path()
    # neo.seek(agent_smith.pos)
    map.draw(screen=map.screen)
    
    for path_block in walk:
        path_block.draw(CI_COLORS.GREY_LIGHT)

    if len(agent_smith.px_path) > 2:
            pygame.draw.lines(map.screen, CI_COLORS.BLUE.value, closed=False, points=agent_smith.px_path)


    start_pos.draw(CI_COLORS.GREEN)
    end_pos.draw(CI_COLORS.RED)

    agent_smith.draw(screen=map.screen)
    # neo.draw(screen=map.screen)
    pygame.display.update()