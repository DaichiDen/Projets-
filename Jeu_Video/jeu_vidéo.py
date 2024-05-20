# Créé par zapoid, le 23/01/2024 en Python 3.7
import io
import pygame
from random import *
from pygame.locals import *
from urllib.request import urlopen

pygame.init()
pygame.key.set_repeat(1,20)

screen=pygame.display.set_mode((1024, 683))#,pygame.FULLSCREEN)


#Chargement des images
title=pygame.image.load("background1.png")
fond=pygame.image.load("background.jpg")
perso = pygame.transform.scale(pygame.image.load("mc.png"),(64,128))
no_s=pygame.image.load("no_stam.png").convert_alpha()
stam=pygame.image.load("full_stam.png").convert_alpha()
half_s=pygame.image.load("half_stam.png").convert_alpha()
r = pygame.transform.scale(pygame.image.load("r.png"),(60,120))
r_g = pygame.transform.scale(pygame.image.load("r_g.png"),(60,120))
fall=pygame.transform.scale(pygame.image.load("fall.png"),(64,128))
garg=pygame.transform.scale(pygame.image.load("garg.png"),(100,128))
projectile_garg=pygame.transform.scale(pygame.image.load("projectile_garg.png"),(180,80))
half_hp=pygame.image.load("half_hp.png").convert_alpha()
full_hp=pygame.image.load("full_hp.png").convert_alpha()
one_hit=pygame.image.load("20%hp.png").convert_alpha()
three_hits=pygame.image.load("80%hp.png").convert_alpha()
g_o=pygame.transform.scale(pygame.image.load("g_o.jpg"),(1024, 683))
pov_g=pygame.image.load("pov_g.png").convert_alpha()
mc_arme=pygame.transform.scale(pygame.image.load("mc_arme.png"),(64,128))
arrow=pygame.transform.scale(pygame.image.load("arrow.png"),(32,64))

#Initialisation des positions de chaque image utilisé

pos_full_hp=full_hp.get_rect()
pos_full_hp=pos_full_hp.move(-32,-10)

pos_half_hp=half_hp.get_rect()
pos_half_hp=pos_half_hp.move(-32,-10)

pos_onehit=one_hit.get_rect()
pos_onehit=pos_onehit.move(-32,-10)

pos_threehits=three_hits.get_rect()
pos_threehits=pos_threehits.move(-32,-10)

pos_pov_g=pov_g.get_rect()
pos_pov_g=pos_pov_g.move(550,360)

pos_no_s=no_s.get_rect()
pos_no_s=pos_no_s.move(-1,50)

pos_half_s=half_s.get_rect()
pos_half_s=pos_half_s.move(-1,50)

pos_stam=stam.get_rect()
pos_stam=pos_stam.move(-1,50)

pos_sc=perso.get_rect()
pos_sc=pos_sc.move(50,360)

pos_rg=r_g.get_rect()
pos_rg=pos_sc

pos_r=r.get_rect()
pos_r=pos_sc

pos_mc_arme=mc_arme.get_rect()
pos_mc_arme=pos_sc

pos_fall=fall.get_rect()
pos_fall=pos_fall.move(50,360)

pos_garg=garg.get_rect()
pos_garg=pos_garg.move(700,360)

pos_projectile_garg=projectile_garg.get_rect()
pos_projectile_garg.x = pos_garg.x - 50
pos_projectile_garg.y = pos_garg.y

pos_arrow=arrow.get_rect()
pos_arrow=pos_mc_arme
#Initialisation des variables nécessaires dans la boucle

etat_fond=0

limit_hp_garg=10

vitesse = 5

puissance_saut = 200

limit_hp=4

limit_stamina = 2

regen_stamina = 0.03

cooldown=2

cooldown_regen=0.03

state_stam=0

stamina=limit_stamina

etat_mc=0

etat_shoot=0

crouch=False

courir_g=False

courir=False

saut = False

avancer = False

reculer= False

within_range=False

Dead=False

shoot=False

shoot_h=False

shoot_b=False

is_hit=False

Dead_garg=False

debut=False

degats_proj=True
collided=0
continuer = 1
screen.blit(title,(0,0))

