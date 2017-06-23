#!usr/bin/python
# -*- coding: utf-8 -*-
 
"""
Ce programme cree un client qui recoit les debits de flux video envoyes mesurés par le serveur par protocole IP
Il mesure en meme temps les debits de flux video recus et permet de choisir le nombre de mesures
Il enregistre ces valeurs dans des listes et affiche ensuite un graphe permettant la comparaison entre les deux
 
Le programme nécessite l'installation de python-matplotlib:
	sudo apt-get install python-matplotlib
"""
 
import socket, sys
import matplotlib.pyplot as plt
import mesure_debit
 
NB_VAL = int(5) #Nombre de test que a faire
 
def comparer_mesures(HOST,PORT):

	#initialisation des differentes variables
	liste_debitemis = []
	liste_debitrecu = []
	i = int(0)
 
	NB_VAL = input("Combien de valeurs désirez-vous mesurer ? ")
 
	#Création du socket
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#Envoi d'une requête de connexion au serveur :
	try:
		mySocket.connect((HOST, PORT))
	except socket.error:
		print "La connexion a échoué."
		sys.exit()	
	print "Connexion établie avec le serveur."	
 
	#Dialogue avec le serveur
	msgServeur = mySocket.recv(1024)
	print msgServeur
	mySocket.send("Mesure(s) restantes:")	
	liste_debitrecu.append(mesure_debit.ledebit("rx"))
	msgServeur = mySocket.recv(1024)
 
	while (i<NB_VAL-1):  #determine le nombre de valeurs restantes
		liste_debitemis.append(msgServeur)
		i+=1
		mySocket.send(str(NB_VAL-i))	#Cet envoi permet l'affichage d'un  decompte du nombre de valeurs restatntes au serveur
										#mais surtout la synchronisation des deux mesures de débit
		print str(NB_VAL-i)         	#indique au client le nb de mesures restantes
		liste_debitrecu.append(mesure_debit.ledebit("rx"))
		msgServeur = mySocket.recv(1024)
	liste_debitemis.append(msgServeur)
 
	#Fin de la transmission
	mySocket.send("FIN")
	msgServeur = mySocket.recv(1024)
	print msgServeur
 
	#Affichage brut des resultats dans la console
	print "Emis: ", liste_debitemis, '\n', "Recu :", liste_debitrecu
 
	#Création et affichage des courbes de comparaison
	plt.grid(True)
	plt.title("Debits")
	plt.plot(range(0,5*NB_VAL,5),liste_debitemis,'g',label="Debit emis")
	plt.plot(range(0,5*NB_VAL,5),liste_debitrecu,'r',label="Debit recu")
	plt.ylabel('Debit en Mbps')
	plt.xlabel('Temps en s')
	plt.legend()
	plt.show()
	#Une fois que le graphe est ferme le client est redirige vers l'IHM 
