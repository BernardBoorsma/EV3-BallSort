#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import random

# Rijden		= motor A + motor D
driveL = LargeMotor('outA')
driveR = LargeMotor('outD')
# Omhoog/omlaag = motor B
up = LargeMotor('outB')
# Grijper		= motor C
grabber = MediumMotor('outC')
# Touchsensor	= sensor 1
touch = TouchSensor('in1')
# Kleursensor	= sensor 3
color = ColorSensor('in3')
color.mode = 'COL-COLOR'

Balletjes = [0]
DrivePos = 0 # Huidige positie

Stap = 95 # Afstand in graden voor één stap.
Speed = 100 # Snelheid rijden

def Startpunt():
	# Startpunt zoeken
	grabber.run_timed(time_sp=1000, speed_sp=-100)
	up.run_forever(speed_sp=100)
	up.wait_until_not_moving()
	up.stop()
	up.run_to_rel_pos(position_sp=-5, speed_sp=100)
	up.wait_while('running')
	driveL.run_forever(speed_sp=100)
	driveR.run_forever(speed_sp=100)
	while touch.value() == 0:
		sleep(0.01)
	driveL.stop()
	driveR.stop()
	up.run_timed(time_sp=1000, speed_sp=-400)
	DrivePos = 0

def Scannen():
	Startpunt()
	for i in range(0,15):
		driveL.run_to_rel_pos(position_sp=-Stap, speed_sp=Speed)
		driveR.run_to_rel_pos(position_sp=-Stap, speed_sp=Speed)
		driveL.wait_while('running')
		driveR.wait_while('running')
		val = color.value()
		while val <= 1 or val >= 6:
			# Heen en weer bewegen om de kleur te herkennen.
			rand = random.randint(-3, 3)*5
			driveL.run_to_rel_pos(position_sp=10, speed_sp=100)
			driveR.run_to_rel_pos(position_sp=10, speed_sp=100)
			driveL.wait_while('running')
			driveR.wait_while('running')
			val = color.value()
			driveL.run_to_rel_pos(position_sp=-10, speed_sp=100)
			driveR.run_to_rel_pos(position_sp=-10, speed_sp=100)
			driveL.wait_while('running')
			driveR.wait_while('running')
		Balletjes.append(val)
	Startpunt()
	s = ""
	for i in range(1,16):
		s = s + str(Balletjes[i])
	print(s)
	sleep(5)

def Grab(dicht):
	if dicht:
		grabber.run_timed(time_sp=800, speed_sp=200)
		grabber.wait_while('running')
		up.run_timed(time_sp=500, speed_sp=400)
		up.wait_while('running')
	else:
		up.run_timed(time_sp=500, speed_sp=-300)
		up.wait_while('running')
		grabber.run_timed(time_sp=700, speed_sp=-200)
		grabber.wait_while('running')

def Verplaats(van, naar):
	global DrivePos
	if van == 0:
		driveL.run_forever(speed_sp=100)
		driveR.run_forever(speed_sp=100)
		while touch.value() == 0:
			sleep(0.01)
		driveL.stop()
		driveR.stop()
	elif van != DrivePos:
		dist = Stap * (van - DrivePos)
		driveL.run_to_rel_pos(position_sp=-dist, speed_sp=Speed)
		driveR.run_to_rel_pos(position_sp=-dist, speed_sp=Speed)
		driveL.wait_while('running')
		driveR.wait_while('running')
	DrivePos = van
	Grab(True)
	if naar == 0:
		driveL.run_forever(speed_sp=100)
		driveR.run_forever(speed_sp=100)
		while touch.value() == 0:
			sleep(0.01)
		driveL.stop()
		driveR.stop()
	else:
		dist = Stap * (naar - DrivePos)
		driveL.run_to_rel_pos(position_sp=-dist, speed_sp=Speed)
		driveR.run_to_rel_pos(position_sp=-dist, speed_sp=Speed)
		driveL.wait_while('running')
		driveR.wait_while('running')
	DrivePos = naar
	Grab(False)

def LEDS(colL, colR):
	if colL == 2:
		#Blauw
		Leds.set_color(Leds.LEFT, Leds.ORANGE, pct=0)
	elif colL == 3:
		#Groen
		Leds.set_color(Leds.LEFT, Leds.GREEN, pct=1)
	elif colL == 4:
		#Geel
		Leds.set_color(Leds.LEFT, Leds.YELLOW, pct=1)
	elif colL ==5:
		#Rood
		Leds.set_color(Leds.LEFT, Leds.RED, pct=1)
	
	if colR == 2:
		#Blauw
		Leds.set_color(Leds.RIGHT, Leds.ORANGE, pct=0)
	elif colR == 3:
		#Groen
		Leds.set_color(Leds.RIGHT, Leds.GREEN, pct=1)
	elif colR == 4:
		#Geel
		Leds.set_color(Leds.RIGHT, Leds.YELLOW, pct=1)
	elif colR ==5:
		#Rood
		Leds.set_color(Leds.RIGHT, Leds.RED, pct=1)

def Wissel(a,b):
	LEDS(Balletjes[a], Balletjes[b])
	print('wissel '+str(a)+' '+str(b))
	h = Balletjes[a]
	Verplaats(a,0)
	Balletjes[a] = Balletjes[b]
	Verplaats(b,a)
	Balletjes[b] = h
	Verplaats(0,b)


def SelSort():
	for i in range(1,15):
		k = i
		for j in range(i+1,16):
			col1 = Balletjes[j]
			col2 = Balletjes[k]
			print(str(j))
			if col1 < col2:
				k = j
		if i != k:
			Wissel(i,k)

def Sorteren():
	Scannen()
	driveL.run_to_rel_pos(position_sp=-100, speed_sp=100)
	driveR.run_to_rel_pos(position_sp=-100, speed_sp=100)
	SelSort()
	Startpunt()
	driveL.wait_while('running')
	driveR.wait_while('running')
	up.wait_while('running')
	grabber.wait_while('running')
	Sound.beep().wait()

Sorteren()