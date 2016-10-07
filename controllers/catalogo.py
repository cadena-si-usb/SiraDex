# -*- coding: utf-8 -*-
from funciones_siradex import get_tipo_usuario


tipo_campos = ['Fecha', 'Teléfono', 'Texto','Documento', 'Imagen', 'Número']

'''
Funcion que se encarga de obtener los datos para mostrar los catalogos
que existen en el sistema.
'''
def vGestionarCatalogos():
    # Obtengo el tipo del usuario para permitir el acceso a la visa
    # Limpio el Session del sistema.
    admin = get_tipo_usuario()
    message = ""
    # Se obtienen los nombres de todos los catalogos y se pasan al html.
    catalogos = db(db.CATALOGO).select(db.CATALOGO.nombre, db.CATALOGO.id_catalogo)
    return dict(admin = admin, catalogos = catalogos, message = message)

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
        redirect(URL('vModificarCatalogo.html',args=[id_catalogo]))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en el Formulario.'
    else:
        session.message = ''

    return(dict(formulario = formulario, admin = admin))

'''
Funcion que se encarga de mostrar los campos del catalogo,
permite crear y elminiar campos relacionados con el catalogo indicado.
'''
def vModificarCatalogo():

    admin = get_tipo_usuario()

    # Obtengo el id del catalogo
    id_catalogo = request.args[0]

    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese catalogo
    campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select()

    #Como los catalogos son unicos, tomamos siempre el primer elemento del query.
    nombre_catalogo  = db.CATALOGO[id_catalogo].nombre

    # Busco el id del catalogo
    # Genero formulario para los campos
    formulario = SQLFORM.factory(
                    Field('nombre',
                          requires = [IS_NOT_EMPTY(error_message='El nombre del campo no puede quedar vacio.'),
                                      IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del campo debe comenzar con una letra.")]),
                    Field('tipo_campo',
                           requires = [IS_IN_SET(tipo_campos, zero='Seleccione...', error_message="Debe seleccionar un tipo para el campo.")],
                           widget = SQLFORM.widgets.options.widget),
                    Field('obligatorio', type='boolean', default = False),
                    labels = {'nombre'      : 'Nombre',
                              'tipo_campo'  : 'Tipo',
                              'obligatorio' : 'Obligatorio'},
                    submit_button='Agregar'
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
            db.CAMPO_CATALOGO.insert(id_catalogo = id_catalogo,
                                     nombre =  nombre_campo_nuevo,
                                     tipo_campo = request.vars.tipo_campo,
                                     obligatorio = request.vars.obligatorio)
            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vModificarCatalogo', args=[id_catalogo]))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Datos invalidos para el campo.'
    else:
        if(not(session.msgErr)):
            session.message = ''

    return dict(formulario = formulario,
                campos_guardados = campos_guardados,
                nombre_catalogo = nombre_catalogo,
                admin      = admin)

'''
Funcion auxiliar que se encarga de colocar
el mensaje de exito.
'''
def agregarTipoAux():
    session.message = 'Catalogo agregado exitosamente'
    redirect(URL('vGestionarCatalogos.html'))


'''
Funcion auxiliar que se encarga de colocar
el mensaje de exito.
'''
def agregarTipoAux2():
    session.message = 'Catalogo editado exitosamente'
    redirect(URL('vGestionarCatalogos.html'))

'''
Funcion que se encarga de eliminar un catalogo, los campos
que este posee y todas las relaciones entre ellos.
'''
def eliminarCatalogo():

    # Obtengo el id del Catalogo a eliminar
    id_catalogo = request.args[0]

    #eliminamos todos los campos de ese catalogo
    campos_del_catalogo = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).delete()

    #eliminarmos el catalogo.
    del db.CATALOGO[id_catalogo]

    redirect(URL('vGestionarCatalogos.html'))

# '''
# Funcion que se encarga de agregar valores a los
# campos de un catalogo, en caso de que no exista
# otra instancia con el mismo valor.
# '''
# def vAgregarElementoCampo():
#     # Obtengo el tipo del usuario y el id del catalogo.
#     admin = get_tipo_usuario()
#     id_catalogo = request.args[0]
#
#     # Busco los campos asociados al catalogo.
#     query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == id_catalogo,
#                                       db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
#                                       db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
#     aux = db(query).select(db.CAMPO_CATALOGO.nombre)
#     # Creo 2 arreglos para almacenar los campos y los id de cada campo.
#     campos = []
#     idsCampos = []
#     # Nombres de los campos
#     for row in aux:
#         campos.append(row['nombre'])
#
#     arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
#     cantidadCampos = len(campos)
#     # Obtengo los ids de los campos
#     for row in arrId:
#         idsCampos.append(row['id_campo_cat'])
#     # Creo un arreglo con todos los campos del formulario.
#     arreglo = []
#     for i in range (0,len(campos)):
#         arreglo += [ Field("pr"+str(i),'string', label=T(str(campos[i]))) ]
#     if(len(arreglo) > 0):
#         forma = SQLFORM.factory(
#             *arreglo)
#     else:
#         session.message = "El catalogo no posee campos"
#         redirect(URL('vGestionarCatalogos.html'))
#
#     if len(request.vars)>0:
#         for i in range(0, cantidadCampos):
#             valor = request.vars["pr"+str(i)]
#
#             # Genero un query para revisar si el valor existe en alguna instancia del campo.
#             query2 = reduce(lambda a, b: (a&b), [db.VALORES_CAMPO_CATALOGO.valor == valor, db.VALORES_CAMPO_CATALOGO.id_catalogo == id_catalogo,
#                                                  db.VALORES_CAMPO_CATALOGO.id_campo_cat == idsCampos[i]])
#             if(len(db(query2).select()) > 0):
#                 session.nombreMostrar = id_catalogo
#                 session.message = "El valor de un campo esta duplicado"
#                 redirect(URL('vMostrarCatalogo.html'))
#
#         # Almaceno los valores en cada uno de los campos
#         for i in range(0, cantidadCampos):
#             valor = request.vars["pr"+str(i)]
#             db.VALORES_CAMPO_CATALOGO.insert(id_campo_cat = idsCampos[i], id_catalogo = id_catalogo, valor = valor)
#         session.nombreMostrar = id_catalogo
#         redirect(URL('vMostrarCatalogo.html'))
#
#     return (dict(forma = forma, admin = admin))

'''
Funcion encargada de mostrar todas las instancias
de los campos de un catalogo en una tabla.
'''
def vMostrarCatalogo():
    admin = get_tipo_usuario()
    # Obtengo el id del catalogo a mostrar
    id_catalogo = request.args[0]

    # Buscamos los campos que se necesitan de los catalogos.
    campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select()

    #Como los catalogos son unicos, tomamos siempre el primer elemento del query.
    nombre_catalogo  = db.CATALOGO[id_catalogo].nombre

    return dict(campos_guardados = campos_guardados,
                id_catalogo      = id_catalogo,
                nombre_catalogo  = nombre_catalogo,
                admin = admin)

'''
Funcion que se encarga de modificar las caracteriticas de un
campo de un catalogo.
'''
def vModificarCampo():

    #Obtenemos el tipo de Usuario.
    admin = get_tipo_usuario()

    #obtenemos el campo que queremos modificar:
    id_campo    = request.args[0]
    #obtenemos el id del catalogo al que pertenece el campo en cuestion
    id_catalogo = request.args[1]

    #obtenemos los datos de ese campo
    datos_campo = db.CAMPO_CATALOGO[id_campo]

    formulario = SQLFORM.factory(
                    Field('nombre',
                          requires = [IS_NOT_EMPTY(error_message='El nombre del campo no puede quedar vacio.'),
                                      IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del campo debe comenzar con una letra.")]),
                    Field('tipo_campo',
                           requires = [IS_IN_SET(tipo_campos, zero='Seleccione...', error_message="Debe seleccionar un tipo para el campo.")],
                           widget = SQLFORM.widgets.options.widget),
                    Field('obligatorio', type='boolean', default = False),
                    labels = {'nombre'      : 'Nombre',
                              'tipo_campo'  : 'Tipo',
                              'obligatorio' : 'Obligatorio'},
                    submit_button='Guardar'
                   )

    #Prellenamos el formulario con los campos que ya tenia el formulario.
    print datos_campo

    formulario.vars.nombre      = datos_campo.nombre
    formulario.vars.tipo_campo  = datos_campo.tipo_campo
    formulario.vars.obligatorio = datos_campo.obligatorio

    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):

        nombre_nuevo = request.vars.nombre
        nombre_repetido    = False

        #Bucamos los campos que esten guardados
        campos_guardados = db(db.CAMPO_CATALOGO.id_catalogo == id_catalogo).select()

        #Si existe un campo que tenga el mismo nombre
        #Y no sea el campo que estamos modificando.
        #Entonces existe un campo con nombre repetido.
        for campo in campos_guardados:
            if (campo.nombre == nombre_nuevo and
                campo.id_campo_cat != datos_campo.id_campo_cat):
                nombre_repetido = True
                break

        # Si el nombre no esta repetido, modificamos el campo
        if nombre_repetido:
            session.msgErr = 1
            session.message = 'Ya existe un campo llamado "' + nombre_nuevo + '" en el catalogo.'
        else:
            #Actualizamos el campo
            db.CAMPO_CATALOGO[id_campo] = dict(nombre      = nombre_nuevo,
                                               tipo_campo  = request.vars.tipo_campo,
                                               obligatorio = request.vars.obligatorio)

            session.msgErr = 0
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('vModificarCatalogo', args=[id_catalogo]))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Datos invalidos para el campo.'
    else:
        if(not(session.msgErr)):
            session.message = ''

    return(dict(formulario=formulario, admin=admin))

# '''
# Funcion que se encarga de eliminar una instancia
# de los campos de un catalogo.
# '''
# def eliminarValorCampo():
#     # Obtengo el tipo del usuario y el nombre del campo a eliminar.
#     admin = get_tipo_usuario()
#     id_campo = request.args[0]
#     valor = request.args[1]
#     print("id_campo: ", id_campo, " valor: ", valor)
#     for dic in session.filas:
#         for i in dic:
#             if (str(i['id_campo_cat'])==id_campo) and (str(i['valor']) == valor):
#                 diccionario = i
#                 dcc = dic
#                 print("request.args: ", request.args)
#                 print("session.filas: ", session.filas)
#
#     # Genero un query para buscar los campos que tiene el catalogo.
#     query = reduce(lambda a, b: (a&b),[db.CATALOGO.id_catalogo == diccionario['id_catalogo'],
#                                        db.CATALOGO.id_catalogo == db.CATALOGO_TIENE_CAMPO.id_catalogo,
#                                       db.CATALOGO_TIENE_CAMPO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat])
#     aux = db(query).select(db.CAMPO_CATALOGO.nombre)
#     # Arreglos auxiliares para guardar los campos y los ids respectivamente.
#     cmpo = []
#     ids = []
#     # Nombres de los campos
#     for row in aux:
#         cmpo.append(row['nombre'])
#
#     arrId = db(query).select(db.CAMPO_CATALOGO.id_campo_cat)
#
#     # Ids de los campos
#     for row in arrId:
#         ids.append(row['id_campo_cat'])
#     # Voy eliminando el valor de cada campo de la fila seleccionada
#     for i in range(0,len(cmpo)):
#         for f in dcc:
#             if(f['id_campo_cat'] == ids[i]):
#                 df = f['valor']
#
#         db(db.VALORES_CAMPO_CATALOGO.valor == df).delete()
#     session.nombreMostrar = db(db.CATALOGO.id_catalogo == diccionario['id_catalogo']).select(db.CATALOGO.id_catalogo)[0].id_catalogo
#     redirect(URL('vMostrarCatalogo.html'))

'''
Funcion que se encarga de eliminar un campo del catalogo,
eliminando todas las relaciones existentes e instancias
del catalogo.
'''
def eliminarCampos():

    # Obtengo el id del campo que se eliminara
    id_campo_cat = request.args[0]
    id_catalogo  = request.args[1]

    # Elimino el campo del catalogo. Esto no afecta los tipos de actividades
    # Que estan definidas ya, ni los productos ya listos.
    del db.CAMPO_CATALOGO[id_campo_cat]

    redirect(URL('vModificarCatalogo.html', args=[id_catalogo]))
