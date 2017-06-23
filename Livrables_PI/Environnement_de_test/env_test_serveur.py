#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Ce programme cree un serveur qui envoit les debits du flux video envoye au client par protocole IP
"""

import socket, sys
import mesure_debit

#Definition des parametres de l'adresse du serveur
HOST = '192.168.0.111'
PORT = 50000
 
#création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#liaison du socket à une adresse précise :
try:
	mySocket.bind((HOST, PORT))
except socket.error:
	print "La liaison du socket à l'adresse choisie a échoué."
	sys.exit()
 
while 1:
	#Attente de la requête de connexion d'un client
	print "Serveur prêt, en attente de requêtes ..."
	mySocket.listen(5)
	
	#Etablissement de la connexion
	connexion, adresse = mySocket.accept()
	print "Client connecté, adresse IP %s, port %s\n" % (adresse[0], adresse[1])
	
	#Dialogue avec le client
	connexion.send("Vous êtes connecté au serveur. Début des mesures...\n\nMesure(s) restantes:")
	msgClient = connexion.recv(1024)
	while 1:
		print msgClient
		if msgClient.upper() == "FIN" or msgClient.upper() == "FINAL":
			testfin = msgClient
			break
		connexion.send(mesure_debit.ledebit("tx"))
		msgClient = connexion.recv(1024)
 
	#Fermeture de la connexion avec le client:
	connexion.send("Fin des mesures\n")
	print "Connexion interrompue."
	connexion.close()
 
	#Fermeture du programme:
	if testfin == "FINAL":
		break
