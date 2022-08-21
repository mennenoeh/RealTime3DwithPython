# Distancen mehr nutzen
 
# TODO: wayfinding in agent überführen, 
# KDE überführung, 
# mehrere Agenten generieren, 
# shoppinglist und TSP integrieren, 
# if durch dict ersetzen
# draw order: erst grid, dann heatmap, dann regale
#status bar füllen
# kategorien mit mausrad auswählen können

from util import CI_COLORS
from random import randint, choice
import numpy as np  
import sys, pygame

from sim_kls import Agent, Map
from tcod import path
from wayfinding import get_path

pygame.init()

MAP_SIZE = width_cells, height_cells = 50, 30
CELL_SIZE_PX = 30
STATUS_BAR_HEIGHT_PX = 50

draw_area_size_px = width_px, height_px = width_cells * CELL_SIZE_PX, height_cells * CELL_SIZE_PX
window_size_px = width_px, height_px + STATUS_BAR_HEIGHT_PX
status_bar_size_px = width_px, STATUS_BAR_HEIGHT_PX

# create surfaces
draw_area = pygame.surface.Surface(draw_area_size_px)
status_bar = pygame.surface.Surface(status_bar_size_px)
window = pygame.display.set_mode(window_size_px)
print(window.get_size())



# create map
map = Map(MAP_SIZE, cell_size=CELL_SIZE_PX, statusbar_height=STATUS_BAR_HEIGHT_PX)

#create sample agent

# start_pos = 0, 5
# end_pos = 0, 22
start_pos = choice(map.get_cells_from_type("start"))
end_pos = choice(map.get_cells_from_type("end"))

agent_smith = Agent(map=map)
agent_smith.set_pos(np.array((float(randint(0,width_px)), float(randint(0,height_px))))) # hier nich set path

# walk = get_path(map, choice(map.get_cells_from_type("start")), choice(map.get_cells_from_type("end")))
# walk = get_path(map, start_pos, end_pos)

# agent_smith.set_path(agent_smith.calculate_cell_path(start_pos, end_pos))

choice(map.get_cells_from_type("start")), choice(map.get_cells_from_type("end"))

agents = [Agent(map=map) for _ in range(100)]
for agent in agents:
    agent.set_path(agent_smith.calculate_cell_path(choice(map.get_cells_from_type("start")), choice(map.get_cells_from_type("end"))))

# agents = [agent.set_path(agent.calculate_cell_path(choice(map.get_cells_from_type("start")), choice(map.get_cells_from_type("end")))) for agent in agents]
print(len(agents))

mode : str = ""

draw_area.fill(CI_COLORS.WHITE.value)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            # np.savetxt("store.csv", (map.grid.T), delimiter=",", fmt="%2i")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "b"
                print(mode)
            elif event.key == pygame.K_s:
                mode = "s"
                print(mode)
            elif event.key == pygame.K_e:
                mode = "e"
                print(mode)
        # event.type == pygame.MOUSEBUTTONDOWN

       
        if pygame.mouse.get_pressed()[0] == 1:
            print(map.mouse_to_cell())
            if mode == "b":
                map.set_cell_from_mouse(cell_type="blocked")
            elif mode == "s":
                map.set_cell_from_mouse(cell_type="start")
            elif mode == "e":
                map.set_cell_from_mouse(cell_type="end")
            for agent in agents:
                 agent.set_path(agent_smith.calculate_cell_path(choice(map.get_cells_from_type("start")), choice(map.get_cells_from_type("end"))))

        if pygame.mouse.get_pressed()[2] == 1:
            map.set_cell_from_mouse(cell_type="free")
            for agent in agents:
                 agent.set_path(agent_smith.calculate_cell_path(choice(map.get_cells_from_type("start")), choice(map.get_cells_from_type("end"))))
        
    
    window.blit(draw_area, (0, STATUS_BAR_HEIGHT_PX))
    window.blit(status_bar, (0, 0))

    status_bar.fill(CI_COLORS.WHITE.value)
    draw_area.fill(CI_COLORS.WHITE.value)
    # agent_smith.follow_path() -- beruht noch auf spots
    # neo.seek(agent_smith.pos)
    map.draw(screen=draw_area)
    
    # for path_block in walk:
    #     path_block.draw(CI_COLORS.GREY_LIGHT)

    # if len(agent_smith.px_path) > 2:
    #         pygame.draw.lines(draw_area, CI_COLORS.BLUE.value, closed=False, points=agent_smith.px_path)


    # start_pos.draw(CI_COLORS.GREEN)
    # end_pos.draw(CI_COLORS.RED)

    # agent_smith.draw(screen=draw_area)

    for agent in agents:
        agent.draw(screen=draw_area)
    
    # neo.draw(screen=draw_area)
    pygame.display.update()