# -*- coding: utf-8 -*-
from notificaciones import *
from funciones_siradex import get_tipo_usuario,get_tipo_usuario_not_loged
from log import insertar_log
import pygal
from datetime  import date

# Funcion para busquedas publicas
def busqueda():
    print request.vars

    dictionary = {}
    for key in request.vars:
        dictionary[key] = request.vars[key]

    print dictionary


    admin = get_tipo_usuario_not_loged(session)
    try:
        sql = "SELECT prod.descripcion," + \
                     "prod.nombre," +\
                     "prod.id_tipo," +\
                     "prod.id_producto,"+\
                     "prod.fecha_realizacion,"+\
                     "p.id_programa,"+\
                     "p.nombre,"+\
                     "p.abreviacion"+\
                " FROM (( PRODUCTO AS prod INNER JOIN TIPO_ACTIVIDAD AS a ON prod.id_tipo=a.id_tipo)"+\
                     "INNER JOIN PROGRAMA AS p ON a.id_programa = p.id_programa) "+\
                " WHERE p.papelera=False "


        if (request.vars.Producto == ""):
            pass
        else:
            sql += "AND plainto_tsquery('english','"+request.vars.Producto+"') @@ to_tsvector('english',coalesce(prod.nombre,'') || ' '|| coalesce(prod.descripcion,''))"

        if request.vars.Programa != None and\
           request.vars.TipoActividad != None and\
           request.vars.fecha != None and\
           request.vars.Autor != None:


            # Anadimos el filtro del usuario
            if request.vars.Autor != "all":
                sql += " AND prod.usbid_usu_creador=\'" + request.vars.Autor + "\'"

            # Anadimos el filtro del tipo de actividad
            if request.vars.Programa != "all" and request.vars.TipoActividad == "all":
                sql += " AND p.id_programa=" + str(request.vars.Programa)

            elif request.vars.TipoActividad != "all":
                sql += " AND prod.id_tipo=\'" + str(request.vars.TipoActividad)+"'"

            # Anadimos el filtro de la fecha
            if request.vars.fecha != "":
                sql += " AND prod.fecha_realizacion <= '" + request.vars.fecha +"'"

        if request.vars.anio != None:
            sql += " AND extract(year FROM prod.fecha_realizacion)=" + request.vars.anio

        # Ahora dependiendo del usuario anadimos las restricciones del estado (no se contempla cuando
        # el usuario esta bloqueado porqu no deberia llegar aqui)
        if (session.usuario == None or session.usuario["tipo"] == "Usuario"):
            sql += " AND prod.estado=\'Validado\';"
        elif (session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador"):
            sql += ";"

        print "\nsql"
        print sql
        productos = db.executesql(sql)
        print "\nLo resultante"
        print productos

        infoTabla = tabla(productos)
        infoBarChart = graficaBar(productos)

        infoPieChart = graficaPie(productos)
        #graficaPie = URL(c='busq_val',f='graficaPie',vars=dict(productos=productos))

        return locals()
    except:

        return locals()

# Mostrar productos
def ver_producto():

    admin = get_tipo_usuario_not_loged(session)
    if not request.args:
        raise HTTP(404)
    id_producto = int(request.args(0))
    producto = db(db.PRODUCTO.id_producto == id_producto).select().first()
    usuario_producto = db(db.USUARIO.usbid == producto.usbid_usu_creador).select().first()
    usuario_nombre = usuario_producto.nombres + " " + usuario_producto.apellidos
    tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == producto.id_tipo).select().first()
    programa_nombre = db(db.PROGRAMA.id_programa == tipo_actividad.id_programa).select().first().nombre

    #Obtenemos el nombre de los autores
    nombres_autores  = usuario_nombre #Primer autor siempre es el creador.
    autores = db(db.PARTICIPA_PRODUCTO.id_producto == id_producto).select()

    for autor in autores:
      autorAux = db(db.USUARIO.usbid == autor.usbid_usuario).select().first()
      nombres_autores  = nombres_autores + ', ' + autorAux.nombres +' '+ autorAux.apellidos

    query = "SELECT id_comprobante, descripcion FROM COMPROBANTE WHERE producto="+str(id_producto)+";"
    comprobantes = db.executesql(query)

    form = SQLFORM.factory(
            Field("Nombre_Producto", default=producto.nombre,writable = False),
            Field('Descripcion',default=producto.descripcion,writable = False),
            Field('Fecha_de_Relizacion', default=producto.fecha_realizacion,writable=False),
            Field('Lugar', default=producto.lugar,writable=False),
            readonly=True,
            labels = {'Descripcion' : 'Descripción',
                            'Fecha_de_Relizacion' : 'Fecha de Realización'})

    #Agregamos los otros elementos de los campos
    campos = db(db.PRODUCTO_TIENE_CAMPO.id_prod == producto.id_producto).select()

    hayDoc = False
    elementos = []
    documento= []
    for campo_valor in campos:
        campo = db(db.CAMPO.id_campo == campo_valor.id_campo).select().first()
        nombre_campo = campo.nombre_interno
        label_campo = campo.nombre
        nombre_campo = nombre_campo.replace(" ", "_")

        try :
            if int(nombre_campo[0]):
                nombre_campo = "campo_"+nombre_campo
        except:
            pass

        if campo.tipo_campo=="Documento":
            hayDoc = True
            temp=[campo.id_campo,campo_valor.valor_campo, nombre_campo,campo_valor.id_prod,label_campo]
            documento += [temp]
        else :
            if campo_valor.valor_campo!='' and  campo_valor.valor_campo!=None :
                elementos.append(Field(nombre_campo, label=label_campo, default=campo_valor.valor_campo, writable=False))
            else:
                elementos.append(Field(nombre_campo, label=label_campo, default="-- Información no proporcionada --", writable=False))

    if len(elementos) != 0:
        form_datos = SQLFORM.factory(*elementos, readonly=True)

    form_validado = SQLFORM(
            db.PRODUCTO,
            fields=['nombre'],
            labels={'nombre':'Nuevo nombre'},
            col3={'nombre':'Este es el nombre que aparecerá al momento de exportar las actividades'}

    )
    form_validado.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    form_validado.element(_type='submit')['_value']="Actualizar"



    ## Formulario para colocar la razon de rechazo de un producto.
    formulario_validar = SQLFORM.factory(
                          Field('nombre','string',
                                    requires=[IS_NOT_EMPTY(error_message="El nombre del producto no puede quedar vacío."),
                                              IS_LENGTH(50, error_message="El nombre del producto no puede superar los 50 caracteres.")]),
                          Field('id_producto',type="string"),
                          submit_button = 'Validar',
                          labels = {'nombre' : 'Nuevo Nombre'})

    formulario_validar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_validar.element(_type='submit')['_value']="Validar"

    ## Formulario para colocar la razon de rechazo de un producto.
    formulario_rechazar = SQLFORM.factory(
                          Field('razon', type="text"),
                          Field('id_producto_r', type="string", default=""),
                          submit_button = 'Agregar',
                          labels = {'razon' : 'Razón de Rechazo del Producto'})

    formulario_rechazar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_rechazar.element(_type='submit')['_value']="Rechazar"

    hayErrores = {}

    if formulario_validar.accepts(request.vars, session, formname="formulario_validar"):
        id_producto = request.vars.id_producto
        nuevo_nombre = request.vars.nombre

        #Actualizamos el nombre del producto
        db.PRODUCTO[id_producto] = dict(nombre = nuevo_nombre)
        #Validamos el producto
        validar(id_producto)
    else:
        hayErrores = formulario_validar.errors

    if formulario_rechazar.accepts(request.vars, session, formname="formulario_rechazar"):
        print "se rechazo"
        print request.vars
        id_producto = request.vars.id_producto_r
        razon = request.vars.razon

        ## Enviamos notificacion de rechazo
        # obtenemos el producto a rehazar
        producto =  db(db.PRODUCTO.id_producto == id_producto).select().first()
        print producto
        # obtenemos el usuario que realizo el producto
        usuario = db(db.USUARIO.usbid == producto.usbid_usu_creador).select().first()

        print usuario
        # parseamos los datos para la notificacion
        datos_usuario = {'nombres' : usuario.nombres + ' ' + usuario.apellidos}
        datos_usuario['correo_inst'] = usuario.correo_inst
        datos_usuario['correo_alter'] = None
        if usuario.correo_alter != None:
            if usuario.correo_alter != "":
                datos_usuario['correo_alter'] = usuario.correo_alter
            datos_usuario['correo_alter'] = usuario.correo_alter

        producto = {'nombre': producto.nombre}

        # enviamos la notificacion
        print "enviar correo"
        enviar_correo_rechazo(mail, datos_usuario, producto, razon)
        print "se envio el correo"
        # rechazamos efectimavamente el producto.
        print "llamando a rechazar"
        rechazar(id_producto)

    ## Fin formulario de rechazo

    return locals()

