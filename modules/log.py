# -*- coding: utf-8 -*-
'''
    Insersión y descarga del log en la base de datos.
'''
from gluon import current
import os

    # Field('accion',type='string'), #En el schema aparece como TEXT, investigar diferencias.
    # Field('accion_fecha',type='date'),
    # Field('accion_ip',type='string', length=256),
    # Field('descripcion',type='string'),
    # Field('usbid_usuario',db.USUARIO.usbid),

def insertar_log(db, accion, fecha, ip, descripcion, usbid_usuario):
     db.LOG_SIRADEX.insert(
        accion = accion,
        accion_fecha = fecha,
        accion_ip = ip,
        descripcion = descripcion,
        usbid_usuario = usbid_usuario
     )

def download_logfile(db):
    pass
