from curses import COLOR_BLACK, COLOR_BLUE
from util import CI_COLORS
from random import randint
import numpy as np  
import sys, pygame

from sim_kls import Agent, Map, Spot

pygame.init()

map_size = m_width, m_height = 50, 30
grid_size = 20

size = width, height = m_width * grid_size, m_height * grid_size

# screen = pygame.display.set_mode(size)
# print(screen.get_size())

agent_smith = Agent()
agent_smith.set_pos(np.array((float(randint(0,width)), float(randint(0,height)))))
neo = Agent()

map = Map()

start_pos = Spot(5, 25, 0, map)
end_pos   = Spot(25, 25, 0, map)

map.screen.fill(CI_COLORS.WHITE.value)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                map.set_blocked()
            if pygame.mouse.get_pressed()[2] == 1:
                map.set_empty()
        

    map.screen.fill(CI_COLORS.WHITE.value)
    # agent_smith.seek(pygame.mouse.get_pos())
    # neo.seek(agent_smith.pos)
    map.draw(screen=map.screen)
    start_pos.draw(CI_COLORS.GREEN)
    end_pos.draw(CI_COLORS.RED)

    # agent_smith.draw(screen=map.screen)
    # neo.draw(screen=map.screen)
    pygame.display.flip()