# Vista de validaciones
def gestionar_validacion():
    session.message=""
    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))


    # Hago el query Espera

    sqlValidadas = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='Validado';"
    sqlEspera = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='Por Validar';"
    sqlRechazadas = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='No Validado';"
    productosV = db.executesql(sqlValidadas)
    productosE = db.executesql(sqlEspera)
    productosR = db.executesql(sqlRechazadas)

    return locals()

# Metodo para validar un producto
def validar(id_producto):

    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(url)

    db(db.PRODUCTO.id_producto == id_producto).update(estado='Validado')
    insertar_log(db, 'VALIDACION', datetime.datetime.now(), request.client, 'PRODUCTO CON ID ' + str(id_producto) + ' VALIDADO', session.usuario['usbid'])

    ## INICIO NOTIFICACION ##

    # obtenemos el producto a validar
    producto =  db(db.PRODUCTO.id_producto == id_producto).select().first()

    # obtenemos el usuario que realizo el producto
    usuario = db(db.USUARIO.usbid == producto.usbid_usu_creador).select().first()

    # parseamos los datos para la notificacion
    datos_usuario = {'nombres' : usuario.nombres + ' ' + usuario.apellidos}
    datos_usuario['correo_inst'] = usuario.correo_inst
    datos_usuario['correo_alter'] = None
    if usuario.correo_alter != None:
        datos_usuario['correo_alter'] = usuario.correo_alter


    producto = {'nombre': producto.nombre}

    # enviamos la notificacion al usuario creador
    enviar_correo_validacion(mail,datos_usuario, producto)

    # enviamos notificacion a los coautores (si existen)
    participaciones = db(db.PARTICIPA_PRODUCTO.id_producto == id_producto).select()
    for participacion in participaciones:
        #obtenemos el coautor
        usuario = db(db.USUARIO.usbid == participacion.usbid_usuario).select().first()

        datos_coautor = {'nombres' : usuario.nombres + ' ' + usuario.apellidos }
        datos_coautor['correo_inst'] = usuario.correo_inst
        datos_coautor['correo_alter'] = None
        if usuario.correo_alter != None:
            datos_coautor['correo_alter'] = usuario.correo_alter
        # Enviamos el correo.
        enviar_correo_validacion_coautor(mail, datos_coautor, datos_usuario, producto)

    ## FIN NOTIFICACION ##

    session.message = 'Producto validado exitosamente'
    redirect(URL('gestionar_validacion.html'))

