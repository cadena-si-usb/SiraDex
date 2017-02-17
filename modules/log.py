# -*- coding: utf-8 -*-
'''
    Insersión y descarga del log en la base de datos.
'''
from gluon import current
import os

def insertar_log(db, accion, fecha, ip, descripcion, usbid_usuario):
     db.LOG_SIRADEX.insert(
        accion = accion,
        accion_fecha = fecha,
        accion_ip = ip,
        descripcion = descripcion,
        usbid_usuario = usbid_usuario
     )
