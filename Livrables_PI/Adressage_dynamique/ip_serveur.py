#!/usr/bin/env python
# coding: utf-8

"""Ce programme sert à initialiser la connexion Client-serveur entre les deux appareils notamment en permettant aux appareils de connaitre l'addresse ip du serveur
le multithreading est utilisé, un thread pour la reception de message et un autre pour l'émission
le thread d'émission envoie à toutes les addresses disponibles (broadcast) un message pour signaler sa présence
d'un autre coté un appareil sera en écoute et recevra ce message
une fois ce message recu cet appareil enregitrera l'addresse IP de l'émetteur puis renverra à l'émetteur un autre message contenant cette même addresse IP
Quand le message sera reçu l'appareil enregitrera cette addresse IP et fermera les threads
Ainsi maintenant les deux appareils connaissent l'addresse IP de l'HOST"""

HOST = '127.0.0.1'	#init de la variable HOST par l'addresse locale
MDP = "motdepasse"	#def mot de passe 

addr_tx = ('<broadcast>', 33333)	# address broadcast, port Emission
addr_rx = ('', 33334)  # host, port reception

import socket, threading, time, sys

#thread gérant la réception des messages
class ThreadReception(threading.Thread): 
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.UDPSock_rx = conn           # réf. du socket de connexion
        
	def run(self):
		while 1:
			data, addr_rx = UDPSock_rx.recvfrom(1024)
			HOST = data
			break

		# Le thread réception se termine ici.
		# On force la fermeture du thread émission :
		th_E._Thread__stop()
		print "Appareil trouvé à l'addresse '%s'" %addr_rx[0]
		self.UDPSock_rx.close()
		print "Votre addresse IP : '%s'" %HOST
		
#objet thread gérant l'émission des messages 
class ThreadEmission(threading.Thread):
	
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.UDPSock_tx = conn           # réf. du socket de connexion
        
	def run(self):
		while 1:
			UDPSock_tx.sendto(MDP, addr_tx)
			time.sleep(30)
		


# Programme principal - Établissement des connexions :

# Creation socket envoi
UDPSock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
UDPSock_tx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Creation socket et connexion à l'addresse de reception
UDPSock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock_rx.bind(addr_rx)

            
# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(UDPSock_tx)
th_R = ThreadReception(UDPSock_rx)
th_E.start()
th_R.start() 

#Attente de la fermeture des threads
th_E.join()
th_R.join()

print "Lancement réussi et terminé"
