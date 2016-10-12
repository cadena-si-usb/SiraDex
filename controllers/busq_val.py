# Funcion para busquedas publicas
def busqueda():
    if request.vars.Programa == "all" and request.vars.TipoActividad == "all":
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor + "%\');" 

        productos = db.executesql(sql)

    elif request.vars.Programa != "all" and request.vars.TipoActividad == "all":
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor\
         + "%\') AND id_tipo IN (SELECT id_tipo FROM TIPO_ACTIVIDAD WHERE id_programa=" + request.vars.Programa + ");"

        productos = db.executesql(sql)

    elif request.vars.Programa == "all" and request.vars.TipoActividad != "all":
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor\
         + "%\') AND id_tipo=\'" + request.vars.TipoActividad + "\';" 

        productos = db.executesql(sql)

    else:
        sql = "SELECT nombre FROM PRODUCTO WHERE nombre LIKE \'%" + request.vars.Producto \
         + "%\' AND ci_usu_creador IN (SELECT ci FROM usuario WHERE nombres LIKE \'%" + request.vars.Autor\
         + "%\') AND id_tipo IN (SELECT id_tipo FROM TIPO_ACTIVIDAD WHERE id_programa=" + request.vars.Programa\
         + ") AND id_tipo=\'" + request.vars.TipoActividad + "\' ;"

        productos = db.executesql(sql)

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


    # Hago el query
    query = reduce(lambda a, b: (a&b),[db.PRODUCTO.validacion == 'En espera',
                                       db.PRODUCTO.id_tipo == db.TIPO_ACTIVIDAD.id_tipo
                                       ]
                  )
    # Muestro los ids y nombres de las actividades a validar o rechazar
    aux = db(query).select(db.PRODUCTO.id_producto, db.PRODUCTO.id_tipo
                         )
    aux1 = db(query).select(db.TIPO_ACTIVIDAD.nombre, db.TIPO_ACTIVIDAD.id_tipo
                         )

    return dict(tipos = aux1, productos = aux, admin = admin)

# Metodo para validar un producto
def validar():
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

    id_act = int(request.args[0])
    db(db.PRODUCTO.id_producto == id_act).update(validacion='Validada')
    session.message = 'Producto validado exitosamente'
    redirect(URL('gestionar_validacion.html'))

# Metodo para rechazar una producto
def rechazar():
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

    id_act = int(request.args[0])
    db(db.PRODUCTO.id_producto == id_act).update(validacion='Rechazada')
    session.message = 'Producto rechazado'
    redirect(URL('gestionar_validacion.html'))
