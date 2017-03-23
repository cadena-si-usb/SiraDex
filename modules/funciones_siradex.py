# -*- coding: utf-8 -*-
'''
  Define funciones generales, disponibles para todos los controladoes.
'''
from gluon import *
import math



# No en python3
def convertToNumber(s):
    return int(s.encode('hex'), 16)

def get_tipo_usuario(session):

    # Session Actual
    
    if session.usuario != None:

        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL(c = "default",f="index"))

        elif(session.usuario["tipo"] == "DEX"):
            admin = 2
        
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        
        elif (session.usuario["tipo"] == "Usuario"):
            admin = 0
        
        else:
            redirect(URL(c ="default",f="index"))

        
    else:
        redirect(URL(c ="default",f="index"))
        #admin = -1

    return admin

def get_tipo_usuario_not_loged(session):

    # Session Actual
    #print("Usuario:-->"+session.usuario["tipo"])
    #session = current.session
    if session.usuario != None:

        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL(c = "default",f="index"))

        elif(session.usuario["tipo"] == "DEX"):
            admin = 2
        
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        
        elif (session.usuario["tipo"] == "Usuario"):
            admin = 0
        
    else:
        #redirect(URL(c ="default",f="index"))
        admin = -1

    return admin
    