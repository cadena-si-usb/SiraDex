# -*- coding: utf-8 -*-
''' '''
'''
Vista de Gestionar Tipo Actividad, tiene las opciones:
- Agregar Tipo
- Eliminar Tipo
- Papelera (No funcional)
'''
def gestionar():
    # Obtengo datos de los tipo_actividades en base de datos para generar
    # tabla que los muestre
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.id_tipo != None, db.TIPO_ACTIVIDAD.papelera == False])
   
    ids = db(query).select(db.TIPO_ACTIVIDAD.id_tipo)
    nombres = db(query).select(db.TIPO_ACTIVIDAD.nombre)
    descripcion = db(query).select(db.TIPO_ACTIVIDAD.descripcion)
    programas = db(query).select(db.TIPO_ACTIVIDAD.programa)

    tipos = db(query).select(db.TIPO_ACTIVIDAD.nombre, db.TIPO_ACTIVIDAD.descripcion, db.TIPO_ACTIVIDAD.id_tipo)

    # Decido que mensaje se va a mostrar
    if(session.message not in ['Tipo Eliminado', 'Tipo agregado exitosamente']):
        session.message = ''
    
    return dict(ids=ids,nombres=nombres,descripcion=descripcion, programas = programas, tipos=tipos, admin = get_tipo_usuario())

'''
Vista con el formulario para agregar un Tipo Actividad
'''
def agregar_tipo():
    # Configuro widgets para el formulario de Agregar Tipo Actividad
    db.TIPO_ACTIVIDAD.nombre.widget = SQLFORM.widgets.string.widget
    db.TIPO_ACTIVIDAD.descripcion.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.producto.widget = SQLFORM.widgets.text.widget
    db.TIPO_ACTIVIDAD.nro_campos.widget = SQLFORM.widgets.integer.widget
    def horizontal_radio(f, v):
        return SQLFORM.widgets.radio.widget(f, v, cols=2)
    db.TIPO_ACTIVIDAD.tipo_p_r.widget = horizontal_radio

    # Genero el formulario para el tipo_actividad
    '''
    formulario = SQLFORM(db.TIPO_ACTIVIDAD,
                         buttons=['submit'],
                         fields=[
                                # 'nombre','tipo_p_r','descripcion','programa','producto'
                                 'nombre','tipo_p_r','descripcion','programa'
                                ],
                         labels = {'tipo_p_r' : 'Tipo de Producto', 'descripcion' : 'Descripción'},
                         submit_button='Agregar'
                        )
    '''
    catalogo = db(db.CATALOGO.nombre == 'Programas').select(db.CATALOGO.ALL).first()
    programas2 = []
    if(catalogo != None):
        #programas2.append(catalogo.id_catalogo)
        query = reduce(lambda a, b: (a&b),[db.CATALOGO_TIENE_CAMPO.id_catalogo == catalogo.id_catalogo,
                                           db.CAMPO_CATALOGO.nombre == 'Nombre',
                                           db.CAMPO_CATALOGO.id_campo_cat == db.CATALOGO_TIENE_CAMPO.id_campo_cat,
                                           db.VALORES_CAMPO_CATALOGO.id_campo_cat == db.CAMPO_CATALOGO.id_campo_cat,
                                           db.VALORES_CAMPO_CATALOGO.id_catalogo == catalogo.id_catalogo
                                          ])
    
        programas = db(query).select(db.VALORES_CAMPO_CATALOGO.ALL)
    
        for i in range(0, len(programas)):
            programas2.append(programas[i].valor)
            #programas2.append(programas[i].id_catalogo)

    formulario = SQLFORM.factory(
                        Field('Nombre', requires=IS_NOT_EMPTY()),
                        Field('Tipo', requires=IS_IN_SET(['P', 'R']), default='P'),
                        Field('Descripcion', requires=IS_NOT_EMPTY()),
                        Field('Programa', requires=IS_IN_SET(programas2)),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción'},
                        )

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if formulario.accepts(request.vars, session):
        session.form_nombre = request.vars.Nombre
        db.TIPO_ACTIVIDAD.insert(nombre = request.vars.Nombre,
                                 tipo_p_r = request.vars.Tipo,
                                 descripcion = request.vars.Descripcion,
                                 programa = request.vars.Programa
                                 #id_jefe_creador = session.usuario['cedula']
                                 )
        redirect(URL('agregar_tipo_campos.html'))
    # En caso de que el formulario no sea aceptado
    elif formulario.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''
        
    return dict(formulario=formulario, admin = get_tipo_usuario())

