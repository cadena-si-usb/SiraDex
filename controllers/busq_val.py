# -*- coding: utf-8 -*-
from notificaciones import *

# Funcion para busquedas publicas
def busqueda():


    if request.vars.Programa == "all" and request.vars.TipoActividad == "all":
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor + "%\') AND estado=\'Validada\';"

        productos = db.executesql(sql)

    elif request.vars.Programa != "all" and request.vars.TipoActividad == "all":
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor\
         + "%\') AND id_tipo IN (SELECT id_tipo FROM TIPO_ACTIVIDAD WHERE id_programa=" + request.vars.Programa + ") AND estado=\'Validada\';"

        productos = db.executesql(sql)

    elif request.vars.Programa == "all" and request.vars.TipoActividad != "all":
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor\
         + "%\') AND id_tipo=\'" + request.vars.TipoActividad + "\' AND estado=\'Validada\';"

        productos = db.executesql(sql)

    else:
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor\
         + "%\') AND id_tipo IN (SELECT id_tipo FROM TIPO_ACTIVIDAD WHERE id_programa=" + request.vars.Programa\
         + ") AND id_tipo=\'" + request.vars.TipoActividad + "\' AND estado=\'Validada\';"

        productos = db.executesql(sql)
    return locals()

# Mostrar productos
def ver_producto():
  if session.usuario != None:
    if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
      if(session.usuario["tipo"] == "DEX"):
        admin = 2
      elif(session.usuario["tipo"] == "Administrador"):
        admin = 1
      else:
        admin = 0
    else:
      redirect(URL(c ="default",f="vMenuPrincipal"))
  else:
    redirect(URL(c ="default",f="index"))

  id_producto = int(request.args(0))
  producto = db(db.PRODUCTO.id_producto == id_producto).select().first()
  usuario_producto = db(db.USUARIO.ci == producto.ci_usu_creador).select().first()
  usuario_nombre = usuario_producto.nombres + " " + usuario_producto.apellidos
  tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == producto.id_tipo).select().first()
  programa_nombre = db(db.PROGRAMA.id_programa == tipo_actividad.id_programa).select().first().nombre


  form = SQLFORM.factory(
            Field("Nombre_Producto", default=producto.nombre,writable = False),
            Field('Descripcion',default=producto.descripcion,writable = False),
            Field('Fecha_de_Relaizacion', default=producto.fecha_realizacion,writable=False),
            Field('Lugar', default=producto.lugar,writable=False),
            readonly=True)

  #Agregamos los otros elementos de los campos
  campos = db(db.PRODUCTO_TIENE_CAMPO.id_prod == producto.id_producto).select()

  elementos = []
  for campo_valor in campos:
    campo = db(db.CAMPO.id_campo == campo_valor.id_campo).select().first()
    nombre_campo = campo.nombre
    nombre_campo = nombre_campo.replace(" ", "_")
    try :
      if int(nombre_campo[0]):
        nombre_campo = "campo_"+nombre_campo
    except:
      pass

    elementos.append(Field(nombre_campo, default=campo_valor.valor_campo, writable=False))

  if len(elementos) != 0:
    form_datos = SQLFORM.factory(*elementos, readonly=True)

  form_validado = SQLFORM(
            db.PRODUCTO,
            fields=['nombre'],
            labels={'nombre':'Nuevo nombre'},
            col3={'nombre':'Este es el nombre que aparecera al momento de exportar las actividades'}

  )
  form_validado.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
  form_validado.element(_type='submit')['_value']="Actualizar"



  ## Formulario para colocar la razon de rechazo de un producto.
  formulario_validar = SQLFORM.factory(
                          Field('nombre','string',
                                    requires=[IS_NOT_EMPTY(error_message="El nombre del producto no puede quedar vacio."),
                                              IS_LENGTH(50, error_message="El nombre del producto no puede superar los 50 caracteres.")]),
                          Field('id_producto',type="string"),
                          submit_button = 'Validar',
                          labels = {'nombre' : 'Nuevo Nombre'})

  ## Formulario para colocar la razon de rechazo de un producto.
  formulario_rechazar = SQLFORM.factory(
                          Field('razon', type="text"),
                          Field('id_producto', type="string", default=""),
                          submit_button = 'Agregar',
                          labels = {'razon' : 'Razón de Rechazo del Producto'})

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
      id_producto = request.vars.id_producto
      razon = request.vars.razon

      ## Enviamos notificacion de rechazo
      # obtenemos el producto a rehazar
      producto =  db(db.PRODUCTO.id_producto == id_producto).select().first()

      # obtenemos el usuario que realizo el producto
      usuario = db(db.USUARIO.ci == producto.ci_usu_creador).select().first()

      # parseamos los datos para la notificacion
      datos_usuario = {'nombres' : usuario.nombres}
      if usuario.correo_alter != None:
          datos_usuario['email'] = usuario.correo_alter
      else:
          datos_usuario['email'] = usuario.correo_inst

      producto = {'nombre': producto.nombre}

      # enviamos la notificacion
      enviar_correo_rechazo(mail, datos_usuario, producto, razon)

      # rechazamos efectimavamente el producto.
      rechazar(id_producto)


  ## Fin formulario de rechazo

  return locals()

# Vista de validaciones
def gestionar_validacion():

    if session.usuario != None:
        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))


    # Hago el query Espera

    sqlValidadas = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='Validada';"
    sqlEspera = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='En espera';"
    sqlRechazadas = "select producto.id_producto, producto.nombre, tipo_actividad.nombre from producto inner join tipo_actividad"\
    + " on producto.id_tipo=tipo_actividad.id_tipo where producto.estado='Rechazada';"
    productosV= db.executesql(sqlValidadas)
    productosE = db.executesql(sqlEspera)
    productosR = db.executesql(sqlRechazadas)

    return locals()

# Metodo para validar un producto
def validar(id_producto):

    db(db.PRODUCTO.id_producto == id_producto).update(estado='Validada')

    ## INICIO NOTIFICACION ##

    # obtenemos el producto a validar
    producto =  db(db.PRODUCTO.id_producto == id_producto).select().first()

    # obtenemos el usuario que realizo el producto
    usuario = db(db.USUARIO.ci == producto.ci_usu_creador).select().first()

    # parseamos los datos para la notificacion
    datos_usuario = {'nombres' : usuario.nombres}
    if usuario.correo_alter != None:
        datos_usuario['email'] = usuario.correo_alter
    else:
        datos_usuario['email'] = usuario.correo_inst

    producto = {'nombre': producto.nombre}

    # enviamos la notificacion
    enviar_correo_validacion(mail,datos_usuario, producto)

    ## FIN NOTIFICACION ##

    session.message = 'Producto validado exitosamente'
    redirect(URL('gestionar_validacion.html'))

# Metodo para rechazar una producto
def rechazar(id_producto):
    db(db.PRODUCTO.id_producto == id_producto).update(estado='Rechazada')
    session.message = 'Producto rechazado'
    redirect(URL('gestionar_validacion.html'))