while continuer:
    pygame.time.Clock().tick(120)
    #Quitter
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

    keys=pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        continuer = 0
    if limit_hp_garg<1:
        Dead_garg=True
    #Changment d'écran
    if keys[pygame.K_RETURN]:
        etat_fond=1
    #Aller à droite
    if keys[pygame.K_d]:
        avancer = True
        etat_mc=1
        debut=True
    if not keys[pygame.K_d]:
        avancer = False
        etat_mc=0
    if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
        courir=True
        etat_mc=1
        debut=True
    if not (keys[pygame.K_d] and keys[pygame.K_LSHIFT]):
        courir=False
        etat_mc=0

    #Aller à gauche
    if keys[pygame.K_a]:
        reculer= True
        etat_mc=2
        debut=True
    if not keys[pygame.K_a]:
        reculer=False
        etat_mc=0
    if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
        courir_g=True
        etat_mc=2
        debut=True
    if not (keys[pygame.K_a] and keys[pygame.K_LSHIFT]):
        courir_g=False
        etat_mc=0

    #Sprite perso armé
    if keys[pygame.K_RIGHT] and debut==True:
        shoot = True
        etat_shoot=1
        pos_mc_arme.x=pos_sc.x+10
        pos_mc_arme.y=pos_sc.y
    if not keys[pygame.K_RIGHT]:
        etat_shoot=0
    #collision projectile
    if pos_projectile_garg.collidepoint(pos_sc.x,pos_sc.y):
        if degats_proj:
            limit_hp-=1
        pos_projectile_garg.x = pos_garg.x -30
    #collision projectile joueur
    if pos_arrow.collidepoint(pos_garg.x,pos_garg.y):
        limit_hp_garg-=1
        degats_proj=False
        shoot=False
        pos_arrow=pos_sc
    #Saut Diagonale Droite
    if keys[pygame.K_w] and keys[pygame.K_d] and not saut and stamina>=1:
        pos_sc=pos_sc.move(vitesse*2,-puissance_saut)
        saut=True
        stamina-=1
        debut=True
    #Saut Diagonale Gauche
    elif keys[pygame.K_w] and keys[pygame.K_a] and not saut and stamina >=1:
        pos_sc=pos_sc.move(-vitesse*2,-puissance_saut)
        saut=True
        stamina-=1
        debut=True
    #Saut Normal
    elif keys[pygame.K_w] and not saut and stamina >=1:
        pos_sc=pos_sc.move(0,-puissance_saut)
        saut = True
        stamina-=1
        debut=True

    if saut:
        pos_sc=pos_sc.move(0,puissance_saut/24)
        if pos_sc.y>=360:
            saut=False
    if pos_sc.x>300:
        within_range=True
    if avancer :
        if saut:
            pos_sc=pos_sc.move(vitesse*2,0)
        else:
            pos_sc=pos_sc.move(vitesse,0)
        etat_mc=1

    if courir :
        if saut:
            pos_sc=pos_sc.move(vitesse*1.5,0)
        else:
            pos_sc=pos_sc.move(vitesse,0)
        etat_mc=1
    if reculer:
        if saut:
            pos_sc=pos_sc.move(-vitesse*1.1,0)
        else:
            pos_sc=pos_sc.move(-vitesse,0)
        etat_mc=2
    if courir_g :
        if saut:
            pos_sc=pos_sc.move(-vitesse*1.5,0)
        else:
            pos_sc=pos_sc.move(-vitesse,0)
        etat_mc=2




    # Murs invisibles
    if pos_sc.x >= 690:
        pos_sc.x = 690

    if pos_sc.x <= 0:
        pos_sc.x = 0

    #affichage des images en fonction des différentes variables d'état
    if etat_fond==1:
        screen.blit(fond, (0,0))
        if not Dead_garg:
            screen.blit(garg,pos_garg)
        if etat_shoot==1 :
            screen.blit(mc_arme,pos_mc_arme)
        else:
            if etat_mc==0 :
                screen.blit(perso,pos_sc)
            if etat_mc==1 :
                screen.blit(r,pos_sc)
            if etat_mc==2:
                screen.blit(r_g,pos_sc)


        if limit_hp==4 :
            screen.blit(full_hp,pos_full_hp)
        if limit_hp==3 :
            screen.blit(three_hits,pos_threehits)
        if limit_hp==2 :
            screen.blit(one_hit,pos_onehit)
        if limit_hp<1 :
            Dead=True
            screen.blit(g_o,(0,0))


    if stamina==2 and etat_fond==1 and not Dead:
        screen.blit(stam,pos_stam)
    if stamina<2 and etat_fond==1 and not Dead:
        screen.blit(half_s,pos_half_s)
    if stamina>=0 and stamina<1 and etat_fond==1 and not Dead:
        screen.blit(no_s,pos_no_s)
    if within_range and not Dead and not Dead_garg:
        pos_projectile_garg=pos_projectile_garg.move(-5,0)
        if pos_projectile_garg.x<0:
            pos_projectile_garg.x = pos_garg.x
        screen.blit(projectile_garg,pos_projectile_garg)
    if shoot and etat_fond==1 and not Dead:
        pos_arrow=pos_arrow.move(10,0)
        if pos_arrow.x>800:
            shoot=False
            pos_arrow=pos_mc_arme
        screen.blit(arrow,pos_arrow)
    pygame.display.flip()

    if stamina<2:
        stamina +=regen_stamina
    else:
        stamina = limit_stamina
print(pos_sc.x)
print(pos_sc.y)

# si garg est sur le sol, tire projectile perpendiculaire au sol, si dans les airs tire en diagonale
# si perso est dans champ de vision de garg,tire rayon sinon non
# faire pos_rg/pos_g/pos_mc_arme=pos_sc (comme pour pos_mc_arme, ça fera moins de lignes)


pygame.quit()
