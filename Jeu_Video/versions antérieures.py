# Créé par zapoid, le 23/01/2024 en Python 3.7
import io
import pygame
from pygame.locals import *
from urllib.request import urlopen

pygame.init()
pygame.key.set_repeat(1,20)

screen= pygame.display.set_mode((1024, 683))


#Chargement des images
fond=pygame.image.load("background.jpg")
perso = pygame.image.load("mc.png").convert_alpha()
no_s=pygame.image.load("no_stam.png").convert_alpha()
stam=pygame.image.load("full_stam.png").convert_alpha()
half_s=pygame.image.load("half_stam.png").convert_alpha()


pos_no_s=no_s.get_rect()
pos_no_s=pos_no_s.move(0,0)
pos_half_s=half_s.get_rect()
pos_half_s=pos_half_s.move(0,0)
pos_stam=stam.get_rect()
pos_stam=pos_stam.move(0,0)



pos_sc=perso.get_rect()
pos_sc=pos_sc.move(50,450)








vitesse = 5
puissance_saut = 200
limit_stamina = 2
regen_stamina = 0.01
state_stam=0
stamina=limit_stamina

etat_mc=0
courir_g=False
courir=False
saut = False
avancer = False
reculer= False

continuer = 1
while continuer:
    pygame.time.Clock().tick(60)
    print(stamina)

    for event in pygame.event.get():
        keys=pygame.key.get_pressed()
#Quitter
        if event.type == QUIT:
            continuer = 0
#Aller à droite
        if keys[pygame.K_d]:
            avancer = True
        if event.type==KEYUP and event.key==K_d:
            avancer = False
        if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
            courir=True
        if event.type==KEYUP and event.key==K_d:
            courir=False
#Aller à gauche
        if keys[pygame.K_a]:
            reculer= True
        if event.type==KEYUP and event.key==K_a:
            reculer=False
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
            courir_g=True
        if event.type==KEYUP and event.key==K_a:
            courir_g=False

#Saut Diagonale Droite
        if keys[pygame.K_w] and keys[pygame.K_d] and not saut and stamina>=1:
            pos_sc=pos_sc.move(vitesse*2,-puissance_saut)
            stamina-=1
            saut=True

#Saut Diagonale Gauche
        elif keys[pygame.K_w] and keys[pygame.K_a] and not saut and stamina >=1:
            pos_sc=pos_sc.move(-vitesse*2,-puissance_saut)
            saut=True
            stamina-=1
#Saut Normal
        elif keys[pygame.K_w] and not saut and stamina >=1:
            pos_sc=pos_sc.move(0,-puissance_saut)
            saut = True
            stamina-=1
    if saut:
        pos_sc=pos_sc.move(0,puissance_saut/13)
        if pos_sc.y>450:
            saut=False
    if avancer :
        if saut:
            pos_sc=pos_sc.move(vitesse*1.1,0)
        else:
            pos_sc=pos_sc.move(vitesse,0)
    if courir :
        if saut:
            pos_sc=pos_sc.move(vitesse*2,0)
        else:
            pos_sc=pos_sc.move(vitesse,0)
    if reculer:
        if saut:
            pos_sc=pos_sc.move(-vitesse*1.1,0)
        else:
            pos_sc=pos_sc.move(-vitesse,0)
    if courir_g :
        if saut:
            pos_sc=pos_sc.move(-vitesse*2,0)
        else:
            pos_sc=pos_sc.move(-vitesse,0)
    screen.blit(fond, (0,0))
    screen.blit(perso,pos_sc)
    if stamina==2:
        screen.blit(stam,pos_stam)
    if stamina<2:
        screen.blit(half_s,pos_half_s)
    if stamina>=0 and stamina<1:
        screen.blit(no_s,pos_no_s)

    pygame.display.flip()

    if stamina<2:
        stamina +=regen_stamina
    else:
        stamina = limit_stamina





pygame.quit()
