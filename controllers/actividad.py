# coding: utf8
# try something like

from pprint import pprint
from datetime import time

def gestionar():
    if session.usuario != None:
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0
    else:
        redirect(URL(c ="default",f="index"))

    rows = db(db.ACTIVIDAD.ci_usuario_crea==session.usuario['cedula']).select()
    detalles = {}
    cant_esp = 0
    cant_val = 0
    cant_rec = 0

    for row in rows:
        dict_campos = dict()
        campos = db((db.TIENE_CAMPO.id_campo == db.CAMPO.id_campo)
                    & (db.TIENE_CAMPO.id_actividad == row.id_actividad)).select()

        for campo in campos:
            dict_campos[campo.CAMPO.nombre] = campo.TIENE_CAMPO.valor_campo

        detalles[row] = dict_campos

        if row["validacion"] == "En espera":
            cant_esp += 1
        elif row["validacion"] == "Validada":
            cant_val += 1 
        elif row["validacion"] == "Rechazada":
            cant_rec += 1

    return locals()

def tipos():
    if session.usuario != None:
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0
    else:
        redirect(URL(c ="default",f="index"))

    rows = db(db.TIPO_ACTIVIDAD.papelera=='False').select()
    return locals()


def agregar():
    if session.usuario != None:
    	if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
	else:
		admin = 0
    else:
        redirect(URL(c ="default",f="index"))

    tipo = int(request.args(0))
    rows = db(db.ACT_POSEE_CAMPO.id_tipo_act == tipo).select()
    nombre_tipo = db(db.TIPO_ACTIVIDAD.id_tipo == tipo).select().first().nombre
    fields = []
    for row in rows:
        rows_campo = db(db.CAMPO.id_campo == row.id_campo).select().first()
        nombre = rows_campo.nombre
        print nombre
        print "hola"
        nombre = nombre.replace(" ", "_")
        obligatorio = rows_campo.obligatorio
        tipo_campo = ''
        tipo_campo = rows_campo.lista
# tipo_campos = ['fecha', 'participante', 'ci', 'comunidad', 'telefono', 'texto','documento', 'cantidad entera', 'cantidad decimal']
        if obligatorio:
            if tipo_campo in   ['fecha']:             fields.append(Field(nombre,'date',requires=[IS_NOT_EMPTY(),IS_DATE(format=T('%Y-%m-%d'),error_message='Fecha invalida, debe ser: AAA-MM-DD')]))
            elif tipo_campo in ['participante,texto']:fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(error_message='Inserte texto')]))
            elif tipo_campo in ['ci']:                fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_MATCH('\d{2}.\d{3}.\d{3}$', error_message='CI invalida, debe ser: XX.XXX.XXX')]))
            elif tipo_campo in ['comunidad']:         fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY()]))
            elif tipo_campo in ['documento']:         fields.append(Field(nombre,'upload',uploadfolder=URL('static/archivos'),requires=[IS_NOT_EMPTY(error_message='Debe subirse un archivo')]))
            elif tipo_campo in ['telefono']:          fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_MATCH('\(0\d{3}\)\d{3}-\d{2}-\d{2}$', error_message='Telefeno invalido, debe ser: (0xxx)xxx-xx-xx')]))
            elif tipo_campo in ['cantidad entera']:   fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(-9223372036854775800, 9223372036854775807)]))
            elif tipo_campo in ['cantidad decimal']:  fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_DECIMAL_IN_RANGE(-9223372036854775800, 9223372036854775807, dot=".",error_message='El numero debe ser de la forma X.X, donde X esta entre -9223372036854775800 y 9223372036854775807')]))
        else:
            if tipo_campo in   ['fecha']:             fields.append(Field(nombre,'date',requires=IS_EMPTY_OR(IS_DATE(format=T('%Y-%m-%d'),error_message='Fecha invalida, debe ser: AAA-MM-DD'))))
            elif tipo_campo in ['participante,texto']:fields.append(Field(nombre,'string'))
            elif tipo_campo in ['ci']:                fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_MATCH('\d{2}.\d{3}.\d{3}$',error_message='CI invalida, debe ser: XX.XXX.XXX'))))
            elif tipo_campo in ['comunidad']:         fields.append(Field(nombre,'string'))
            elif tipo_campo in ['documento']:         fields.append(Field(nombre,'upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME()),uploadfolder=URL('static/archivos')))
            elif tipo_campo in ['telefono']:          fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_MATCH('\(0\d{3}\)\d{3}-\d{2}-\d{2}$', error_message='Telefeno invalido, debe ser: (0xxx)xxx-xx-xx'))))
            elif tipo_campo in ['cantidad entera']:   fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_INT_IN_RANGE(-9000000000000000000, 9000000000000000000,error_message='Numero muy grande o muy pequeno'))))
            elif tipo_campo in ['cantidad decimal']:  fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_DECIMAL_IN_RANGE(-9000000000000000000, 9000000000000000000, dot=".",error_message='El numero debe ser de la forma X.X, donde X esta entre -+9000000000000000000'))))

    #fields.append(Field(nombre,requires=IS_IN_SET([(1,'Method1'), (2,'Method2'), (3,'Method3')], zero='Select')))

    form=SQLFORM.factory(*fields)

    if form.process().accepted:
        dicc_act = db.ACTIVIDAD.insert(id_tipo = tipo,ci_usuario_crea= session.usuario['cedula'])
        id_act = dicc_act['id_actividad']
        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.CAMPO.nombre==campo).select().first().id_campo
            valor = getattr(form.vars ,var)
            db.TIENE_CAMPO.insert(id_actividad=id_act,id_campo=id_cam,valor_campo= valor)
        redirect(URL('gestionar'))
    elif form.errors:
        response.flash = 'el formulario tiene errores'

    return locals()

