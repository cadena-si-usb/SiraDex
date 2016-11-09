# -*- coding: utf-8 -*-
'''
  Define funciones generales, disponibles para todos los controladoes.
'''
# from gluon import *

# def get_tipo_usuario():

#     # Session Actual
#     print("Usuario:-->"+session.usuario["tipo"])
#     session = current.session
#     if session.usuario != None:
#         if session.usuario["tipo"] == "Bloqueado":
#             redirect(URL(c = "default",f="index"))
#         if session.usuario["tipo"] == "Administrador":
#             if(session.usuario["tipo"] == "DEX"):
#                 admin = 2
#             elif(session.usuario["tipo"] == "Administrador"):
#                 admin = 1
#             elif(session.usuario["tipo"] == "Bloqueado"):
#                 admin = -1
#             else:
#                 admin = 0
#         else:
#             redirect(URL(c ="default",f="perfil"))
#     else:
#         redirect(URL(c ="default",f="index"))

#     return admin
