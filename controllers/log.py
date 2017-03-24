# -*- coding: utf-8 -*-
'''
    Este controlador provee las funciones necesarias para la consulta del LOG.
'''
from funciones_siradex import get_tipo_usuario
from log import insertar_log
import StringIO

'''

'''
def consultar():
    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    formulario = formulario_descargar_log_periodo()

    if formulario.process(formname="formulario_descargar_log_periodo").accepted:
        periodo = request.vars.periodo
        if periodo == "Todo":
            redirect(URL(c ="log",f="download", args=[0]))
        elif periodo == "Hoy":
            redirect(URL(c ="log",f="download", args=[1]))
        elif periodo == "Semana pasada":
            redirect(URL(c ="log",f="download", args=[2]))
        elif periodo == "Mes pasado":
            redirect(URL(c ="log",f="download", args=[3]))
        elif periodo == "Hace 3 meses":
            redirect(URL(c ="log",f="download", args=[4]))

    #log_entries =  db().select(db.LOG_SIRADEX.ALL, orderby=~db.LOG_SIRADEX.id_log)

    if len(request.args):
        page=int(request.args[0])
    else:
        page=0

    items_per_page = 20

    limitby=(page*items_per_page,(page+1)*items_per_page+1)

    log_entries =  db().select(db.LOG_SIRADEX.ALL, orderby=~db.LOG_SIRADEX.id_log, limitby=limitby)
    return dict(admin=admin, log_entries = log_entries, formulario_periodo = formulario, \
                page=page,items_per_page=items_per_page)

def download():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    periodo = request.args[0]
    if periodo == "0":
        query = "SELECT * FROM LOG_SIRADEX;"
    elif periodo == "1":
        date = datetime.date.today()
        query = "SELECT * FROM LOG_SIRADEX WHERE accion_fecha = '" + str(date) + "';"
    elif periodo == "2":
        date = datetime.date.today() - datetime.timedelta(days=7)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion_fecha >= '" + str(date) + "';"
    elif periodo == "3":
        date = datetime.date.today() - datetime.timedelta(days=31)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion_fecha >= '" + str(date) + "';"
    elif periodo == "4":
        date = datetime.date.today() - datetime.timedelta(days=93)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion_fecha >= '" + str(date) + "';"

    insertar_log(db, 'LOG', datetime.datetime.now(), request.client, 'DESCARGA DE LOG', session.usuario['usbid'])

    #Excecute query
    rows = db.executesql(query, fields=db.LOG_SIRADEX)

    #convert query to csv
    tempfile = StringIO.StringIO()
    rows.export_to_csv_file(tempfile)
    response.headers['Content-Type'] = 'text/csv'
    attachment = 'attachment; filename="LOGSIRADEX.csv"'
    response.headers['Content-Disposition'] = attachment
    return tempfile.getvalue()

def formulario_descargar_log_periodo():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    # Genero formulario para los campos
    formulario = SQLFORM.factory(
                    Field('periodo',
                           requires = [IS_IN_SET(["Hoy", "Semana pasada", "Mes pasado", "Hace 3 meses", "Todo"], zero='Seleccione...', error_message="Debe seleccionar un periodo para descargar el Log.")],
                           widget = SQLFORM.widgets.options.widget),
                    labels = {'periodo'      : 'Periodo'},
                    submit_button='Descargar'
                   )

    return formulario

def graficas():

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))


    # Reistro de login la ultima semana.
    login_last_week = []
    for i in range(6,-1,-1):
        date = datetime.date.today() - datetime.timedelta(days=i)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion = 'LOGIN' AND descripcion = 'LOGIN SATISFACTORIO' AND accion_fecha = '" + str(date) + "';"
        rows = db.executesql(query, fields=db.LOG_SIRADEX)
        login_last_week.append([str(date), len(rows)])

    # Reistro de login trimestre
    login_last_trim = []
    sem = 12
    for i in range(84,0,-7):
        date  = datetime.date.today() - datetime.timedelta(days=i)
        date2 = datetime.date.today() - datetime.timedelta(days=i - 7)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion = 'LOGIN' AND descripcion = 'LOGIN SATISFACTORIO' AND accion_fecha BETWEEN '" + str(date) + "' AND '" + str(date2) + "';"
        rows = db.executesql(query, fields=db.LOG_SIRADEX)
        login_last_trim.append([sem, len(rows)])
        sem = sem - 1

    # Reistro de PRoductos la ultima semana.
    prod_last_week = []
    for i in range(6,-1,-1):
        date = datetime.date.today() - datetime.timedelta(days=i)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion = 'PRODUCTO' AND descripcion ~ 'NUEVO PRODUCTO' AND accion_fecha = '" + str(date) + "';"
        rows = db.executesql(query, fields=db.LOG_SIRADEX)
        prod_last_week.append([str(date), len(rows)])

    # Reistro de PRoductos trimestre
    prod_last_trim = []
    sem = 12
    for i in range(84,0,-7):
        date  = datetime.date.today() - datetime.timedelta(days=i)
        date2 = datetime.date.today() - datetime.timedelta(days=i - 7)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion = 'PRODUCTO' AND descripcion ~ 'NUEVO PRODUCTO' AND accion_fecha BETWEEN '" + str(date) + "' AND '" + str(date2) + "';"
        rows = db.executesql(query, fields=db.LOG_SIRADEX)
        prod_last_trim.append([sem, len(rows)])
        sem = sem - 1

    # Reistro de PRoductos trimestre
    # [rechazados, validados]
    apr_vs_rech = [0,0]
    sem = 12
    for i in range(84,0,-7):
        date  = datetime.date.today() - datetime.timedelta(days=i)
        date2 = datetime.date.today() - datetime.timedelta(days=i - 7)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion = 'VALIDACION' AND descripcion ~ 'NO VALIDADO' AND accion_fecha BETWEEN '" + str(date) + "' AND '" + str(date2) + "';"
        rows = db.executesql(query, fields=db.LOG_SIRADEX)
        apr_vs_rech[0] += len(rows)
        sem = sem - 1
    sem = 12
    for i in range(84,0,-7):
        date  = datetime.date.today() - datetime.timedelta(days=i)
        date2 = datetime.date.today() - datetime.timedelta(days=i - 7)
        query = "SELECT * FROM LOG_SIRADEX WHERE accion = 'VALIDACION' AND descripcion ~ 'VALIDADO' AND accion_fecha BETWEEN '" + str(date) + "' AND '" + str(date2) + "';"
        rows = db.executesql(query, fields=db.LOG_SIRADEX)
        apr_vs_rech[1] += len(rows)
        sem = sem - 1

    apr_vs_rech[1] = apr_vs_rech[1] - apr_vs_rech[0]

    return dict(admin=admin, login_last_week=login_last_week, login_last_trim=login_last_trim, prod_last_week=prod_last_week, prod_last_trim = prod_last_trim, apr_vs_rech=apr_vs_rech)
