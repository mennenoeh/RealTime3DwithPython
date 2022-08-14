import sys
from turtle import color
import pygame

MAP_SIZE_PX_X, MAP_SIZE_PX_Y = MAP_SIZE_PX = (800, 600)
STATUS_BAR_PX_X, STATUS_BAR_PX_Y = STATUS_BAR_PX = (MAP_SIZE_PX_X , 50)
SCREEN_SIZE_PX_X, SCREEN_SIZE_PX_Y = SCREEN_SIZE_PX = (MAP_SIZE_PX_X, MAP_SIZE_PX_Y + STATUS_BAR_PX_Y)

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE_PX_X, SCREEN_SIZE_PX_Y))

draw_area = pygame.surface.Surface((MAP_SIZE_PX_X, MAP_SIZE_PX_Y))
draw_area.fill((255, 255, 255))



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    screen.blit(draw_area, (0, STATUS_BAR_PX_Y))
    
    pygame.display.update()

