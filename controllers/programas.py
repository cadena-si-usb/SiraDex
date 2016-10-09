# -*- coding: utf-8 -*-
from funciones_siradex import get_tipo_usuario

'''
Vista de Gestionar Programas tiene las opciones:
- Agregar Programa
- Editar  Programa
- Por ahora, no se pueden eliminar programas.
'''


def agregar_programa():

    admin = get_tipo_usuario
    formulario = SQLFORM.factory(
                        Field('Nombre',
                              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                                          IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del programa no puede iniciar con numeros.")]),
                        Field('Descripcion', type="text",
                              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción',
                                  'Nombre' : 'Nombre del Programa'},
                        )

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        db.PROGRAMA.insert(nombre = request.vars.Nombre,
                           descripcion = request.vars.Descripcion
                           )
        redirect(URL('gestionar_programas.html'))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en los datos del formulario, por favor intente nuevamente.'
    # Metodo GET
    else:
        session.message = ''

    return dict(formulario=formulario, admin = admin)


# Permitiria Modificar o Desactivar Programas
# del sistema Siradex.
def gestionar_programas():
    admin = get_tipo_usuario()

    # Obtengo todos los programas almacenados en la base de datos.
    programas = db().select(db.PROGRAMA.ALL)

    formulario = SQLFORM.factory(
        Field('Nombre',
              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                          IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del programa no puede iniciar con numeros.")]),
        Field('Descripcion', type="text",
              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
        submit_button = 'Agregar',
        labels = {'Descripcion' : 'Descripción',
                  'Nombre' : 'Nombre del Programa'},
        )
    formulario.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario.element(_type='submit')['_value']="Agregar"

    formulario_editar  = SQLFORM.factory(
        Field('Nombre',
              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                          IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del programa no puede iniciar con numeros.")]),
        Field('Descripcion', type="text",
              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
        submit_button = 'Agregar',
        labels = {'Descripcion' : 'Descripción',
                  'Nombre' : 'Nombre del Programa'},
        )
    formulario_editar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    formulario_editar.element(_type='submit')['_value']="Editar"

    return dict(admin=admin, programas=programas, formulario=formulario, formulario_editar=formulario_editar)


def eliminar_programa():
    admin = get_tipo_usuario()
    db(db.PROGRAMA.id==request.args(0)).delete()
    redirect(URL('gestionar_programas'))
    return locals()


def editar_programa():

    admin = get_tipo_usuario()  # Obtengo el tipo del usuario actual.
    id = request.args[0]        # Se identifica cual programa se identificará.

    # Se busca el programa en la base de datos.
    programa = db(db.PROGRAMA.id_programa == id).select()[0]

    # Se presenta el formulario donde se modificarán los valores del programa.
    formulario = SQLFORM.factory(
                        Field('Nombre',
                              default = programa.nombre,
                              requires = [IS_NOT_EMPTY(error_message='El nombre del programa no puede quedar vacio.'),
                                          IS_MATCH('([A-Za-z])([A-Za-z0-9" "])*', error_message="El nombre del programa debe comenzar con una letra.")]),
                        Field('Descripcion', type="text",
                              default = programa.descripcion,
                              requires=IS_NOT_EMPTY(error_message='La descripcion del programa no puede quedar vacia.')),
                        submit_button = 'Actualizar',
                        labels = {'Descripcion' : 'Descripción',
                                  'Nombre' : 'Nombre del Programa'},
                        )

    # Se verifica si los campos están llenos correctamente.
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        programa.nombre = request.vars.Nombre
        programa.descripcion = request.vars.Descripcion
        programa.update_record()                    # Se actualiza el programa.
        redirect(URL('gestionar_programas.html'))   # Se redirige a la vista de gestión.

    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en los datos del formulario, por favor intente nuevamente.'
    # Metodo GET
    else:
        session.message = ''

    return dict(formulario=formulario, admin = admin)
