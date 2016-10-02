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
                                          IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del catalogo debe comenzar con una letra."),
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
    campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == id_cat).select()

    # Busco el id del catalogo
    # Genero formulario para los campos
    formulario = SQLFORM(db.CAMPO_CATALOGO,
                   submit_button='Agregar',
                   fields = ['nombre', 'tipo_campo', 'obligatorio'],
                   labels = {'tipo_campo' : 'Tipo'}
                   )
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):

        nombre_campo_nuevo = request.vars.nombre
        nombre_repetido    = False

        for campo in campos_guardados:
            if campo.nombre == nombre_campo_nuevo:
                nombre_repetido = True
                break

        # Si el nombre no esta repetido, lo eliminamos.
        if nombre_repetido:
            session.msgErr = 1
            session.message = 'Ya existe el campo'
        else:
            db.CAMPO_CATALOGO.insert(id_catalogo = id_cat,
                                     nombre =  nombre_campo_nuevo,
                                     tipo_campo = request.vars.tipo_campo,
                                     obligatorio = request.vars.obligatorio)
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vAgregarCampos', args=[id_cat]))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Datos invalidos para el campo.'
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
def deshabilitarCatalogo():
    # Obtengo el id o nombre del Catalogo
    if len(request.args)!=0:
        nombreCat = request.args[0]
        subQueryCatalogo = (db.CATALOGO.id_catalogo == nombreCat)
    else:
        nombreCat = session.catAgregar
        subQueryCatalogo = (db.CATALOGO.nombreCat == nombreCat)
    # Construyo query para obtener la relacion entre los campos y el catalogo
    # que debo eliminar
    query = reduce(lambda a, b: (a&b),[subQueryCatalogo,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])

    # Guardo los resultados en 'aux'
    aux = db(query).select(db.CATALOGO_TIENE_CAMPO.ALL)

    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        aux2 = db(db.CAMPO.despliega_cat == aux[0].id_catalogo).select()
        db(db.VALORES_CAMPO_CATALOGO.id_catalogo == aux[0].id_catalogo).delete()
        if(len(aux2) >0):
            db(db.ACT_POSEE_CAMPO.id_campo == aux2[0]['id_campo']).delete()
        db(db.CATALOGO_TIENE_CAMPO.id_catalogo == aux[0].id_catalogo).delete()
        db(db.CAMPO.despliega_cat == aux[0].id_catalogo).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        query2 = reduce(lambda a,b: (a&b),[db.CAMPO_CATALOGO.id_campo_cat == row.id_campo_cat])
        aux3 = db(query2).select(db.CAMPO_CATALOGO.ALL)
        db(db.CAMPO_CATALOGO.id_campo_cat == aux3[0].id_campo_cat).delete()


    # Borro el catalogo
    db(subQueryCatalogo).delete()

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
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    aux = db(query).select(db.CAMPO_CATALOGO.nombre)
    # Creo 2 arreglos para almacenar los campos y los id de cada campo.
    campos = []
    idsCampos = []
    # Nombres de los campos
    for row in aux:
        campos.append(row['nombre'])

    arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
    cantidadCampos = len(campos)
    # Obtengo los ids de los campos
    for row in arrId:
        idsCampos.append(row['id_campo_cat'])
    # Creo un arreglo con todos los campos del formulario.
    arreglo = []
    for i in range (0,len(campos)):
        arreglo += [ Field("pr"+str(i),'string', label=T(str(campos[i]))) ]
    if(len(arreglo) > 0):
        forma = SQLFORM.factory(
            *arreglo)
    else:
        session.message = "El catalogo no posee campos"
        redirect(URL('vGestionarCatalogo.html'))

    if len(request.vars)>0:
        for i in range(0, cantidadCampos):
            valor = request.vars["pr"+str(i)]

            # Genero un query para revisar si el valor existe en alguna instancia del campo.
            query2 = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_catalogo,
                                                 db.VALORES_CAMPO_CATALOGO.id_campo_cat == idsCampos[i]])
            if(len(db(query2).select()) > 0):
                session.nombreMostrar = id_catalogo
                session.message = "El valor de un campo esta duplicado"
                redirect(URL('vMostrarCatalogo.html'))

        # Almaceno los valores en cada uno de los campos
        for i in range(0, cantidadCampos):
            valor = request.vars["pr"+str(i)]
            db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = idsCampos[i], id_catalogo = id_catalogo, valor = valor)
        session.nombreMostrar = id_catalogo
        redirect(URL('vMostrarCatalogo.html'))

    return (dict(forma = forma, admin = admin))

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
    query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
                                      db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
                                      db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
    query2 = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
                                       db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                       db.VALORES_CAMPO_CATALOGO.id_catalogo == db.CATALOGO.id_catalogo])

    # Guardo los resultados del los queries creados
    campos_guardados = db(query).select(db.CAMPO_CATALOGO.ALL, db.CATALOGO_TIENE_CAMPO.ALL)
    id_campos = db(query).select(db.CATALOGO_TIENE_CAMPO.ALL)
    valores_campos = db(query2).select(db.VALORES_CAMPO_CATALOGO.ALL)
    nroCampos = len(campos_guardados)
    nroValores = len(valores_campos)

    # Calculo el numero de filas que debera mostrar la tabla.
    if(nroCampos != 0):
        nroFilas = nroValores/nroCampos
    else:
        nroFilas = 0

    # Arreglos auxiliares para almacenar las filas y las columnas de la tabla
    filas = []
    columnas = []
    j = 0
    # Creo las columnas de la tabla (Los valores de cada campo)
    for i in range(0,len(id_campos)):
        arr = []
        id_act = id_campos[i]['id_campo_cat']
        for j in range(0,len(valores_campos)):
            if(valores_campos[j]['id_campo_cat'] == id_act):
                arr.append(valores_campos[j])
        columnas.append(arr)
    j = 0
    # Creo las filas que se mostraran en la tabla.
    for i in range(0,nroFilas):
        aux = []
        for j in range(0,len(columnas)):
            aux.append(columnas[j][i])
        filas.insert(-1,aux)
    # Guardo las filas globalmente para poder acceder a ellas de forma sencilla y eficiente.
    session.filas = filas
    nombre = db(db.CATALOGO.id_catalogo == id_catalogo).select(db.CATALOGO.nombre)
    print("VMostrarCatalogo filas: ",filas)
    return dict(campos_guardados = campos_guardados,filas = filas, admin = admin, nombre = id_catalogo)

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
    print("333: KKKK", request.args)
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
    print(ids[0])
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
    print("id_campo: ", id_campo, " valor: ", valor)
    for dic in session.filas:
        for i in dic:
            if (str(i['id_campo_cat'])==id_campo) and (str(i['valor']) == valor):
                diccionario = i
                dcc = dic
                print("request.args: ", request.args)
                print("session.filas: ", session.filas)

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
        print("492: ",request.vars)
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
def eliminarCampos():
    # Obtengo el nombre del campo que se eliminara
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
