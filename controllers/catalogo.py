# -*- coding: utf-8 -*-
from funciones_siradex import get_tipo_usuario

'''
Funcion que se encarga de obtener los datos para mostrar los catalogos
que existen en el sistema.
'''
def vGestionarCatalogo():
    # Obtengo el tipo del usuario para permitir el acceso a la visa
    # Limpio el Session del sistema.
    admin = get_tipo_usuario()
    session.nombreMostrar = ""
    session.nombreModificar = ""
    message = session.message
    session.message = ""
    # Se obtienen los nombres de todos los catalogos y se pasan al html.
    aux = db(db.CATALOGO).select(db.CATALOGO.nombre, db.CATALOGO.id_catalogo)
    return dict(admin = admin, catalogos = aux, message = message)

'''
Funcion que se encarga de agregar un catalogo a la
lista de catalogos existentes, en caso de que no exista
uno con el mismo nombre, se encarga de crearlo y almacenarlo
en la base de datos.
'''
def vAgregarCatalogo():
    # Se obtiene el tipo de usuario.
    admin = get_tipo_usuario()
    # Se crea un formulario para introducir un nombre
    formulario = SQLFORM.factory(
                        Field('nombre',
                              requires = [IS_NOT_EMPTY(error_message='El nombre del catalogo no puede quedar vacio.'),
                                          IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del catalogo no puede iniciar con numeros."),
                                          IS_NOT_IN_DB(db, 'CATALOGO.nombre', error_message="Ya existe un catalogo con ese nombre.")]),
                              submit_button='Agregar',
                              labels={'nombre':'Nombre'})

    if formulario.accepts(request.vars, session):
        # Creamos el catalogo y obtenemos su id, para pasarlo al controlador de agregar campo.
        id_catalogo = db.CATALOGO.insert(nombre = request.vars.nombre)['id_catalogo']
        redirect(URL('vAgregarCampos.html',args=[id_catalogo]))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en el Formulario.'
    else:
        session.message = ''

    return(dict(formulario = formulario, admin = admin))

'''
Funcion que se encarga de agregar un campo al catalogo,
crearlo y relacionarlo con el catalogo indicado.
'''
def vAgregarCampos():

    admin = get_tipo_usuario()
    
    # Obtengo el id del catalogo
    id_cat = request.args[0]
    
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese catalogo
    queryCamposAgregados = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_cat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(queryCamposAgregados).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL,db.CATALOGO.ALL)
    # Busco el id del catalogo
    # Genero formulario para los campos
    formulario = SQLFORM(db.CAMPO_CATALOGO,
                   submit_button='Agregar',
                   fields = ['nombre', 'tipo_cat', 'eliminar'],
                   labels = {'tipo_cat' : 'Tipo'}
                   )
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el campo al catalogo en caso de que no exista.
        idd_campo = db(db.CAMPO_CATALOGO.nombre == request.vars.nombre).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        queryCamposConMismoNombre = reduce(lambda a, b: (a&b), [db.CATALOGO_TIENE_CAMPO.id_campo_cat == idd_campo,
                                             db.CATALOGO_TIENE_CAMPO.id_catalogo == id_cat])
        if len(db(queryCamposConMismoNombre).select())>0:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vAgregarCampos', args=[id_cat]))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Datos invalidos'
    else:
        if(not(session.msgErr)):
            session.message = ''
    
    return dict(formulario = formulario, campos_guardados = campos_guardados,admin = admin)

'''
Funcion auxiliar que se encarga de colocar
el mensaje de exito.
'''
def agregarTipoAux():
    session.message = 'Catalogo agregado exitosamente'
    redirect(URL('vGestionarCatalogo.html'))


'''
Funcion auxiliar que se encarga de colocar
el mensaje de exito.
'''
def agregarTipoAux2():
    session.message = 'Catalogo editado exitosamente'
    redirect(URL('vGestionarCatalogo.html'))

