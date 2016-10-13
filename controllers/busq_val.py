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
    ''''
    formulario = SQLFORM(db.PRODUCTO,id_act)
    if formulario.process(session=None, formname='validar_producto').accepted:
        print "se envio"
        redirect(URL('gestionar_validacion'))
    elif formulario.errors:
        print "error"
        print formulario.errors
    else:
        print "fatal"
    '''
    db(db.PRODUCTO.id_producto == id_act).update(estado='Validada')
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
    db(db.PRODUCTO.id_producto == id_act).update(estado='Rechazada')
    session.message = 'Producto rechazado'
    redirect(URL('gestionar_validacion.html'))
