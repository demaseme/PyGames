# 1 importando librerias
import pygame
import math
from pygame.locals import *
import random

# 2 inicializando el juego

pygame.init()
width, height = 640,480
screen=pygame.display.set_mode((width,height))
keys = [False, False, False, False]
playerpos=[100,100]
acc=[0,0]
arrows=[]
badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194
pygame.mixer.init()
background = pygame.Surface((screen.get_size()))
backgroundrect = background.get_rect()
background.fill((255,255,255)) # fill white
background = background.convert()
screen.blit(background,(0,0))
# 3 cargando imagenes

player=pygame.image.load("resources/images/dude.png")
player2=pygame.image.load("resources/images/dude2.png")
player3=pygame.image.load("resources/images/dude3.png")
grass=pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow=pygame.image.load("resources/images/bullet.png")
badguyimg1=pygame.image.load("resources/images/badguy.png")
badguyimg2=pygame.image.load("resources/images/badguy2.png")
badguyimg3=pygame.image.load("resources/images/badguy3.png")
badguyimg4=pygame.image.load("resources/images/badguy4.png")
badguyimg=badguyimg1
badguyimgs=[badguyimg1,badguyimg2,badguyimg3,badguyimg4]
healthbar=pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover=pygame.image.load("resources/images/gameover.png")
youwin=pygame.image.load("resources/images/youwin.png")

# 3.1 cargar audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)

# 4 ciclos
running=1
exitcode=0
picnr=0
counter=0

while 1:
	counter+=1
	badtimer-=1
	# 5 limpiamos la pantalla antes de volver a dibujarla
	screen.fill(0)
	# 6 dibujamos los elementos de la pantalla
	for x in range(width/grass.get_width()+1):
		for y in range(height/grass.get_height()+1):
			screen.blit(grass,(x*100,y*100))
			#background.blit(grass,(x*100,y*100))
	screen.blit(castle,(0,30))
	screen.blit(castle,(0,135))
	screen.blit(castle,(0,240))
	screen.blit(castle,(0,345))
	#screen.blit(player,playerpos)
	####################################################
	position = pygame.mouse.get_pos()
	angle = math.atan2(position[1]-(playerpos[1]),position[0]-(playerpos[0]))
	playerrot=pygame.transform.rotate(player,360-angle*57.29) #radianes -> grados
	playerrot2=pygame.transform.rotate(player2,360-angle*57.29) #radianes -> grados
	playerpos1=(playerpos[0]-playerrot.get_rect().width/2,playerpos[1]-playerrot.get_rect().height/2)
	playerpos2=(playerpos[0]-playerrot2.get_rect().width/2,playerpos[1]-playerrot2.get_rect().height/2)
	screen.blit(playerrot,playerpos1)
	#6.2 dibujar flechas
	for bullet in arrows:
		screen.blit(grass,playerpos1)
		screen.blit(playerrot2,playerpos1)
		index = 0
		velx=math.cos(bullet[0])*10
		vely=math.sin(bullet[0])*10
		bullet[1]+=velx
		bullet[2]+=vely
		if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
			arrows.pop(index)
		index+=1
		for projectile in arrows:
			arrow1=pygame.transform.rotate(arrow,360-projectile[0]*57.29)
			screen.blit(arrow1,(projectile[1],projectile[2]))
	#6.3 dibujar badgers
	if badtimer==0:
		badguys.append([640,random.randint(50,430)])
		badtimer=100-(badtimer1*2)
		if badtimer1>=35:
			badtimer1=35
		else:
			badtimer1+=5
	index=0
	for badguy in badguys:
		if badguy[0]<-64:
			badguys.pop(index)
		badguy[0]-=7
		#print badguy
		#6.3.1 ataque al castillo
		badrect=pygame.Rect(badguyimg.get_rect())
		badrect.top=badguy[1]
		badrect.left=badguy[0]
		#Si toca el castillo...
		if badrect.left<64:
			hit.play()
			healthvalue -= random.randint(5,20)
			badguys.pop(index)
		#6.3.2  
		index1=0
		#Checar cada flecha para ver si choco con un badger
		for bullet in arrows:
			bullrect=pygame.Rect(arrow.get_rect())
			bullrect.left=bullet[1]
			bullrect.top=bullet[2]
			if badrect.colliderect(bullrect):
				enemy.play()
				acc[0]+=1
				badguys.pop(index)
				arrows.pop(index1)
			index1+=1
		#6.3.3 proximo badger 
		index+=1
	for badguy in badguys:
		mypicture=badguyimgs[picnr]
		#screen.blit(grass,badguy)
		screen.blit(mypicture,badguy)
		print counter
		if counter%10>1:
			picnr=1
		if counter%10>2:
			picnr=2
		if counter%10>3:
			picnr=3
		if counter%10>4:
			counter=0
			picnr=1
		
	#6.4 dibujar reloj
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+
	str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
	textRect=survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(survivedtext,textRect)
	#6.5 dibujar vida
	screen.blit(healthbar,(5,5))
	for health1 in range(healthvalue):
		screen.blit(health,(health1+8,8))
	# 7 actualizamos la pantalla
	pygame.display.flip()
	# 8 ciclo de los eventos
	for event in pygame.event.get():
		#checamos si el evento es un key x
		if event.type==pygame.QUIT:
			#si lo es, entonces sal del juego
			pygame.quit()
			exit(0)
		if event.type == pygame.KEYDOWN:
			if event.key==K_w:
				keys[0]=True
			elif event.key==K_a:
				keys[1]=True
			elif event.key==K_s:
				keys[2]=True
			elif event.key==K_d:
				keys[3]=True
		if event.type==pygame.KEYUP:
			if event.key==pygame.K_w:
				keys[0]=False
			elif event.key==pygame.K_a:
				keys[1]=False
			elif event.key==pygame.K_s:
				keys[2]=False
			elif event.key==pygame.K_d:
				keys[3]=False
		#Get mouse position and calculate arrow rotation based
		#on the rotated player position and the cursor position. 
		#Then stores the rotation value in arrows array.
		if event.type==pygame.MOUSEBUTTONDOWN:
			shoot.play()		
			position=pygame.mouse.get_pos()
			acc[1]+=100
			arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
	if keys[0]:
		playerpos[1]-=5
	elif keys[1]:
		playerpos[0]-=5
	elif keys[2]:
		playerpos[1]+=5
	elif keys[3]:
		playerpos[0]+=5
	# 10 checar win/lose
	if pygame.time.get_ticks()>=90000:
		running=0
		exitcode=1
		break
	if healthvalue<=0:
		running=0
		exitcode=0
		break
	if acc[1]!=0:
		accuarcy=acc[0]*1.0/acc[1]*100
	else:
		accuarcy=0
#11 Mostrar win/lose
if exitcode==0:
	pygame.font.init()
	font=pygame.font.Font(None, 24)
	text= font.render("Accuarcy: "+str(accuarcy)+"%", True,(255,0,0))
	textRect= text.get_rect()
	textRect.centerx=screen.get_rect().centerx
	textRect.centery=screen.get_rect().centery+24
	screen.blit(gameover,(0,0))
	screen.blit(text,textRect)
else:
	pygame.font.init()
	font=pygame.font.Font(None,24)
	text = font.render("Accuarcy: "+str(accuarcy)+"%", True, (0,255,0))
	textRect=text.get_rect()
	textRect.centerx=screen.get_rect().centerx
	textRect.centery=screen.get_rect().centery
	screen.blit(youwin,(0,0))
	screen.blit(text,textRect)
while 1:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			exit(0)
	pygame.display.flip()
			