'''
Funcion que se encarga de eliminar un catalogo, los campos
que este posee y todas las relaciones entre ellos.
'''
def eliminarCampos():
    # Obtengo el id o nombre del Catalogo
    if len(request.args)!=0:
        nombreCat = request.args[0]
        subQueryCatalogoActual = (db.CATALOGO.id_catalogo == nombreCat)
    else:
        nombreCat = session.catAgregar
        subQueryCatalogoActual = (db.CATALOGO.nombreCat == nombreCat)
    # Construyo query para obtener la relacion entre los campos y el catalogo
    # que debo eliminar
    queryCamposDelCatalogo = reduce(lambda a, b: (a&b),[subQueryCatalogoActual,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    
    # Guardo los resultados en 'aux'
    camposDelCatalogo = db(queryCamposDelCatalogo).select(db.CATALOGO_TIENE_CAMPO.ALL)
    
    # Borro las relaciones (en caso de que hayan)
    if(len(camposDelCatalogo) > 0):
        camposDeActividad = db(db.CAMPO.despliega_cat == camposDelCatalogo[0].id_catalogo).select()
        #Se borran los campos del catalogo
        db(db.VALORES_CAMPO_CATALOGO.id_catalogo == camposDelCatalogo[0].id_catalogo).delete()
        #Si una actividad esta asociada a un catalogo
        if(len(camposDeActividad) >0):
            #Se elimina la relación con la actividad
            db(db.ACT_POSEE_CAMPO.id_campo == camposDeActividad[0]['id_campo']).delete()
        #Se elimina la relacion entre los campos y el catalogo
        db(db.CATALOGO_TIENE_CAMPO.id_catalogo == camposDelCatalogo[0].id_catalogo).delete()
        #Se eliminan los campos asociados a las actividades
        db(db.CAMPO.despliega_cat == camposDelCatalogo[0].id_catalogo).delete()
    
    # Borro los campos asociados a estas relaciones
    for row in camposDelCatalogo:
        queryCampo = db.CAMPO_CATALOGO.id_campo_cat == row.id_campo_cat
        campoCatalogo = db(queryCampo).select(db.CAMPO_CATALOGO.ALL)
        db(db.CAMPO_CATALOGO.id_campo_cat == campoCatalogo[0].id_campo_cat).delete()
    
    
    # Borro el catalogo
    db(subQueryCatalogoActual).delete()
    
    redirect(URL('vGestionarCatalogo.html'))

'''
Funcion que se encarga de agregar valores a los
campos de un catalogo, en caso de que no exista
otra instancia con el mismo valor.
'''
def vAgregarElementoCampo():
    # Obtengo el tipo del usuario y el id del catalogo.
    admin = get_tipo_usuario()
    id_catalogo = request.args[0]
    # Busco los campos asociados al catalogo.
    queryCamposCatalogo = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    nombresCamposCatalogo = db(queryCamposCatalogo).select(db.CAMPO_CATALOGO.nombre)
    # Creo 2 arreglos para almacenar los campos y los id de cada campo.
    campos = []
    idsCampos = []
    # Nombres de los campos
    for row in nombresCamposCatalogo:
        campos.append(row['nombre'])
    
    arrIdCamposCatalogo = db(queryCamposCatalogo).select(db.CAMPO_CATALOGO.id_campo_cat)
    cantidadCampos = len(campos)
    # Obtengo los ids de los campos
    for row in arrIdCamposCatalogo:
        idsCampos.append(row['id_campo_cat'])
    # Creo un arreglo con todos los campos del formulario.
    arregloCampos = []
    for i in range (0,len(campos)):
        arregloCampos += [ Field("pr"+str(i),'string', label=T(str(campos[i]))) ]
    if(len(arregloCampos) > 0):
        formulario = SQLFORM.factory(
            *arregloCampos)
    else:
        session.message = "El catalogo no posee campos"
        redirect(URL('vGestionarCatalogo.html'))
    
    if len(request.vars)>0:
        for i in range(0, cantidadCampos):
            valor = request.vars["pr"+str(i)]
    
            # Genero un query para revisar si el valor existe en alguna instancia del campo.
            queryValorDuplicado = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_catalogo,
                                                 db.VALORES_CAMPO_CATALOGO.id_campo_cat == idsCampos[i]])
            if(len(db(queryValorDuplicado).select()) > 0):
                session.nombreMostrar = id_catalogo
                session.message = "El valor de un campo esta duplicado"
                redirect(URL('vMostrarCatalogo.html'))
    
        # Almaceno los valores en cada uno de los campos
        for i in range(0, cantidadCampos):
            valor = request.vars["pr"+str(i)]
            db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = idsCampos[i], id_catalogo = id_catalogo, valor = valor)
        session.nombreMostrar = id_catalogo
        redirect(URL('vMostrarCatalogo.html'))
    
    return (dict(formulario = formulario, admin = admin))

