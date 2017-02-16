# -*- coding: utf-8 -*-
'''
    Este controlador provee las funciones necesarias para la consulta del LOG.
'''
from funciones_siradex import get_tipo_usuario
from log import insertar_log, download_logfile
import StringIO

'''

'''
def consultar():
    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    log_entries =  db().select(db.LOG_SIRADEX.ALL, orderby=~db.LOG_SIRADEX.id_log)

    formulario_periodo = formulario_descargar_log_periodo()

    if formulario_periodo.process(formname = "formulario_periodo").accepted:
        periodo = request.vars.periodo
        if periodo == "Hoy":
            download(None)


    return dict(admin=admin, log_entries = log_entries, formulario_periodo = formulario_periodo)

def download(query):

    insertar_log(db, 'LOG', datetime.datetime.now(), request.client, 'DESCARGA DE LOG', session.usuario['usbid'])

    # creamos el archivo con el backup
    rows = db.executesql("SELECT * FROM LOG_SIRADEX;", fields=db.LOG_SIRADEX)
    tempfile = StringIO.StringIO()
    rows.export_to_csv_file(tempfile)
    response.headers['Content-Type'] = 'text/csv'
    attachment = 'attachment; filename="LOGSIRADEx.csv"'
    response.headers['Content-Disposition'] = attachment
    return tempfile.getvalue()

def formulario_descargar_log_periodo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    # Genero formulario para los campos
    formulario = SQLFORM.factory(
                    Field('periodo',
                           requires = [IS_IN_SET(["Hoy", "Semana pasada", "Mes pasado", "Hace 3 meses", "Todo"], zero='Seleccione...', error_message="Debe seleccionar un periodo para el descargar el Log.")],
                           widget = SQLFORM.widgets.options.widget),
                    labels = {'periodo'      : 'Periodo'},
                    submit_button='Descargar'
                   )

    return formulario
