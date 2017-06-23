#!/usr/bin/env python
# coding: utf-8

"""
Ce programme cree un serveur qui recoit les commandes de la caméra par protocole IP
Puis il verifie la bonne transmission de celles-ci 
Et enfin les transmets par protocole VISCA a la camera
"""

import socket, sys
import time
import serial

#Definition du port serie selon le protocole VISCA 
ser = serial.Serial(
	port='/dev/ttyAMA0',	#chemin du port serie de la Raspberry
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
 
#Definition des parametres de l'adresse du serveur
HOST = '192.168.0.111'
PORT = 11111

#création du socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#liaison du socket à une adresse précise
try:
	mySocket.bind((HOST, PORT))
except socket.error:
	print("La liaison du socket à l'adresse choisie a échoué.")
	sys.exit
 
while 1:
	#Attente de la requête de connexion d'un client
	print("Serveur prêt, en attente de requêtes ...")
	mySocket.listen(2)
	
	#Etablissement de la connexion
	connexion, adresse = mySocket.accept()
	print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))
	msgServeur ="Vous êtes connecté au serveur. Envoyez vos messages."
	
	#Dialogue avec le client
	connexion.send(msgServeur)
	msgClient = connexion.recv(1024)
	while 1:
		print("Commande recu: ", msgClient)
		if msgClient.upper() == "FIN" :
			break
		while msgClient != "Valide":	#test vérifiant la bonne réception de la commande
			commande = msgClient	#sauvegarde de la commande 
			connexion.send(commande)	#envoi de la commande recu au serveur
			
			msgClient = connexion.recv(1024)	#En attente de la confirmation du serveur, 
												#si la commande est bonne le message sera "Valide"
												#sinon la commande est renvoyé par le client
		ser.write(commande)	#transmission de la commande sur le port serie
		msgServeur = "Recu" #indication au client que qu'il peut continuer
		connexion.send(msgServeur)
		msgClient = connexion.recv(1024) #attente d'une nouvelle commande
		
	#Fermeture de la connexion avec le client
	connexion.send("fin")
	print("Connexion interrompue.")
	connexion.close()