'''
Funcion encargada de mostrar todas las instancias
de los campos de un catalogo en una tabla.
'''
def vMostrarCatalogo():
    admin = get_tipo_usuario()
    # Obtengo el nombre del catalogo a mostrar
    if(session.nombreMostrar != ""):
        id_catalogo = session.nombreMostrar
    else:
        id_catalogo = request.args[0]
    
    # Creo 2 queries para buscar los campos que contiene el catalogo
    # y los valores de cada uno de ellos.
    queryCamposCatalogo = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    queryValoresCampos = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
                                       db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                       db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])
    
    # Guardo los resultados del los queries creados
    campos_guardados = db(queryCamposCatalogo).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL)
    id_campos = db(queryCamposCatalogo).select(db.CATALOGO_TIENE_CAMPO.ALL)
    valores_campos = db(queryValoresCampos).select(db.VALORES_CAMPO_CATALOGO.ALL)
    nroCampos = len(campos_guardados)
    nroValores = len(valores_campos)
    
    # Calculo el numero de filas que debera mostrar la tabla.
    if(nroCampos != 0):
        nroFilas = nroValores/nroCampos
    else:
        nroFilas = 0
    
    # Arreglos auxiliares para almacenar las filas y las columnas de la tabla
    filasCatalogo = []
    columnasCatalogo = []
    j = 0
    # Creo las columnas de la tabla (Los valores de cada campo)
    for i in range(0,len(id_campos)):
        arregloValoresCampo = []
        idCampoCatalogo = id_campos[i]['id_campo_cat']
        for j in range(0,len(valores_campos)):
            if(valores_campos[j]['id_campo_cat'] == idCampoCatalogo):
                arregloValoresCampo.append(valores_campos[j])
        columnasCatalogo.append(arregloValoresCampo)
    j = 0
    # Creo las filas que se mostraran en la tabla.
    for i in range(0,nroFilas):
        aux = []
        for j in range(0,len(columnasCatalogo)):
            aux.append(columnasCatalogo[j][i])
        filasCatalogo.insert(-1,aux)
    # Guardo las filas globalmente para poder acceder a ellas de forma sencilla y eficiente.
    session.filas = filasCatalogo
    nombre = db(db.CATALOGO.id_catalogo == id_catalogo).select(db.CATALOGO.nombre)
    return dict(campos_guardados = campos_guardados,filas = filasCatalogo, admin = admin, nombre = id_catalogo)

'''
Funcion que se encarga de modificar el valor de una
instancia de los campos de un catalogo.
'''
def vModificarCampos():
    # Obtengo el tipo de usuario y el id del campo a modificar.
    admin = get_tipo_usuario()
    id_campo = request.args[0]
    # Busco el diccionario al cual esta asociado la fila de campos que deseo modificar.
    for j in session.filas[int(request.args[1])]:
        if str(j['id_campo_cat'])==id_campo:
            diccionario = j
            dcc = session.filas[int(request.args[1])]
    # Creo un query para sacar los campos que tiene el catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    # Guardo los resultados del query en aux
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    id_catalogo= db(query).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    # Arreglos auxiliares para guardar los nombres y ids de los campos respectivamente.
    cmpo = []
    ids = []
    # Nombres de los campos
    for row in aux:
        cmpo.append(row['nombre'])

    id_cat = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0]['id_catalogo']
    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)

    # Ids de los campos
    for row in arrId:
        ids.append(row['id_campo_cat'])
    arreglo = []
    df =None
    # Almaceno los campos a mostrar en el formulario
    for i in range(0,len(cmpo)):
        for f in dcc:
            if(f['id_campo_cat'] == ids[i]):
                df = f['valor']
        if df != None:
            arreglo += [ Field("pr"+str(i),'string',default= df, label=T(str(cmpo[i]))) ]
    forma = SQLFORM.factory(
        *arreglo)
    # Reviso si ningun valor esta duplicado para luego insertarlo en la base.
    if len(request.vars)>0:
        for i in range(0,len(cmpo)):
            for f in dcc:
                if(f['id_campo_cat'] == ids[i]):
                    df = f['valor']
            valor = request.vars["pr"+str(i)]
            if(valor != df):
                query2 = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_cat,
                                                     db.VALORES_CAMPO_CATALOGO.id_campo_cat == ids[i]])
                if(len(db(query2).select()) > 0):
                    session.nombreMostrar = id_catalogo
                    session.message = "El valor de un campo esta duplicado"
                    redirect(URL('vMostrarCatalogo.html'))
        for i in range(0,len(cmpo)):
            for f in dcc:
                if(f['id_campo_cat'] == ids[i]):
                    df = f['valor']
            valor = request.vars["pr"+str(i)]
            db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
            db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = ids[i], id_catalogo = id_cat, valor = valor)
        session.nombreMostrar = id_catalogo
        redirect(URL('vMostrarCatalogo.html'))
    return (dict(forma = forma, admin = admin))

