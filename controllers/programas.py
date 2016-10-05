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

    # Seleccionamos todos los programas.
    programas = db().select(db.PROGRAMA.ALL)

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
    formulario.element(_type='submit')['_class']="btn btn-success"
    formulario.element(_type='submit')['_value']="Agregar"

    return dict(programas=programas, admin = admin, form=formulario)
