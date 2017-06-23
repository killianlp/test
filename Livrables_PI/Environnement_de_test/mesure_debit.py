#!usr/bin/python
# -*- coding: utf-8 -*-
 
"""
Ce programme propose une fonction permetant de mesurer le debit entrant ou sortant sur un port de l'appareil
L'execution necessite l'installation de vnstat:
	sudo apt-get install vnstat
"""

import os
 
#La fonction retourne la valeur du debit voulue.  
def ledebit(mot):   #mot = tx pour le debit transmis 
					#rx pour le debit recu
	ch = str()
	ch2 = str()
	i = int(0)
	a = int(0)
	test_debit = os.popen("vnstat -i eth0 -tr","r").read()  #écriture du résultat de la commande affichant les valeurs du debit sur les 5 dernière secondes dans un fichier
															#eth0 correspond au nom du port que l'on veut surveiller
															#pour voir les differents ports disponibles dans le terminal: ifconfig
	nb = test_debit.find(mot)
	nb +=2  #on se place apres le mot
 
	#Boucle pour se placer au niveau de la valeur voulue
	while(test_debit[nb] == " "):
		nb += 1
	debut = nb
 
	#Boucle pour recuperer tous les chiffres voulus
	while( test_debit[nb]!=" "):
        	
		if(test_debit[nb]==","): #pour eviter les erreurs de conversions pour les flotants changement de la virgule en point
			ch += "."
			a = nb - debut  	#nb de chiffre avant la virgule, utile si une conversion est necessaire
		else:
			ch += test_debit[nb]	#ecriture des chiffres un a un
		nb+=1
 
	#conversion en Mbps si necessaire et exprimation du resultat en Mbps
	if(test_debit[nb]=="k" and a==3):
		ch2="0."
		for i in range (a) :
			ch2 = ch2 + ch[i]
		ch2 = ch2 + ch[a+1]
		ch2 = ch2 + ch[a+2]
		return ch2
		
	elif(test_debit[nb]=="k" and a==2):
		ch2="0.0"
		for i in range (a) :
			ch2 = ch2 + ch[i]
		ch2 = ch2 + ch[a+1]
		ch2 = ch2 + ch[a+2]
		return ch2
 
	elif(test_debit[nb]=="k" and a==1):
		ch2="0.00"
		for i in range (a) :
			ch2 = ch2 + ch[i]
		ch2 = ch2 + ch[a+1]
		ch2 = ch2 + ch[a+2]
		return ch2
 
	else :
		return ch
