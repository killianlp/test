#!/usr/bin/env python

"""
Ce programme sert à lire le port série du PC selon le protocole VISCA
"""

import time
import serial

#Definition du port serie selon le protocole VISCA 
ser = serial.Serial(
	port='/dev/ttyS0',	#chemin du port serie de l'ordinateur
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

while 1:
	commande=ser.readline()	#lecture des donnees
	if commande.upper() == "STOP":	#test pour l'arret du programme 
		break
	elif commande != '':	#sinon on écrit la commande
		print commande
