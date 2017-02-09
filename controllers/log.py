# -*- coding: utf-8 -*-
'''
    Este controlador provee las funciones necesarias para la consulta del LOG.
'''
from funciones_siradex import get_tipo_usuario
from log import download_logfile
import StringIO

def consultar():
    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    log_entries =  db().select(db.LOG_SIRADEX.ALL)

    return dict(admin=admin, log_entries = log_entries)

def download():

    # creamos el archivo con el backup
    rows = db.executesql('SELECT * FROM LOG_SIRADEX;', fields=db.LOG_SIRADEX)
    tempfile = StringIO.StringIO()
    rows.export_to_csv_file(tempfile)
    response.headers['Content-Type'] = 'text/csv'
    attachment = 'attachment; filename="LOGSIRADEX.csv"'
    response.headers['Content-Disposition'] = attachment
    return tempfile.getvalue()
