#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import curses  #per la TUI
from curses.textpad import rectangle
from time import time as t
from random import uniform, randint
from math import sqrt

#constants
N_ELEMENTS_POPULATION = 500
MUTATION_RATE = 0.01
 
MAX_ACC_X = 2
MAX_ACC_Y = 2
MAX_SPD_X   = 2
MAX_SPD_Y   = 2
N_FRAMES = 200
DELAY_STEP = 55 #ms

SCREEN_SIZE_W = 10
SCREEN_SIZE_H = 10
SCREEN_MARGIN  = 3

GOAL_X = 2
GOAL_Y = 2

GOAL_W = 4
GOAL_H = 4

OBSTACLES = []

def print_goal(stdscr):
	x0 = GOAL_X - (GOAL_W//2)
	y0 = GOAL_Y - (GOAL_H//2)
	for i in range(GOAL_W):
		for j in range(GOAL_H):
			if i == 0 or j == 0 or i ==GOAL_W -1 or  j ==GOAL_H -1:
				stdscr.addstr(y0+j,x0+i, ' ',curses.color_pair(4) )
			else:
				stdscr.addstr(y0+j,x0+i, ' ',curses.color_pair(3) )
class Obstacle():
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	
class Mobil():
	def __init__ (self, x0 = 0, y0 = 0):
		#creates position, speed, and acceleration
		self.pos = [ x0, y0 ]
		self.spd0 = [ uniform(- MAX_SPD_X, MAX_SPD_X),
					 uniform(- MAX_SPD_Y, MAX_SPD_Y)]
		self.spd = self.spd0
		self.acc = []
		for i in range(N_FRAMES):
			acc =[ uniform(- MAX_ACC_X, MAX_ACC_X),
			       uniform(- MAX_ACC_Y, MAX_ACC_Y)]
			self.acc.append(acc)
		#entorn variables
		self.end_time   = -1
		self.start_time = t()
		self.finished   = False
		self.crashed    = False
		self.frame = 0
		self.fitness = 0
		
	def update(self):
		#Updates position if all is okey
		if not self.finished and not self.crashed:
			#updating position
			self.pos[0] += self.spd[0]
			self.pos[1] += self.spd[1]
			#updating speed
			self.spd[0] += self.acc[self.frame][0]
			self.spd[1] += self.acc[self.frame][1]
			if self.spd[0] > MAX_SPD_X:
				self.spd[0] = MAX_SPD_X
			elif self.spd[0] < -MAX_SPD_X:
				self.spd[0] = -MAX_SPD_X
			if self.spd[1] > MAX_SPD_Y:
				self.spd[1] = MAX_SPD_Y
			elif self.spd[1] < -MAX_SPD_Y:
				self.spd[1] = -MAX_SPD_Y
			self.fitness = 1 / sqrt( ((GOAL_X-self.pos[0])**2)+ ((GOAL_Y-self.pos[1])**2))
			self.fitness -= 0.014
			self.fitness = abs(self.fitness)
			self.fitness *= 10
			self.frame +=1
		#if crashed
		if self.pos[0] > SCREEN_MARGIN + SCREEN_SIZE_W or self.pos[0] < SCREEN_MARGIN or self.pos[1] > SCREEN_MARGIN + SCREEN_SIZE_H or self.pos[1] < SCREEN_MARGIN:
			   self.crashed = True
		for obstacle in OBSTACLES:
			if self.pos[0] > obstacle.x and self.pos[0] < obstacle.x +obstacle.w and self.pos[1] > obstacle.y and self.pos[1] < obstacle.y +obstacle.h:
				self.crashed = True
		#if finished  
		if not self.finished and  self.pos[0] >= GOAL_X - (GOAL_W/ 2.0) and self.pos[0] <= GOAL_X + (GOAL_W/ 2.0) and self.pos[1] >= GOAL_Y - (GOAL_H// 2.0) and self.pos[1] <= GOAL_Y + (GOAL_H// 2.0):
			self.finished = True
			self.end_time = t() - self.start_time
			self.fitness = 5#15
		
	def get_pos(self):
		x = int(self.pos[0])
		y = int(self.pos[1])
		return x, y
		
	def set_spd(self, spd):
		self.spd0 = spd
		self.spd  = spd

def print_obstacles(stdscr):
	for obst in OBSTACLES:
		for i in range(obst.w):
			for j in range(obst.h):
				stdscr.addstr(obst.y+j, obst.x+i,' ',curses.color_pair(8))

def main(stdscr):
	global SCREEN_SIZE_W
	global SCREEN_SIZE_H 
	global GOAL_X
	global GOAL_Y
	global OBSTACLES
	#creating some obstacles:
	obs = Obstacle(20, 10, 5, 10)
	OBSTACLES.append(obs)
	obs = Obstacle(45, 8, 5, 10)
	OBSTACLES.append(obs)
	obs = Obstacle(60, 7, 5, 10)
	OBSTACLES.append(obs)
	obs = Obstacle(20, 8, 25, 5)
	OBSTACLES.append(obs)
	
	curses.curs_set(0)
	option = 0
	#parell de colors: id, lletres, bk
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
	curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(7, curses.COLOR_BLACK, 39)
	curses.init_pair(8, curses.COLOR_BLACK, 3)
	
	h, w = stdscr.getmaxyx() # get the window size
	#Setting the screen board
	SCREEN_SIZE_W = w - (2 * SCREEN_MARGIN)
	SCREEN_SIZE_H = h - (2 * SCREEN_MARGIN)
	#setting the Goal ubication
	GOAL_X = w - (GOAL_W//2)-SCREEN_MARGIN
	GOAL_Y = h //2 
	#selecciona el parell de colors
	stdscr.attron(curses.color_pair(1))
	#per apagar attroff #attrivute off
	#per poder fer servir el getch amb timeout de 150ms:
	stdscr.nodelay(True)
	stdscr.timeout(DELAY_STEP) #ms
	goOn = True
	#CREATING THE GENERATION 0 randomly:
	naus = []
	for i in range(N_ELEMENTS_POPULATION):
		new_nau = Mobil(x0 = SCREEN_MARGIN, y0 = h//2)
		naus.append(new_nau)
	gen   = 0
	frame = 0         
	while goOn:
		key = stdscr.getch()
		#if c or esc pressed
		if key == ord('c') or key == 27:
			goOn = False
		#Updates the generation
		if frame < N_FRAMES:
			stdscr.clear()
			rectangle(stdscr, SCREEN_MARGIN, SCREEN_MARGIN, SCREEN_MARGIN+SCREEN_SIZE_H, SCREEN_MARGIN+SCREEN_SIZE_W)
			print_goal(stdscr)
			print_obstacles(stdscr)
			best_fit = 0
			best_nau = -1
			naus_actives = 0
			sum_fit = 0
			for nau in naus:
				x, y = nau.get_pos()
				sum_fit += nau.fitness
				if nau.fitness > best_fit:
					best_fit = nau.fitness
					best_nau = naus.index(nau)
				if not nau.crashed:
					if nau.finished:
						stdscr.addstr(y, x, '#',curses.color_pair(6))
					else:
						stdscr.addstr(y, x, '#',curses.color_pair(2))
						naus_actives += 1
				else:
					stdscr.addstr(y, x, '#',curses.color_pair(5))
				nau.update()
			
			if best_nau != -1:
				x, y = naus[best_nau].get_pos()
				stdscr.addstr(y, x, '#', curses.color_pair(7))	
			#Print frames and gen:
			stdscr.addstr(0, 1,' Frame : {0:4d} / {1:d}'.format(frame, N_FRAMES),curses.color_pair(1))
			stdscr.addstr(1, 1,' Best F: {0:.3f} '.format(best_fit),curses.color_pair(1))
			stdscr.addstr(2, 1,' Aver F: {0:.3f} '.format(sum_fit / N_ELEMENTS_POPULATION ),curses.color_pair(1))
			stdscr.addstr(h-2, 1,' Alive: {0:04d} '.format(naus_actives),curses.color_pair(1))
			stdscr.addstr(h-1, 1,' Gen: {0:05d} '.format(gen),curses.color_pair(1))
			stdscr.refresh()
			frame+=1
			# si no queden naus actives
			if naus_actives ==0:
				frame = N_FRAMES
			#Si acaben la iteració:
			if frame >= N_FRAMES:
				#premia els que han acabat abans donant el temps invers:
				t_max = -1
				for nau in naus:
					if nau.end_time > t_max:
						t_max = nau.end_time
				for nau in naus:
					if nau.end_time > -1:
						nau.fitness*= ((t_max/nau.end_time)**2)
				#torna a començar amb una nova generació
				gen+=1
				frame = 0
				nau_weel = [ ]
				#normalitza i torna en escala de 100 tots els fitness i crea el vector ponderat
				for nau in naus:
					nau.fitness /= best_fit
					nau.fitness =int( nau.fitness * 100.0)
					for i in range(nau.fitness):
						nau_weel.append(nau)
				#crea completament random la nova generació a lo bukake
				for i in range(N_ELEMENTS_POPULATION):
					new_nau = Mobil(x0 = SCREEN_MARGIN, y0 = h//2)
					spd_x = nau_weel[randint(0,len(nau_weel)-1)].spd0[0] 
					if uniform(0,1.0)<= MUTATION_RATE :
						spd_x = uniform(- MAX_SPD_X, MAX_SPD_X)
					spd_y = nau_weel[randint(0,len(nau_weel)-1)].spd0[1] 
					if uniform(0,1.0)<= MUTATION_RATE :
						spd_y = uniform(- MAX_SPD_Y, MAX_SPD_Y)
					spd = [spd_x, spd_y]
					new_nau.set_spd(spd)
					for j in range(N_FRAMES):
						acc_x = nau_weel[randint(0,len(nau_weel)-1)].acc[j][0] 
						if uniform(0,1.0)<= MUTATION_RATE :
							acc_x = uniform(- MAX_ACC_X, MAX_ACC_X)
						acc_y = nau_weel[randint(0,len(nau_weel)-1)].acc[j][1] 
						if uniform(0,1.0)<= MUTATION_RATE :
							acc_y = uniform(- MAX_ACC_Y, MAX_ACC_Y)
						acc = [acc_x, acc_y]
						new_nau.acc[j] = acc
					naus[i] = new_nau
				 					
curses.wrapper(main)
