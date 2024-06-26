from math import sqrt,pi
from random import randint
import pygame as p

def killplanet(planet):
	planets.remove(planet)

BUNCH_PRE = "bunch"
RANDOM_PRE = "random"

def processparam(inp):
	if inp[:len(RANDOM_PRE)] == RANDOM_PRE:
		mid = len(RANDOM_PRE)
		while inp[mid] != ",": mid+=1
		minval = int(inp[len(RANDOM_PRE)+1:mid])
		maxval = int(inp[mid+1:-1])
		return randint(minval,maxval)
	else: return float(inp)

class Planet():
	def __init__(s,x,y,xv=0,yv=0,mass=100):
		s.mass = mass
		s.density = 1
		s.gravconst = 1000
		s.updateradius()

		s.vel = [xv,yv]
		s.pos = [x,y]

	def updateradius(s):
		s.radius = sqrt((s.mass/s.density)/pi)

	def iscol(s,other,dist = None):
		if not dist: dist = s.distanceto(other)
		return dist < other.radius+s.radius

	def distanceto(s,other):
		return sqrt((s.pos[0]-other.pos[0])**2+(s.pos[1]-other.pos[1])**2)

	def update(s):
		for planet in planets:
			if planet == s: continue
			distance = s.distanceto(planet)
			if distance !=0:
				acclmag = planet.mass*s.gravconst/distance**3
				accl = [acclmag*(planet.pos[0]-s.pos[0]),acclmag*(planet.pos[1]-s.pos[1])]
				s.vel[0]+=accl[0]*dt
				s.vel[1]+=accl[1]*dt
			if s.iscol(planet,distance):
				s.vel[0] = (s.vel[0]*s.mass+planet.vel[0]*planet.mass)/(planet.mass+s.mass)
				s.vel[1] = (s.vel[1]*s.mass+planet.vel[1]*planet.mass)/(planet.mass+s.mass)
				if planet.mass > s.mass:
					s.pos = planet.pos
				s.mass+=planet.mass
				s.updateradius()
				killplanet(planet)
		s.pos[0]+=s.vel[0]*dt
		s.pos[1]+=s.vel[1]*dt
			

	def draw(s):
		drawpos = [s.pos[0]+offset[0],s.pos[1]+offset[1]]
		# weird lines when drawing off screen?
		if drawpos[0] < 0 or drawpos[0] > SS[0] or drawpos[1] < 0 or drawpos[1] > SS[1] : return
		p.draw.circle(screen,"black",drawpos,s.radius)

SS = (600,600)

offset = [0,0]
screen = p.display.set_mode(SS)
clock = p.time.Clock()
dt = 1/60

inputfile = open("input.txt")
planets = []

for line in inputfile:
	line = line.lower().strip()
	if len(line) == 0 or line[0] == "#": continue
	params = [x for x in line.split(" ")]
	if params[0] == "bunch":
		for i in range(int(processparam(params[1]))):
			planets.append(Planet(*[processparam(x) for x in params[2:]]))
	else:
		planets.append(Planet(*[processparam(x) for x in params]))



lastmousepos = -1
running = True
while running:
	dt = clock.tick(60)/1000
	for event in p.event.get():
		if event.type == p.QUIT:
			running = False
	if p.mouse.get_pressed()[0]:
		mousepos = p.mouse.get_pos()
		if lastmousepos != -1:
			offset[0]+= mousepos[0]-lastmousepos[0]
			offset[1]+= mousepos[1]-lastmousepos[1]
		lastmousepos = mousepos
	else:
		lastmousepos = -1

	for planet in planets: planet.update()
	screen.fill("white")
	for planet in planets: planet.draw()

	p.display.update()