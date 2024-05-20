import io
import pygame
from pygame.locals import *
from urllib.request import urlopen

pygame.init()
pygame.key.set_repeat(400, 30)

screen= pygame.display.set_mode((1024, 683))


#Chargement des images
fond=pygame.image.load("background.jpg")
perso = pygame.image.load("mc.png").convert_alpha()


pos_sc=perso.get_rect()
pos_sc=pos_sc.move(50,450)


screen.blit(perso,pos_sc)


vitesse = 20
puissasnce_saut = 200
keyboard=py

saut = False
continuer = 1
while continuer:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        if event.type==KEYDOWN:
            if event.key==K_DOWN:
                pos_sc=pos_sc.move(0,vitesse)
            if event.key==K_UP and not saut:
                saut = True
                pos_sc=pos_sc.move(0,-puissasnce_saut)
            if event.key==K_RIGHT:
                pos_sc=pos_sc.move(vitesse,0)
            if event.key==K_LEFT:
                pos_sc=pos_sc.move(-vitesse,0)
            if event.key==K_UP and event.key==K_RIGHT:
                print("test")
    if saut:
        print(pos_sc.y)
        pos_sc=pos_sc.move(0,puissasnce_saut/10)
        if pos_sc.y>450:
            saut=False

    screen.blit(fond, (0,0))
    screen.blit(perso,pos_sc)
    pygame.display.flip()

pygame.quit()