'''
Vista con el formulario para agregar campos al tipo actividad,
tambien tiene una tabla con los campos que ya han sido agregados
'''
def agregar_tipo_campos():
    # Obtengo el nombre del tipo_actividad desde el objeto global 'session'
    nombre_tipo = session.form_nombre
    tipo_campos = ['fecha', 'participante', 'ci', 'comunidad', 'telefono', 'texto','documento', 'imagen', 'cantidad entera', 'cantidad decimal']
    # Creo query para realizar busqueda de los campos que ya han sido agregados
    # a ese tipo actividad
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    # Guardo los resultados de dicho query en 'campos_guardados'
    campos_guardados = db(query).select(db.CAMPO.ALL, db.ACT_POSEE_CAMPO.ALL)
    
    # Busco los catalogos disponibles
    catalogos = db().select(db.CATALOGO.nombre, db.CATALOGO.id_catalogo)
    nombres_catalogos = ['---']
    for i in range(0, len(catalogos)):
        nombres_catalogos.append(catalogos[i].nombre)

    # Busco el id del tipo_actividad
    id_tipo = db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).select(db.TIPO_ACTIVIDAD.id_tipo)[0].id_tipo

    # Genero formulario para los campos
    form = SQLFORM.factory(
                    Field('Nombre', requires=IS_NOT_EMPTY()),
                    Field('Tipo', requires=IS_IN_SET(tipo_campos)),
                    Field('Obligatorio', widget=SQLFORM.widgets.boolean.widget),
                    Field('Catalogo', requires=IS_IN_SET(nombres_catalogos), default='---'),
                    labels = {'Catalogo' : 'Catálogo'},
                    submit_button = 'Agregar'
                    )
    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        # Busco el id del catalogo en caso de que haya uno
        indice = -1
        for i in range(1, len(nombres_catalogos)):
            print(nombres_catalogos[i], request.vars.Catalogo)
            if(nombres_catalogos[i] == request.vars.Catalogo):
                indice = i
        
        # Agrego el campo a la base
        if request.vars.Obligatorio == None:
            request.vars.Obligatorio = False
            
        if indice == -1:
            db.CAMPO.insert(nombre = request.vars.Nombre,
                            obligatorio = request.vars.Obligatorio,
                            lista = request.vars.Tipo,
                            despliega_cat = None
                            )
        else:
            db.CAMPO.insert(nombre = request.vars.Nombre,
                            obligatorio = request.vars.Obligatorio,
                            lista = request.vars.Tipo,
                            despliega_cat = catalogos[indice-1].id_catalogo
                            )
        # Busco el id del campo(que fue agregado al presionar boton
        # de submit) y agrego el objeto de tipo ACT_POSEE_CAMPO a la base
        # (es la relacion entre el campo y el tipo)
        idd_campo = db(db.CAMPO.nombre == request.vars.Nombre).select(db.CAMPO.id_campo)[0].id_campo
        db.ACT_POSEE_CAMPO.insert(id_tipo_act = id_tipo, id_campo = idd_campo)
        # Redirijo a la misma pagina para seguir agregando campos
        redirect(URL('agregar_tipo_campos.html'))
    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Datos invalidos'
    # Metodo GET
    else:
        session.message = ''

    return dict(form = form, campos = campos_guardados, admin = get_tipo_usuario())

'''
Metodo auxiliar usado para agregar el mensaje de exito
al agregar un tipo actividad, solo guarda el mensaje y redirige a
la pagina de gestionar
'''
def agregar_tipo_aux():
    
    session.message = 'Tipo agregado exitosamente'
    redirect(URL('gestionar.html'))

'''
Metodo que aborta la creacion de un tipo_actividad en la vista de
agregar campos, no solo elimina los campos y las relaciones sino
que tambien elimina el tipo_actividad (que a este punto ya se
encuentra en la base)
'''
def eliminar_campos():
    # Obtengo el nombre del tipo_actividad
    nombre_tipo = session.form_nombre

    # Construyo query para obtener la relacion entre los campos y el tipo
    # actividad que quiero eliminar
    query = reduce(lambda a, b: (a&b),[db.TIPO_ACTIVIDAD.nombre == nombre_tipo,
                                      db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                      db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])
    # Guardo los resultados en 'aux'
    aux = db(query).select(db.ACT_POSEE_CAMPO.ALL)

    # Borro las relaciones (en caso de que hayan)
    if(len(aux) > 0):
        db(db.ACT_POSEE_CAMPO.id_tipo_act == aux[0].id_tipo_act).delete()

    # Borro los campos asociados a estas relaciones
    for row in aux:
        db(db.CAMPO.id_campo == row.id_campo).delete()

    # Borro el tipo actiidad
    db(db.TIPO_ACTIVIDAD.nombre == nombre_tipo).delete()
    
    redirect(URL('gestionar.html'))

