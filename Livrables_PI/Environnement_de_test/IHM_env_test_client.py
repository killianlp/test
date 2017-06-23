#!usr/bin/python
# -*- coding: utf-8 -*-
 
"""
Ce programme cree l'interface homme-machine du client qui recoit les debits de flux video envoyes mesurés par le serveur par protocole IP
Il permet soit de lancer un test, soit d'arreter le programme, 
soit d'arreter le programme et de fermer le serveur 
"""
 
import socket, sys
import mesure_debit
import env_test_client

#Definition des parametres de l'adresse du serveur 
HOST = '192.168.0.111'
PORT = 50000
 
reponse = str("O")	#initialisation pour lancer un test directement au premier lancement
 
while reponse.upper() == "O":
	env_test_client.comparer_mesures(HOST,PORT)
	reponse = raw_input("Refaire un test ? (<O>/<N>)\n")

#si "N": fin du programme et demande de fermeture du serveur
terminer = raw_input("Voulez-vous fermer le serveur ? (<O>/<N>)\n")
 
if terminer.upper() == "O": # Pour fermer le serveur
							#Reconnexion rapide au serveur pour lui demander de se fermer
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		mySocket.connect((HOST, PORT))
	except socket.error:
		sys.exit() 
 
	msgServeur = mySocket.recv(1024)
	mySocket.send("FINAL")
	print "Serveur fermé."
