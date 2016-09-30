# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

### Required: do not delete
def user():
    return dict(form=auth())

def download():
    return response.download(request, db)

def call():
    return service()
### end required


#Funcion del inicio
def index():
    datosComp = ["","","","","","","",""]
    return response.render()

# Funcion para busquedas publicas
def busqueda():
    
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
    


    query = reduce(lambda a, b: (a&b),[db.ACTIVIDAD.validacion == 'Validada',
                                       db.ACTIVIDAD.id_tipo == db.TIPO_ACTIVIDAD.id_tipo
                                       ]
                  )
    # Hago el query
    #query=((db.ACTIVIDAD.validacion == 'Validada'))

    # Muestro los ids, el estado y nombres de las actividades validadas
    aux = db(query).select(db.ACTIVIDAD.id_actividad,
                           db.ACTIVIDAD.estado,
                           db.ACTIVIDAD.id_tipo
                          )
    
    aux1 = db(query).select(db.TIPO_ACTIVIDAD.nombre, db.TIPO_ACTIVIDAD.id_tipo
                         )

    return dict(tipos = aux1, actividades = aux, admin = admin) # no necesita el admin, creo

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
    query = reduce(lambda a, b: (a&b),[db.ACTIVIDAD.validacion == 'En espera',
                                       db.ACTIVIDAD.id_tipo == db.TIPO_ACTIVIDAD.id_tipo
                                       ]
                  )
    # Muestro los ids y nombres de las actividades a validar o rechazar
    aux = db(query).select(db.ACTIVIDAD.id_actividad, db.ACTIVIDAD.id_tipo
                         )
    aux1 = db(query).select(db.TIPO_ACTIVIDAD.nombre, db.TIPO_ACTIVIDAD.id_tipo
                         )

    return dict(tipos = aux1, actividades = aux, admin = admin)

# Metodo para validar una actividad
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
    db(db.ACTIVIDAD.id_actividad == id_act).update(validacion='Validada')
    session.message = 'Actividad validada exitosamente'
    redirect(URL('gestionar_validacion.html'))

# Metodo para rechazar una actividad
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
    db(db.ACTIVIDAD.id_actividad == id_act).update(validacion='Rechazada')
    session.message = 'Actividad rechazada'
    redirect(URL('gestionar_validacion.html'))
