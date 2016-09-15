#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: send_error.py
# Description : Fonction qui envoie l'erreur d'exécution du script par email
# Variables : _error : Erreur, _hostname : Hôte qui envoie l'email, _sender : expéditeur
# _recipient : destinataire, _file_name : nom du script en erreur, _smtp_server : serveur SMTP
# Licence : GNU General Public License, version 3 (GPL-3.0)

import smtplib
import email.utils
from email.mime.text import MIMEText

# Fonction SendError
def SendError(_error, _sender, _recipient, _hostname, _file_name, _smtp_server):
	# Création du message
	msg = MIMEText(_error)
	# Destinataire
	msg['To'] = email.utils.formataddr((_recipient, _recipient))
	# Expéditeur
	msg['From'] = email.utils.formataddr((_sender, _sender))
	# Sujet incluant le nom du script en erreur et le nom d'hôte
	msg['Subject'] = '[Erreur] - '+ _file_name +' - '+ _hostname
	# Connexion au serveur SMTP avec un timeout en secondes
	server = smtplib.SMTP(_smtp_server,timeout=60)
	# Affichage des messages de communication avec le serveur SMTP (Pour débogage)
	server.set_debuglevel(True)
	# Envoi du message (expéditeur, destinataire)
	try:
		server.sendmail(_recipient, [_recipient], msg.as_string())
	finally:
		server.quit()
	
