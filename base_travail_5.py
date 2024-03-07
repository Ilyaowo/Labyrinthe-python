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
tilesize = 8 # taille d'une tuile IG
size = (90, 90) # taille du monde
fps = 30 # fps du jeu
player_speed = 30 # vitesse du joueur
next_move = 0 #tic avant déplacement
next2_move = 0
font = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('freesansbold.ttf', 50)
score_player1 = 0
score_player2 = 0
game_over = False
J1_loose = False
J2_loose = False

#sfx
loose_sfx = pygame.mixer.Sound("loose.mp3")
game_over_sfx = pygame.mixer.Sound("game_over.mp3")
pause_sfx = pygame.mixer.Sound("pause.mp3")

# color
read = read_color_parameters()
read.readColors("color.ini")
color = read.c

level = "data/tron_map.dat"

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

direction_player1 = (-1, 0)
direction_player2 = (1, 0)
# keys= { "UP":0 , "DOWN":0, "LEFT":0, "RIGHT":0 , "HAUT":0, "BAS":0, "GAUCHE":0, "DROITE":0}
# kb = keyboard(keys)

player_pos = Pos(87,45)
player2_pos = Pos(3,45)
player_pos_line = []
player2_pos_line = []
    #
    #   Gestion des I/O  
    #
    

    
    #   lecture clavier / souris
running = True
pause = False
while running:

    # kb.get()
    # keys = kb.k
    # kb.n += dt

    # if kb.n>0:
    #    new_x, new_y = player_pos.x, player_pos.y
    #    if keys == ():
    #        direction(0, -1)
    #    elif keys['DOWN'] == 1:
    #        new_y += 1
    #    elif keys['LEFT'] == 1:
    #       new_x -=1
    #    elif keys['RIGHT'] == 1:
    #       new_x += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not pause and not J1_loose == True:
                if event.key == pygame.K_z:
                    direction_player1 = (0, -1)
                    score_player1 += 1
                if event.key == pygame.K_s:
                    direction_player1 = (0, 1)
                    score_player1 += 1
                if event.key == pygame.K_q:
                    direction_player1 = (-1, 0)
                    score_player1 += 1
                if event.key == pygame.K_d:
                    direction_player1 = (1, 0)
                    score_player1 += 1

        if event.type == pygame.KEYDOWN:
            if not pause and not J2_loose == True:
                if event.key == pygame.K_UP:
                    direction_player2 = (0, -1)
                    score_player2 += 1
                if event.key == pygame.K_DOWN:
                    direction_player2 = (0, 1)
                    score_player2 += 1
                if event.key == pygame.K_LEFT:
                    direction_player2 = (-1, 0)
                    score_player2 += 1
                if event.key == pygame.K_RIGHT:
                    direction_player2 = (1, 0)
                    score_player2 += 1
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if pause:
                    pause = False
                else:
                    pause = True
                    pause_sfx.play()
            if event.key == pygame.K_ESCAPE:
                running = False
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if restart_game_button.collidepoint(event.pos):
                    game_over = False
                    J1_loose = False
                    J2_loose = False
                    player_pos = Pos(87, 45)
                    player2_pos = Pos(3, 45)
                    player_pos_line = []
                    player2_pos_line = []
                    next_move = 0
                    next2_move = 0
                    direction_player1 = (-1, 0)
                    direction_player2 = (1, 0)
                    game_over_sfx.stop()
    #
    # gestion des déplacements
    #
    if not pause and not J1_loose == True and game_over != True:
        next_move += dt
        if next_move> 1000 / fps:
            player_pos_line.append((player_pos.x, player_pos.y))
            new_x, new_y = player_pos.x, player_pos.y
            if direction_player1 == (0, -1):
                new_y -=1
            elif direction_player1 == (0, 1):
                new_y += 1
            elif direction_player1 == (-1, 0):
                new_x -=1
            elif direction_player1 == (1, 0):
                new_x += 1
                
            # vérification du déplacement du joueur                                    
            if not laby.hit_box(new_x, new_y):
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

    if not pause and not J2_loose == True and game_over != True:
        next2_move += dt
        if next2_move> 1000 / fps:
            player2_pos_line.append((player2_pos.x, player2_pos.y))  
            new2_x, new2_y = player2_pos.x, player2_pos.y
            if direction_player2 == (0, -1):
                new2_y -=1
            elif direction_player2 == (0, 1):
                new2_y += 1
            elif direction_player2 == (-1, 0):
                new2_x -=1
            elif direction_player2 == (1, 0):
                new2_x += 1

            # vérification du déplacement du joueur                                    
            if not laby.hit_box(new2_x, new2_y):
                player2_pos.x, player2_pos.y = new2_x, new2_y
                next2_move -= player_speed

    if show_pos and game_over != True:
        print("position 1: ",player_pos, "position 2: ", player2_pos)

    #print(player2_pos)
    #print(player_pos_line)

    if J2_loose != True and game_over != True:
        if (player2_pos.x,player2_pos.y) in player2_pos_line or (player2_pos.x,player2_pos.y) in player_pos_line:
                #print("player 2 perdu")
                loose_sfx.play()
                J2_loose = True
                score_player1 += 1

    if J1_loose != True and game_over != True:
        if (player_pos.x,player_pos.y) in player2_pos_line or (player_pos.x,player_pos.y) in player_pos_line:
                #print("player 1 perdu")
                loose_sfx.play()
                J1_loose = True
                score_player2 += 1

    #
    # affichage des différents composants graphique
    #
    screen.fill(color["ground_color"])

    laby.draw(screen, tilesize)

    if show_grid:
        grid.draw(screen)

    pygame.draw.rect(screen, color["player_color"], pygame.Rect(player_pos.x*tilesize, player_pos.y*tilesize, tilesize, tilesize))
    pygame.draw.rect(screen, color["player2_color"], pygame.Rect(player2_pos.x*tilesize, player2_pos.y*tilesize, tilesize, tilesize))
    for elt in player_pos_line:
        pygame.draw.rect(screen, color["line_color"], pygame.Rect(elt[0]*tilesize, elt[1]*tilesize, tilesize, tilesize))
    for elt in player2_pos_line:
        pygame.draw.rect(screen, color["line2_color"], pygame.Rect(elt[0]*tilesize, elt[1]*tilesize, tilesize, tilesize))
    
    
    score1_text = font.render('Score J1: '+ str(score_player1), True, (255, 255, 255), (0, 0, 0))
    screen.blit(score1_text, (0, 0))
    
    score2_text = font.render('Score J2: '+ str(score_player2), True, (255, 255, 255), (0, 0, 0))
    screen.blit(score2_text, (600, 0))
    
    if pause:
        pause_text = font2.render('Pause', True, (255, 255, 255), (0, 0, 0))
        screen.blit(pause_text, (280, 350))
        
    if J1_loose == True:
        direction_player1 = 0
    
    if J2_loose == True:
        direction_player2 = 0
        
    if J1_loose == True and J2_loose == True:
        game_over_sfx.play()
        game_over = True

    if game_over == True:
        game_over_text = font2.render('GAME OVER YEAH !', True, (255, 255, 255), (0, 0, 0))
        screen.blit(game_over_text, (120, 300))
        restart_game_button = pygame.draw.rect(screen, (0, 0, 0), [285, 350, 100, 20])
        restart_text = font.render('Press to restart', True, (255, 255, 255), (0, 0, 0))
        screen.blit(restart_text, (285, 350))
        
    # affichage des modification du screen_view
    pygame.display.flip()
    # gestion fps
    dt = clock.tick(fps)
    
pygame.quit()