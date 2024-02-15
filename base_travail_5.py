# Example file showing a circle moving on screen
import pygame 
import random
from map import carte
from grid import Grid
from utils import Pos
from read_colors import read_color_parameters
from keyboard import keyboard
# pygame setup
pygame.init()

#constantes
tilesize = 32 # taille d'une tuile IG
size = (20, 10) # taille du monde
fps = 30 # fps du jeu
player_speed = 150 # vitesse du joueur
next_move = 0 #tic avant déplacement
next2_move = 0

# color
read = read_color_parameters()
read.readColors("color.ini")
color = read.c

level = "data/laby-02.dat"

laby = carte(size[0], size[1])
laby.load_from_file(level)
laby.set_color(color["wall_color"])

grid = Grid(size[0], size[1],tilesize)
grid.set_color(color["grid_color"])

screen = pygame.display.set_mode((size[0]*tilesize, size[1]*tilesize))
clock = pygame.time.Clock()
running = True
dt = 0

show_grid = True
show_pos = False

keys= { "UP":0 , "DOWN":0, "LEFT":0, "RIGHT":0 , "HAUT":0, "BAS":0, "GAUCHE":0, "DROITE":0}
kb = keyboard(keys)

player_pos = Pos(0,1)
player2_pos = Pos(3,3)
    #
    #   Gestion des I/O  
    #
    
    #   lecture clavier / souris
while kb.running:

    kb.get()
    keys = kb.k
    kb.n += dt

    if kb.n>0:
        new_x, new_y = player_pos.x, player_pos.y
        if keys['UP'] == 1:
            new_y -=1
        elif keys['DOWN'] == 1:
            new_y += 1
        elif keys['LEFT'] == 1:
            new_x -=1
        elif keys['RIGHT'] == 1:
            new_x += 1

    #
    # gestion des déplacements
    #

    next_move += dt
    if next_move>0:
        new_x, new_y = player_pos.x, player_pos.y
        if keys['UP'] == 1:
            new_y -=1
        elif keys['DOWN'] == 1:
            new_y += 1
        elif keys['LEFT'] == 1:
            new_x -=1
        elif keys['RIGHT'] == 1:
            new_x += 1

        next2_move += dt
    if next2_move>0:
        new2_x, new2_y = player2_pos.x, player2_pos.y
        if keys['HAUT'] == 1:
            new2_y -=1
        elif keys['BAS'] == 1:
            new2_y += 1
        elif keys['GAUCHE'] == 1:
            new2_x -=1
        elif keys['DROITE'] == 1:
            new2_x += 1

        # vérification du déplacement du joueur                                    
        if not laby.hit_box(new_x, new_y):
            player_pos.x, player_pos.y = new_x, new_y
            next_move -= player_speed

            if not laby.hit_box(new2_x, new2_y):
                player2_pos.x, player2_pos.y = new2_x, new2_y
                next2_move -= player_speed

        if show_pos:
            print("pos: ",player_pos)

    #
    # affichage des différents composants graphique
    #
    screen.fill(color["ground_color"])

    laby.draw(screen, tilesize)

    if show_grid:
        grid.draw(screen)

    pygame.draw.rect(screen, color["player_color"], pygame.Rect(player_pos.x*tilesize, player_pos.y*tilesize, tilesize, tilesize))
    pygame.draw.rect(screen, color["player2_color"], pygame.Rect(player2_pos.x*tilesize, player2_pos.y*tilesize, tilesize, tilesize))


    # affichage des modification du screen_view
    pygame.display.flip()
    # gestion fps
    dt = clock.tick(fps)

pygame.quit()