def modificar():
    if session.usuario != None:
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0
    else:
        redirect(URL(c ="default",f="index"))

    id_act = int(request.args(0))
    rows = db(db.TIENE_CAMPO.id_actividad == id_act).select()
    fields = []
    valores = []
    for row in rows:
        rows_campo = db(db.CAMPO.id_campo == row.id_campo).select().first()
        nombre = rows_campo.nombre
        nombre = nombre.replace(" ", "_")
        obligatorio = rows_campo.obligatorio
        tipo_campo = ''
        tipo_campo = rows_campo.lista
# tipo_campos = ['fecha', 'participante', 'ci', 'comunidad', 'telefono', 'texto','documento', 'cantidad entera', 'cantidad decimal']
        if obligatorio:
            if tipo_campo in   ['fecha']:             fields.append(Field(nombre,'date',requires=[IS_NOT_EMPTY(),IS_DATE(format=T('%Y-%m-%d'),error_message='Fecha invalida, debe ser: AAA-MM-DD')]))
            elif tipo_campo in ['participante,texto']:fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(error_message='Inserte texto')]))
            elif tipo_campo in ['ci']:                fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_MATCH('\d{2}.\d{3}.\d{3}$', error_message='CI invalida, debe ser: XX.XXX.XXX')]))
            elif tipo_campo in ['comunidad']:         fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY()]))
            elif tipo_campo in ['documento']:         fields.append(Field(nombre,'upload',uploadfolder=URL('static/archivos'),requires=[IS_NOT_EMPTY(error_message='Debe subirse un archivo')]))
            elif tipo_campo in ['telefono']:          fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_MATCH('\(0\d{3}\)\d{3}-\d{2}-\d{2}$', error_message='Telefeno invalido, debe ser: (0xxx)xxx-xx-xx')]))
            elif tipo_campo in ['cantidad entera']:   fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(-9223372036854775800, 9223372036854775807)]))
            elif tipo_campo in ['cantidad decimal']:  fields.append(Field(nombre,'string',requires=[IS_NOT_EMPTY(),IS_DECIMAL_IN_RANGE(-9223372036854775800, 9223372036854775807, dot=".",error_message='El numero debe ser de la forma X.X, donde X esta entre -9223372036854775800 y 9223372036854775807')]))
        else:
            if tipo_campo in   ['fecha']:             fields.append(Field(nombre,'date',requires=IS_EMPTY_OR(IS_DATE(format=T('%Y-%m-%d'),error_message='Fecha invalida, debe ser: AAA-MM-DD'))))
            elif tipo_campo in ['participante,texto']:fields.append(Field(nombre,'string'))
            elif tipo_campo in ['ci']:                fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_MATCH('\d{2}.\d{3}.\d{3}$',error_message='CI invalida, debe ser: XX.XXX.XXX'))))
            elif tipo_campo in ['comunidad']:         fields.append(Field(nombre,'string'))
            elif tipo_campo in ['documento']:         fields.append(Field(nombre,'upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME()),uploadfolder=URL('static/archivos')))
            elif tipo_campo in ['telefono']:          fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_MATCH('\(0\d{3}\)\d{3}-\d{2}-\d{2}$', error_message='Telefeno invalido, debe ser: (0xxx)xxx-xx-xx'))))
            elif tipo_campo in ['cantidad entera']:   fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_INT_IN_RANGE(-9000000000000000000, 9000000000000000000,error_message='Numero muy grande o muy pequeno'))))
            elif tipo_campo in ['cantidad decimal']:  fields.append(Field(nombre,'string',requires=IS_EMPTY_OR(IS_DECIMAL_IN_RANGE(-9000000000000000000, 9000000000000000000, dot=".",error_message='El numero debe ser de la forma X.X, donde X esta entre -+9000000000000000000'))))


        valores.append([nombre,row.valor_campo])

    form=SQLFORM.factory(*fields)

    for i in range(len(valores)):
        setattr(form.vars, valores[i][0], valores[i][1])

    if form.process().accepted:

        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.CAMPO.nombre==campo).select().first().id_campo
            valor = getattr(form.vars ,var)

            sql = "UPDATE TIENE_CAMPO SET valor_campo = '" + str(valor)
            sql = sql + "' WHERE id_actividad = '" + str(id_act) + "' AND id_campo = '" + str(id_cam) + "';"
            db.executesql(sql)

            update_act = "UPDATE ACTIVIDAD SET ci_usuario_modifica = '" + str(session.usuario['cedula'])
            update_act = update_act + "' WHERE id_actividad = '" + str(id_act) + "';"
            db.executesql(update_act)

        redirect(URL('gestionar'))

    return locals()


def eliminar():
    id_act = int(request.args(0))

    set_tiene_campo = db(db.TIENE_CAMPO.id_actividad == id_act)
    set_tiene_campo.delete()
    actividad = db(db.ACTIVIDAD.id_actividad == id_act)
    actividad.delete()

    redirect(URL('gestionar'))

    #return "Actividad {} eliminada".format(actividad)
    return locals()