# Metodo para rechazar una producto
def rechazar(id_producto):
    print "entre a rechazar"
    admin = get_tipo_usuario(session)

    if (admin==0):
        redirect(URL(c ="default",f="index"))

    db(db.PRODUCTO.id_producto == id_producto).update(estado='No Validado')
    insertar_log(db, 'VALIDACION', datetime.datetime.now(), request.client, 'PRODUCTO CON ID ' + str(id_producto) + ' NO VALIDADO', session.usuario['usbid'])
    session.message = 'Producto rechazado'
    print "\n\n\nA redirigir en rechazar"
    redirect(URL('gestionar_validacion.html'))

def graficaPie(productos):
    pie_chart = pygal.Pie()

    if productos == None:
        return pie_chart.render()

    programas = {}

    if type(productos) is str:

        total_productos = 1
        id_programa = productos.split('\'')[4].split(',')[-2]
        nombre = productos.split('\'')[-4]
        abrev = productos.split('\'')[-2]
        programas[id_programa] = {'id':id_programa,'nombre':nombre,'abreviacion':abrev,'repeticiones':1}

    else:
        total_productos = len(productos)

        for producto in productos:
            id_programa = producto[5]
            try:
                programas[id_programa]['repeticiones'] += 1
            except:
                nombre = producto[6]
                abrev = producto[7]
                programas[id_programa] = {'id':id_programa,'nombre':nombre,'abreviacion':abrev,'repeticiones':1}


    for key in programas:
        porcentaje = (programas[key]['repeticiones']*100)//total_productos
        pie_chart.add(programas[key]['abreviacion'],[{'value':porcentaje, 'label':programas[key]['nombre']}])

    return programas

def graficaBar(productos):
    fecha_hasta = date.today().year
    fecha_desde = fecha_hasta - 10
    fechas={}
    programas = db(db.PROGRAMA['papelera']==False).select().as_list()

    for fecha in range(fecha_desde, fecha_hasta + 1):
        fechas[fecha]={}
        for programa in programas:
            ident = int(programa['id_programa'])
            nombre = programa['nombre']
            abrev = programa['abreviacion']
            fechas[fecha][ident]= {'nombre':nombre, 'abreviacion':abrev, 'repeticiones':0}

    for producto in productos:
        anio = producto[4].year
        if anio < fecha_desde:
            anio = fecha_desde
        if anio > fecha_hasta:
            anio = fecha_hasta
        id_programa = producto[5]
        fechas[anio][id_programa]['repeticiones'] += 1
    return fechas

def tabla(productos):

    fecha_hasta = date.today().year
    fecha_desde = fecha_hasta - 10
    programas={}
    programas_db = db(db.PROGRAMA['papelera']==False).select().as_list()

    for programa in programas_db:
        ident = int(programa['id_programa'])
        programas[ident]={'nombre':programa['nombre']}
        for fecha in range(fecha_desde, fecha_hasta + 1):
            programas[ident][fecha]= 0
        programas[ident]['total']=0

    for producto in productos:
        anio = producto[4].year
        if anio < fecha_desde:
            anio = fecha_desde
        if anio > fecha_hasta:
            anio = fecha_hasta
        id_programa = producto[5]
        programas[id_programa][anio]+= 1
        programas[id_programa]['total']+=1
    return programas



def eliminar():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

    archivo = request.args[0]
    comando = "rm ./applications/SiraDex/backup/" + archivo
    resp = os.system(comando)
    redirect(URL('index'))
