# Créé par zapoid, le 23/01/2024 en Python 3.7
import io
import pygame
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
projectile_garg=pygame.transform.scale(pygame.image.load("projectile_garg.png"),(180,120))
half_hp=pygame.image.load("half_hp.png").convert_alpha()
full_hp=pygame.image.load("full_hp.png").convert_alpha()
one_hit=pygame.image.load("20%hp.png").convert_alpha()
three_hits=pygame.image.load("80%hp.png").convert_alpha()



pos_full_hp=full_hp.get_rect()
pos_full_hp=pos_full_hp.move(20,0)

pos_half_hp=half_hp.get_rect()
pos_half_hp=pos_half_hp.move(20,0)

pos_onehit=one_hit.get_rect()
pos_onehit=pos_onehit.move(20,0)

pos_threehits=three_hits.get_rect()
pos_threehits=pos_threehits.move(20,0)

is_hit=False


pos_no_s=no_s.get_rect()
pos_no_s=pos_no_s.move(50,0)
pos_half_s=half_s.get_rect()
pos_half_s=pos_half_s.move(50,0)
pos_stam=stam.get_rect()
pos_stam=pos_stam.move(50,0)

pos_rg=r_g.get_rect()
pos_rg=pos_rg.move(50,360)
pos_r=r.get_rect()
pos_r=pos_r.move(50,360)
pos_sc=perso.get_rect()
pos_sc=pos_sc.move(50,360)

pos_fall=fall.get_rect()
pos_fall=pos_fall.move(50,360)

pos_garg=garg.get_rect()
pos_garg=pos_garg.move(700,140)
pos_projectile_garg=projectile_garg.get_rect()
pos_projectile_garg.x = 550
pos_projectile_garg.y = 360



in_bounds=False


etat_fond=0

vitesse = 5
puissance_saut = 200
limit_hp=4
limit_stamina = 2
regen_stamina = 0.01
state_stam=0
stamina=limit_stamina
etat_mc=0
in_boundsX=True
in_bounds=True
courir_g=False
courir=False
saut = False
avancer = False
reculer= False
within_range=False

#print(pos_sc.y,pos_r.y,pos_rg.y)
continuer = 1
screen.blit(title,(0,0))

while continuer:
    pygame.time.Clock().tick(60)
    #print(stamina)

    #Quitter
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

    keys=pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        continuer = 0
    print(pos_projectile_garg.x)

    #Changment d'écran
    if keys[pygame.K_RETURN]:
        etat_fond=1
    #Aller à droite
    if keys[pygame.K_d]:
        avancer = True
        etat_mc=1
    if not keys[pygame.K_d]:
        avancer = False
        etat_mc=0
    if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
        courir=True
        etat_mc=1
    if not (keys[pygame.K_d] and keys[pygame.K_LSHIFT]):
        courir=False
        etat_mc=0

    #Aller à gauche
    if keys[pygame.K_a]:
        reculer= True
        etat_mc=2
    if not keys[pygame.K_a]:
        reculer=False
        etat_mc=0
    if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
        courir_g=True
        etat_mc=2
    if not (keys[pygame.K_a] and keys[pygame.K_LSHIFT]):
        courir_g=False
        etat_mc=0

    #collision projectile
    if pos_projectile_garg.colliderect(pos_sc):
        limit_hp-=1
        pos_projectile_garg.x = 550
    """
    if pos_sc.x==pos_projectile_garg.x:
        limit_hp-=1
    if pos_r.x==pos_projectile_garg.x:
        limit_hp-=1
    if pos_rg.x==pos_projectile_garg.x:
        limit_hp-=1
    """



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
        pos_sc=pos_sc.move(0,puissance_saut/24)
        pos_r=pos_r.move(0,puissance_saut/24)
        pos_rg=pos_rg.move(0,puissance_saut/24)
        pos_fall=pos_fall.move(0,puissance_saut/24)
        if pos_sc.y>=360:
            saut=False
    if pos_sc.x>0:
        within_range=True
    else:
        within_range=False


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
            pos_r=pos_r.move(vitesse*1.5,0)
            pos_sc=pos_sc.move(vitesse*1.5,0)
            pos_rg=pos_rg.move(vitesse*1.5,0)

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
            pos_sc=pos_sc.move(-vitesse*1.5,0)
            pos_rg=pos_rg.move(-vitesse*1.5,0)
            pos_r=pos_r.move(-vitesse*1.5,0)
        else:
            pos_sc=pos_sc.move(-vitesse,0)
            pos_rg=pos_rg.move(-vitesse,0)
            pos_r=pos_r.move(-vitesse,0)
        etat_mc=2

    if pos_sc.x >= 690:
        pos_sc.x = 690
        pos_r.x=690
        pos_rg.x=690
##    if pos_r.x>690:
##        pos_sc.x = 690
##        pos_r.x=690
##        pos_rg.x=690








    #affichage
##    if etat_fond==1:
##        screen.blit(fond, (0,0))
##    if etat_mc==0 and etat_fond==1:
##        screen.blit(perso,pos_sc)
##    if etat_mc==1 and etat_fond==1:
##        screen.blit(r,pos_r)
##    if etat_mc==2 and etat_fond==1:
##        screen.blit(r_g,pos_rg)
##    if stamina==2 and etat_fond==1:
##        screen.blit(stam,pos_stam)
##    if stamina<2 and etat_fond==1:
##        screen.blit(half_s,pos_half_s)
##    if stamina>=0 and stamina<1 and etat_fond==1:
##        screen.blit(no_s,pos_no_s)


    if etat_fond==1:
        screen.blit(fond, (0,0))
        screen.blit(garg,pos_garg)
    if etat_mc==0 and etat_fond==1:
        screen.blit(perso,pos_sc)
    if etat_mc==1 and etat_fond==1:
        screen.blit(r,pos_sc)
    if etat_mc==2 and etat_fond==1:
        screen.blit(r_g,pos_sc)

    if limit_hp==4 and etat_fond==1:
        screen.blit(full_hp,pos_full_hp)
    if limit_hp==3 and etat_fond==1:
        screen.blit(three_hits,pos_threehits)
    if limit_hp==2 and etat_fond==1:
        screen.blit(one_hit,pos_onehit)





    if stamina==2 and etat_fond==1:
        screen.blit(stam,pos_stam)
    if stamina<2 and etat_fond==1:
        screen.blit(half_s,pos_half_s)
    if stamina>=0 and stamina<1 and etat_fond==1:
        screen.blit(no_s,pos_no_s)
    if within_range:
        pos_projectile_garg=pos_projectile_garg.move(-20,0)
        if pos_projectile_garg.x<200:
            pos_projectile_garg.x = 550
        screen.blit(projectile_garg,pos_projectile_garg)

##    if within_range:
##        print(pos_projectile_garg.x)
##        screen.blit(projectile_garg,pos_projectile_garg)


    pygame.display.flip()

    if stamina<2:
        stamina +=regen_stamina
    else:
        stamina = limit_stamina
print(pos_sc.x)
print(pos_sc.y)

# si garg est sur le sol, tire projectile perpendiculaire au sol, si dans les airs tire en diagonale


pygame.quit()
