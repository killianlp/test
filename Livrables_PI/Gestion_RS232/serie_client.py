#!/usr/bin/env python
# coding: utf-8

"""
Ce programme cree un client qui envoi les commandes de la caméra par protocole IP
et verifie la bonne transmission de celles-ci
"""

import socket, sys

#Definition des parametres de l'adresse du serveur
HOST = '192.168.0.111'
PORT = 11111

#création du socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Envoi d'une requête de connexion au serveur 
try:
  mySocket.connect((HOST, PORT))
except socket.error:
  print("La connexion a échoué.")
  sys.exit()
print("Connexion établie avec le serveur.")

#Dialogue avec le serveur
msgServeur = mySocket.recv(1024)
 
while 1:
	if msgServeur.upper() == "FIN":
		break
	print(msgServeur)
	msgClient = raw_input("Commande: ")
	msgServeur = "raz"	#Remise a zero du message
						#permet le bon deroulement du test qui suit
						
	while msgServeur != msgClient:	#test vérifiant la bonne réception de la commande
									#compare la commande envoye par le client et la commande recu par le serveur 
									#si elle sont differentes la commande est renvoye
		mySocket.send(str(msgClient))	
		msgServeur = mySocket.recv(1024)
		
	mySocket.send("Valide")	#Validation de la bonne reception
	msgServeur = mySocket.recv(1024) #confirmation de la reception par le client
 
#Fin de la transmission
print("Connexion interrompue.")
mySocket.close()