'''
Funcion que se encarga de eliminar una instancia
de los campos de un catalogo.
'''
def eliminarValorCampo():
    # Obtengo el tipo del usuario y el nombre del campo a eliminar.
    admin = get_tipo_usuario()
    id_campo = request.args[0]
    valor = request.args[1]
    for dic in session.filas:
        for i in dic:
            if (str(i['id_campo_cat'])==id_campo) and (str(i['valor']) == valor):
                diccionario = i
                dcc = dic

    # Genero un query para buscar los campos que tiene el catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
                                       db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    # Arreglos auxiliares para guardar los campos y los ids respectivamente.
    cmpo = []
    ids = []
    # Nombres de los campos
    for row in aux:
        cmpo.append(row['nombre'])

    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)

    # Ids de los campos
    for row in arrId:
        ids.append(row['id_campo_cat'])
    # Voy eliminando el valor de cada campo de la fila seleccionada
    for i in range(0,len(cmpo)):
        for f in dcc:
            if(f['id_campo_cat'] == ids[i]):
                df = f['valor']

        db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
    session.nombreMostrar = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0].id_catalogo
    redirect(URL('vMostrarCatalogo.html'))

'''
Funcion que se encarga de modificar un catalogo
permitiendo agregar o eliminar campos del mismo.
'''
def vModificarCatalogo():
    # Obtengo el tipo del usuario conectado.
    admin = get_tipo_usuario()
    # Obtengo el nombre del catalogo a modificar.
    if(session.nombreModificar != ""):
        nombreCat = session.nombreModificar
    else:
        nombreCat = request.args[0]
        valorStr = ""
        for i in range(0,len(request.args[0])):
            if(request.args[0][i] == "_"):
                valorStr += " "
            else:
                valorStr += request.args[0][i]
        #nombreCat = valorStr

    # Creo 2 querys para buscar los valores de los campos y los campos que hay en el catalogo.
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo  == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    query2 = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo  == nombreCat,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                      db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                      db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])

    # Guardo los resultados de dichos queries
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO.ALL)
    valores = db(query2).select(db.VALORES_CAMPO_CATALOGO.ALL)
    campos = db(query).select(db.CAMPO_CATALOGO.ALL)

    if(len(campos) > 0):
        total = len(valores)/len(campos)
    else:
        total = 0
    # Busco el id del catalogo
    id_cat = db(db.CATALOGO.id_catalogo  == nombreCat).select()[0].id_catalogo

    # Genero formulario para los campos
    form = SQLFORM(db.CAMPO_CATALOGO,
                   submit_button='Agregar',
                   fields = ['nombre', 'tipo_cat', 'eliminar'],
                   labels = {'tipo_cat' : 'Tipo'}
                   )
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el campo en caso de que este no exista.
        idd_campo = db(db.CAMPO_CATALOGO.nombre  == request.vars.nombre.strip(' ')).select(db.CAMPO_CATALOGO.id_campo_cat)[0].id_campo_cat
        query2 = reduce(lambda a, b: (a&b), [db.CATALOGO_TIENE_CAMPO.id_campo_cat == idd_campo,
                                             db.CATALOGO_TIENE_CAMPO.id_catalogo == id_cat])
        if len(db(query2).select())>0:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CATALOGO_TIENE_CAMPO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo)
            valor_aux = " "
            for i in range(0,total):
                db.VALORES_CAMPO_CATALOGO.insert(id_catalogo = id_cat, id_campo_cat = idd_campo, valor = valor_aux*(i+1))
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        session.nombreModificar = nombreCat
        redirect(URL('vModificarCatalogo'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        if(not(session.msgErr)):
            session.message = ''

    return dict(form = form, campos_guardados = campos_guardados,admin = admin)

'''
Funcion que se encarga de eliminar un campo del catalogo,
eliminando todas las relaciones existentes e instancias
del catalogo.
'''
def eliminarCampos2():
    # Obtengo el nombre del catalogo
    if len(request.args)!=0:
        nombreCat = request.args[0]
    else:
        nombreCat = session.catAgregar

    # Elimino todas las relaciones relacionadas con el campo
    db(db.CATALOGO_TIENE_CAMPO.id_campo_cat == request.args[1]).delete()
    db(db.VALORES_CAMPO_CATALOGO.id_campo_cat == request.args[1]).delete()

    db(db.CAMPO_CATALOGO.id_campo_cat == request.args[1]).delete()
    session.nombreModificar = nombreCat

    redirect(URL('vModificarCatalogo.html'))
