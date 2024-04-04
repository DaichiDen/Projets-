# Créé par daniz, le 25/01/2024 en Python 3.7
# Créé par zapoid, le 23/01/2024 en Python 3.7
import io
import pygame
from pygame.locals import *
from urllib.request import urlopen

pygame.init()
pygame.key.set_repeat(1,20)

screen=pygame.display.set_mode((1024, 683), pygame.FULLSCREEN)


#Chargement des images
fond=pygame.image.load("background.jpg")
perso = pygame.transform.scale(pygame.image.load("mc.png"),(64,128))
no_s=pygame.image.load("no_stam.png").convert_alpha()
stam=pygame.image.load("full_stam.png").convert_alpha()
half_s=pygame.image.load("half_stam.png").convert_alpha()
r = pygame.transform.scale(pygame.image.load("r.png"),(64,128))
r_g = pygame.transform.scale(pygame.image.load("r_g.png"),(64,128))
idle2=pygame.image.load("idle2.png").convert_alpha()
idle3=pygame.image.load("idle3.png").convert_alpha()



pos_no_s=no_s.get_rect()
pos_no_s=pos_no_s.move(0,0)
pos_half_s=half_s.get_rect()
pos_half_s=pos_half_s.move(0,0)
pos_stam=stam.get_rect()
pos_stam=pos_stam.move(0,0)

pos_rg=r_g.get_rect()
pos_rg=pos_rg.move(50,360)
pos_r=r.get_rect()
pos_r=pos_r.move(50,360)
pos_sc=perso.get_rect()
pos_sc=pos_sc.move(50,360)
pos_idle2=idle2.get_rect()
pos_idle2=pos_idle2.move(50,420)
pos_idle3=idle3.get_rect()
pos_idle3=pos_idle3.move(50,420)


idle_l=[pos_sc,pos_idle2,pos_idle3]





vitesse = 5
puissance_saut = 200
gravité=10
vélocité_y=puissance_saut
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
#print(pos_sc.y,pos_r.y,pos_rg.y)
continuer = 1
while continuer:

    pygame.time.Clock().tick(60)
    #print(stamina)
    for event in pygame.event.get():
        keys=pygame.key.get_pressed()
#Quitter
        if event.type == QUIT:
            continuer = 0
#Aller à droite
        if keys[pygame.K_d]:
            avancer = True
            etat_mc=1
        if event.type==KEYUP and event.key==K_d:
            avancer = False
            etat_mc=0
        if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
            courir=True
            etat_mc=1
        if event.type==KEYUP and event.key==K_d:
            courir=False
            etat_mc=0
#Aller à gauche
        if keys[pygame.K_a]:
            reculer= True
            etat_mc=2
        if event.type==KEYUP and event.key==K_a:
            reculer=False
            etat_mc=0
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
            courir_g=True
            etat_mc=2
        if event.type==KEYUP and event.key==K_a:
            courir_g=False
            etat_mc=0
#Saut Diagonale Droite
        if keys[pygame.K_w] and keys[pygame.K_d] and not saut and stamina>=1:
            pos_sc=pos_sc.move(vitesse*2,-puissance_saut)
            pos_r=pos_r.move(vitesse*2,-puissance_saut)
            pos_rg=pos_rg.move(vitesse*2,-puissance_saut)
            saut=True
            stamina-=1



#Saut Diagonale Gauche
        elif keys[pygame.K_w] and keys[pygame.K_a] and not saut and stamina >=1:
            pos_sc=pos_sc.move(-vitesse*2,-puissance_saut)
            pos_r=pos_r.move(vitesse*2,-puissance_saut)
            pos_rg=pos_rg.move(vitesse*2,-puissance_saut)
            saut=True
            stamina-=1


#Saut Normal
        elif keys[pygame.K_w] and not saut and stamina >=1:
            pos_sc=pos_sc.move(0,-puissance_saut)
            pos_r=pos_r.move(0,-puissance_saut)
            pos_rg=pos_rg.move(0,-puissance_saut)
            saut = True
            stamina-=1
    if saut:
        pos_sc.y-=vélocité_y
        vélocité_y-=gravité
        if vélocité_y<-puissance_saut:
            saut=False
            vélocité_y=puissance_saut
        pos_sc=pos_sc.get_rect(center=(pos_sc.x,pos_sc.y))
        screen.blit(perso,pos_sc)

    if avancer :
        if saut:
            pos_r=pos_r.move(vitesse*1.1,0)
            pos_sc=pos_sc.move(vitesse*1.1,0)
            pos_rg=pos_rg.move(vitesse*1.1,0)
        else:
            pos_r=pos_r.move(vitesse,0)
            pos_sc=pos_sc.move(vitesse,0)
            pos_rg=pos_rg.move(vitesse,0)
        etat_mc=1
    if courir :
        if saut:
            pos_r=pos_r.move(vitesse*2,0)
            pos_sc=pos_sc.move(vitesse*2,0)
            pos_rg=pos_rg.move(vitesse*2,0)

        else:
            pos_r=pos_r.move(vitesse,0)
            pos_sc=pos_sc.move(vitesse,0)
            pos_rg=pos_rg.move(vitesse,0)
        etat_mc=1
    if reculer:
        if saut:
            pos_rg=pos_rg.move(-vitesse*1.1,0)
            pos_sc=pos_sc.move(-vitesse*1.1,0)
            pos_r=pos_r.move(-vitesse*1.1,0)

        else:
            pos_rg=pos_rg.move(-vitesse,0)
            pos_sc=pos_sc.move(-vitesse,0)
            pos_r=pos_r.move(-vitesse,0)
        etat_mc=2
    if courir_g :
        if saut:
            pos_sc=pos_sc.move(-vitesse*2,0)
            pos_rg=pos_rg.move(-vitesse*2,0)
            pos_r=pos_r.move(-vitesse*2,0)
        else:
            pos_sc=pos_sc.move(-vitesse,0)
            pos_rg=pos_rg.move(-vitesse,0)
            pos_r=pos_r.move(-vitesse,0)
        etat_mc=2
    screen.blit(fond, (0,0))
    if etat_mc==0:
        screen.blit(perso,pos_sc)
    if etat_mc==1:
        screen.blit(r,pos_r)
    if etat_mc==2:
        screen.blit(r_g,pos_rg)
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

