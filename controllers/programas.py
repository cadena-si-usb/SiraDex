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
                        Field('Nombre', requires=IS_NOT_EMPTY()),
                        Field('Descripcion', type="text", requires=IS_NOT_EMPTY()),
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
        session.message = 'Error en el formulario.'
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

    return dict(programas=programas, admin = admin)
