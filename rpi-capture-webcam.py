#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description : Capture d'images par webcam et envoi vers une base MySQL
# Copyright (C) 2016 Institut National de la Recherche Agronomique (INRA)
# Licence : GPL-3+
# Auteur : Cédric Goby
# Versioning : https://github.com/CedricGoby/rpi-capture-webcam

# Importation des modules nécessaires
import sys
import os
import grovepi
import MySQLdb
import time
# Importation de la fonction SendError depuis le fichier send__error.py
from send_error import SendError

# Nom de la base MySQL
__db_name ="db-name"
# Nom de la table
__db_table ="db-table"
# Fichier de connexion (contient : utilisateur MySQL, mot de passe, hôte MySQL)
__db_login_file ="db-login.cnf"
# Nom de l'hôte qui envoie les emails
__hostname ="hostname"
# Expéditeur des emails
__sender ="sender@provider.com"
# Destinataire des emails
__recipient ="recipient@provider.com"
# Serveur SMTP pour l'envoi des emails
__smtp_server ="smtp.provider.com"
# Nom du scipt
__file_name = os.path.basename(__file__)
# Date et heure
__datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
# Nom de l'image capturée
__image ="image.jpg"

# Lancement du processus d'acquisition
try:
	# Capture de l'image (execution d'une commande en bash)
	os.system('fswebcam -d /dev/video0 --delay 10 --skip 10 -p yuyv -r 800x600 --set sharpness=30% --set brightness=70% --no-banner --jpeg 95 image.jpg')
	# Connexion à la base MySQL : Timeout en secondes, Nom de la base de données MySQL, fichier d'options (user,password,host)
	con = MySQLdb.connect(connect_timeout=10,db=__db_name,read_default_file=__db_login_file)
	# Ouverture du fichier image au format binaire
	__binaryfile = open(__image, 'rb').read()
	# Création d'un "Cursor object" qui permettra d'exécuter n'importe quelle requête SQL
	cur = con.cursor()
	# Construction de la requête SQL
	sql = "INSERT INTO " + __db_table + " (date_insert, images) VALUES (%s, %s)"
	# Exécution de la requête SQL
	cur.execute(sql, (__datetime, __binaryfile))
	con.commit()
	# Fermeture de la connexion à la base MySQL
	con.close()

# Dans le cas d'une erreur MySQL
except MySQLdb.Error, e:
	try:
		# Récupération de l'erreur MySQL (l'erreur est connue)
		__error = ("Erreur MySQL [%d]: %s" % (e.args[0], e.args[1]))
		# Affichage de l'erreur
		print __error
	except IndexError:
		# Récupération de l'erreur MySQL (l'erreur est inconnue)
		__error =  ("Erreur MySQL: %s" % str(e))
		# Affichage de l'erreur
		print __error
	# Envoi de l'erreur par email avec la fonction SendError
	SendError(__error, __sender, __recipient, __hostname, __file_name, __smtp_server)

# Dans le cas d'une erreur autre qu'une erreur MySQL
except:
	__error = ("Erreur: %s" % sys.exc_info()[0])
	# Affichage de l'erreur
	print __error
	# Envoi de l'erreur par email avec la fonction SendError
	SendError(__error, __sender, __recipient, __hostname, __file_name, __smtp_server)
