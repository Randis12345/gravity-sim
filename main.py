from math import sqrt,pi
import pygame as p

def killplanet(planet):
	planets.remove(planet)

class Planet():
	def __init__(s,x,y,mass=100):
		s.mass = mass
		s.density = 1
		s.gravconst = 1000
		s.updateradius()

		s.vel = [0,0]
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
			acclmag = planet.mass*s.gravconst/distance**3
			accl = [acclmag*(planet.pos[0]-s.pos[0]),acclmag*(planet.pos[1]-s.pos[1])]
			s.vel[0]+=accl[0]*dt
			s.vel[1]+=accl[1]*dt
			if s.iscol(planet,distance):
				s.vel[0] = (s.vel[0]*s.mass+planet.vel[0]*planet.mass)/(planet.mass+s.mass)
				s.vel[1] = (s.vel[1]*s.mass+planet.vel[1]*planet.mass)/(planet.mass+s.mass)
				s.mass+=planet.mass
				s.updateradius()
				killplanet(planet)
		s.pos[0]+=s.vel[0]*dt
		s.pos[1]+=s.vel[1]*dt
			

	def draw(s):
		p.draw.circle(screen,"black",s.pos,s.radius)

SS = (600,600)
screen = p.display.set_mode(SS)
clock = p.time.Clock()
dt = 1/60

planets = [Planet(300,300),Planet(500,400)]

running = True
while running:
	dt = clock.tick(60)/1000
	for event in p.event.get():
		if event.type == p.QUIT:
			running = False

	for planet in planets: planet.update()
	screen.fill("white")
	for planet in planets: planet.draw()

	p.display.update()