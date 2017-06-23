#!/usr/bin/env python
# coding: utf-8

"""Ce programme sert à initialiser la connexion Client-serveur entre les deux appareils notamment en permettant aux appareils de connaitre l'addresse ip du serveur
l'appareil est en écoute pour recevoir un message du serveur
une fois ce message recu l'appareil enregitrera l'addresse IP de l'émetteur puis renverra à l'émetteur un autre message contenant cette même addresse IP
Quand le message sera reçu par l'autre appareil il enregitrera cette addresse IP
Ainsi maintenant les deux appareils connaissent l'addresse IP de l'HOST"""

import socket, sys

HOST = '127.0.0.1' #init de la variable HOST par l'addresse locale
MDP = "motdepasse" # Définition du mot de passe

# Définition des paramètres de réception
addr = ('', 33333)  # host, port

# Creation du socket et connexion à l'addresse
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(addr)

# Réception du message de l'autre appareil
while 1:
	data, addr = UDPSock.recvfrom(1024)
	if data == MDP:
		print "Un serveur a été trouvé depuis l'addresse '%s'" %addr[0]
		HOST = addr[0]
		break

# Définition des paramètres d'émission
addr = (HOST, 33334)

# Envoi de l'addresse ip de l'host à l'host
UDPSock.sendto(HOST, addr) 

# Fermeture de la socket
UDPSock.close()