'''
 Funcion que envia un tipo actividad a la papelera
 el tipo es especificado por un parametr de URL
'''
def enviar_tipo_papelera():
    id_tipo = int(request.args[0])
    db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).update(papelera=True)
    session.message = 'Tipo Enviado a la Papelera'
    redirect(URL('gestionar.html'))

'''
 Vista de gestion de la papelera
'''
def gestionar_archivo_historico():
    aux = db(db.TIPO_ACTIVIDAD.papelera == True).select(db.TIPO_ACTIVIDAD.nombre,
                                                        db.TIPO_ACTIVIDAD.descripcion,
                                                        db.TIPO_ACTIVIDAD.id_tipo)

    return dict(tipos_papelera = aux,admin=get_tipo_usuario())

'''
 Metodo que elimina un tipo actividad de la base de datos
 de manera definitiva
'''
def eliminar_tipo_papelera():
    id_tipo = int(request.args[0])
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


'''
 Metodo que restaura un tipo actividad de la papelera
'''
def restaurar_tipo():
    id_tipo = int(request.args[0])
    db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).update(papelera=False)
    session.message = 'Tipo Restaurado'
    redirect(URL('gestionar.html'))

def ver_tipo_actividad():
    id_tipo = int(request.args[0])

    query = reduce(lambda a, b: (a & b), [db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                          db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                          db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])

    campos_guardados = db(query).select(db.CAMPO.ALL)

    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()

    return dict(campos = campos_guardados, tipo = tipo, admin = get_tipo_usuario())

def ver_tipo_actividad():
    id_tipo = int(request.args[0])

    query = reduce(lambda a, b: (a & b), [db.TIPO_ACTIVIDAD.id_tipo == id_tipo,
                                          db.TIPO_ACTIVIDAD.id_tipo == db.ACT_POSEE_CAMPO.id_tipo_act,
                                          db.ACT_POSEE_CAMPO.id_campo == db.CAMPO.id_campo])

    campos_guardados = db(query).select(db.CAMPO.ALL)

    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()

    return dict(campos = campos_guardados, tipo = tipo, admin=get_tipo_usuario())

def eliminar_campo():
    id_campo = int(request.args[0])

    db(db.ACT_POSEE_CAMPO.id_campo == id_campo).delete()
    db(db.CAMPO.id_campo == id_campo).delete()

    redirect(URL('agregar_tipo_campos.html'))
    
def modificar_tipo():
    id_tipo = int(request.args[0])

    tipo = db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).select(db.TIPO_ACTIVIDAD.ALL).first()

    db.TIPO_ACTIVIDAD.nombre.writable = False
    db.TIPO_ACTIVIDAD.programa.writable = False

    form = SQLFORM.factory(db.TIPO_ACTIVIDAD, record=tipo,
                   fields = ['nombre', 'tipo_p_r', 'descripcion', 'programa'],
                   labels={'tipo_p_r': 'Tipo de Producto','descripcion':'Descripción'},
                   submit_button='Relizar Cambios'
                   )

    db.TIPO_ACTIVIDAD.nombre.writable = True
    db.TIPO_ACTIVIDAD.programa.writable = True

    # Metodos POST
    # En caso de que los datos del formulario sean aceptados
    if form.accepts(request.vars, session):
        db(db.TIPO_ACTIVIDAD.id_tipo == id_tipo).update(descripcion = request.vars.descripcion,
                                                        producto = request.vars.producto)
        redirect(URL('ver_tipo_actividad.html', args=[id_tipo]))

    # En caso de que el formulario no sea aceptado
    elif form.errors:
        session.message = 'Error en el formulario'
    # Metodo GET
    else:
        session.message = ''

    return dict(tipo=tipo, form=form, admin=get_tipo_usuario())

def get_tipo_usuario():
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
        
    return admin
