# coding: utf8
# try something like

from pprint import pprint
from datetime import time
import datetime

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

    rows = db(db.PRODUCTO.ci_usu_creador==session.usuario['cedula']).select()
    detalles = {}
    cant_esp = 0
    cant_val = 0
    cant_rec = 0

    for row in rows:
        dict_campos = dict()
        campos = db((db.PRODUCTO_TIENE_CAMPO.id_campo == db.CAMPO.id_campo)
                    & (db.PRODUCTO_TIENE_CAMPO.id_producto == row.id_producto)).select()

        for campo in campos:
            dict_campos[campo.CAMPO.nombre] = campo.PRODUCTO_TIENE_CAMPO.valor_campo

        detalles[row] = dict_campos

        if row["estado"] == "En espera":
            cant_esp += 1
        elif row["estado"] == "Validada":
            cant_val += 1 
        elif row["estado"] == "Rechazada":
            cant_rec += 1


    # Para el modal de Agregar actividad
    programas = db(db.PROGRAMA).select('nombre')
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

    # Para la fecha maxima de realizacion
    now = datetime.datetime.now()
    if now.month < 10 :
        mes = "-0" +  str(now.month)
    else:
        mes = "-" +  str(now.month)
    if now.day < 10 :
        dia = "-0" +  str(now.day)
    else:
        dia = "-" +  str(now.month)
    fecha_max = str(now.year) + mes + dia

    # Lista de programas para listarlos en el select
    programas =  db(db.PROGRAMA).select(db.PROGRAMA.nombre,db.PROGRAMA.id_programa).as_list()
        

    formulario = SQLFORM(db.PRODUCTO)
    if formulario.process(session=None, formname='crear_tipo').accepted:
        print "se envio"
    elif formulario.errors:
        print "error"
        formulario.errors.fecha = T('mala fecha')
        print formulario.errors
    else:
        print "fatal"

    '''
    tipo =  request.vars.id_tipo
    posibles_campos = {'Fecha':'date', 'Telefono':'string', 'Texto Corto':'string','Documento':'upload', 'Numero Entero':'integer', 'Texto Largo':'text'}

    campos_id = db(db.ACT_POSEE_CAMPO.id_tipo_act == tipo).select()
    tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == tipo).select().first()
    nombre_actividad = tipo_actividad.nombre
    descripcion_actividad = tipo_actividad.descripcion



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
                            print fields
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
                                response.flash = 'el formulario tiene errores

                                '''

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
    rows = db(db.PRODUCTO_TIENE_CAMPO.id_producto == id_act).select()
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
    form.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    form.element(_type='submit')['_value']="Modificar"
    for i in range(len(valores)):
        setattr(form.vars, valores[i][0], valores[i][1])

    if form.process().accepted:

        for var in form.vars:
            campo = var.replace("_"," ")
            id_cam = db(db.CAMPO.nombre==campo).select().first().id_campo
            valor = getattr(form.vars ,var)

            sql = "UPDATE PRODUCTO_TIENE_CAMPO SET valor_campo = '" + str(valor)
            sql = sql + "' WHERE id_producto = '" + str(id_act) + "' AND id_campo = '" + str(id_cam) + "';"
            db.executesql(sql)

            update_act = "UPDATE PRODUCTO SET ci_usuario_modifica = '" + str(session.usuario['cedula'])
            update_act = update_act + "' WHERE id_producto = '" + str(id_act) + "';"
            db.executesql(update_act)

        redirect(URL('gestionar'))

    return locals()


def eliminar():
    id_act = int(request.args(0))


    set_tiene_campo = db(db.PRODUCTO_TIENE_CAMPO.id_producto == id_act)
    set_tiene_campo.delete()
    producto = db(db.PRODUCTO.id_producto == id_act)
    producto.delete()

    redirect(URL('gestionar'))

    #return "producto {} eliminada".format(producto)
    return locals()


# Funcion utilizada para el ajax en el agregar
def obtener_actividades():
    if request.vars.Programa=="":
        respuesta = "jQuery('#nombre_actividad').empty();"
        respuesta += "jQuery('#descripcion_actividad').empty();"
        respuesta += "jQuery('#campos_actividad').empty();"
        respuesta += "jQuery('#lista_tipos').empty()"

        return respuesta
    
    programa = db(db.PROGRAMA.nombre==request.vars.Programa).select().first()
    tiposA = db(db.TIPO_ACTIVIDAD.id_programa==programa.id_programa).select(db.TIPO_ACTIVIDAD.nombre,
        db.TIPO_ACTIVIDAD.id_tipo).as_list()
    
    concat = '<option></option>'

    for tipo in tiposA:

        concat += '<option value='+str(tipo['id_tipo'])+'>'+tipo['nombre']+'</option>'


    return "jQuery('#lista_tipos').empty().append('"+concat+"')"

# Funcion utilizada para el ajax cuando se elige la actividad para que aparezcan los campos
def seleccion_actividad():
    if request.vars.id_tipo=="":
        respuesta = "jQuery('#nombre_actividad').empty();"
        respuesta += "jQuery('#descripcion_actividad').empty();"
        respuesta += "jQuery('#campos_actividad').empty()"
        return respuesta

    tipo =  request.vars.id_tipo
    posibles_campos = {'Fecha':'date', 'Telefono':'string', 'Texto Corto':'string','Documento':'upload', 'Numero Entero':'integer', 'Texto Largo':'text'}

    campos_id = db(db.ACT_POSEE_CAMPO.id_tipo_act == tipo).select()
    tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == tipo).select().first()
    nombre_actividad = tipo_actividad.nombre
    descripcion_actividad = tipo_actividad.descripcion

    respuesta_inputs = ""

    for row in campos_id:

        rows_campo = db(db.CAMPO.id_campo == row.id_campo).select().first()
        nombre_campo = rows_campo.nombre
        nombre_campo_input = nombre_campo.replace(" ", "_").replace("-", "_")
        obligatorio_campo = rows_campo.obligatorio
        tipo_campo = rows_campo.tipo_campo
        es_obligatorio = ""

        if obligatorio_campo:
            nombre_campo += " (*)"
            es_obligatorio += " obligatorio"


        html_input = '<div class="form-group">'+\
                        '<label for="'+nombre_campo_input+'" class = "control-label col-sm-3">'+nombre_campo+'</label>'+\
                        '<div class="col-sm-8">'+\
                            '<input class="form-control input-'+posibles_campos[tipo_campo]+es_obligatorio+'" type="'+posibles_campos[tipo_campo]+'" name="'+nombre_campo_input+'"/>'+\
                        '</div>'+\
                    '</div>' 

        respuesta_inputs += html_input

            
    respuesta = "jQuery('#nombre_actividad').empty().append('"+nombre_actividad+"');"
    respuesta += "jQuery('#descripcion_actividad').empty().append('"+descripcion_actividad+"');"
    respuesta += "jQuery('#campos_actividad').empty().append('"+respuesta_inputs+"')"

    return respuesta