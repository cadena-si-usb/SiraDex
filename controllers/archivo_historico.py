'''
Modulo para la gestion del Archivo Historico
(Papelera).

Maneja elementos borrados de:
- Programas.
- Tipo de Actividades

'''

from funciones_siradex import get_tipo_usuario

#. --------------------------------------------------------------------------- .
'''
 Vista de gestion de la papelera
'''
def gestionar():

    listaTipoActividades = db(db.TIPO_ACTIVIDAD.papelera == True).select(db.TIPO_ACTIVIDAD.nombre
                                                   ,db.TIPO_ACTIVIDAD.descripcion
                                                   ,db.TIPO_ACTIVIDAD.id_tipo
                                                   ,db.TIPO_ACTIVIDAD.tipo_p_r)

    listaProgramas = db(db.PROGRAMA.papelera == True).select()

    return dict(admin=get_tipo_usuario(),
                listaTipoActividades=listaTipoActividades,
                listaProgramas = listaProgramas)

#. --------------------------------------------------------------------------- .
'''
 Metodo que elimina un tipo actividad de la base de datos
 de manera definitiva
'''
def eliminar_tipo_papelera():
    id_tipo = int(request.args[0])
    print("eliminar_def",id_tipo)
    query = reduce(lambda a, b: (a & b), [db.TIPO_ACTIVIDAD.papelera == True,
                                          db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                          db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                          db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo]
                   )
    # Guardo los reusltados en 'aux'
    aux = db(query).select(db.ACT_POSEE_CAMPO.ALL)

    # Borro las relaciones
    if (len(aux) > 0):
        db(db.ACT_POSEE_CAMPO.id_tipo_act == aux[0].id_tipo_act).delete()

    # Borro los campos
    for row in aux:
        db(db.CAMPO.id_campo == row.id_campo).delete()

    # Borro el tipo_activdad
    db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).delete()

    # Guardo mensaje de exito
    session.message = 'Tipo Eliminado'
    redirect(URL('gestionar_archivo_historico.html'))

#. --------------------------------------------------------------------------- .
'''
 Metodo que restaura un tipo actividad de la papelera
'''
def restaurar_tipo():

    id_tipo = request.args[0]
    print(id_tipo)
    tipo_actividad = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()
    print(tipo_actividad.nombre)
    tipo_actividad.update(papelera=False)
    tipo_actividad.update_record()
    print(tipo_actividad.papelera)
    session.message = 'Tipo Restaurado'
    redirect(URL('gestionar_archivo_historico.html'))
