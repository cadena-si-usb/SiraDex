# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os
import re
from usbutils import get_ldap_data, random_key
import urllib2
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

########################################################################################################
############################################# FUNCIONES USUARIO ########################################
########################################################################################################
def get_tipo_usuario():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL(c = "default",f="index"))
        if session.usuario["tipo"] == "Administrador":
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            elif(session.usuario["tipo"] == "Bloqueado"):      
                admin = -1
            else:
                admin = 0
        else:
            redirect(URL(c ="default",f="vMenuPrincipal"))
    else:
        redirect(URL(c ="default",f="index"))
        
def login_cas():
    if not request.vars.getfirst('ticket'):
        #redirect(URL('error'))
        pass
    try:
        import urllib2, ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://secure.dst.usb.ve/validate?ticket="+\
              request.vars.getfirst('ticket') +\
              "&service=http%3A%2F%2F159.90.211.179%2FSiraDex%2Fdefault%2Flogin_cas"
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()

    except Exception, e:
        print "Exception: "
        print e
        # redirect(URL('error'))

    if the_page[0:2] == "no":
        pass
    else:
        # session.casticket = request.vars.getfirst('ticket')
        data  = the_page.split()
        usbid = data[1]

        usuario = get_ldap_data(usbid) #Se leen los datos del CAS
        tablaUsuarios = db.USUARIO

        session.usuario = usuario
        print "Hola",session.usuario
        session.usuario['usbid'] = usbid

        if not db(tablaUsuarios.usbid == usbid).isempty():
            datosUsuario = db(tablaUsuarios.usbid==usbid).select()[0]
            session.usuario['tipo'] = datosUsuario.tipo
            redirect(URL('vMenuPrincipal'))
        else:
            session.usuario['tipo'] = "Administrador"
            db.USUARIO.insert(ci=session.usuario["cedula"],  # Lo insertamos en la base de datos.
            usbid=session.usuario["usbid"],
            nombres=session.usuario["first_name"],
            apellidos=session.usuario["last_name"],
            correo_inst=session.usuario["email"],
            tipo = "Administrador")
            redirect(URL('vRegistroUsuario'))

def logout_cas():
    session.usuario = None
    return response.render()

#Funcion del inicio
def index():
    datosComp = ["","","","","","","",""]
    return response.render()

# Controlador para el registro del usuario
def vRegistroUsuario():
    if session.usuario != None:
        # Se usa un formulario que muestre los datos no modificables.
        form = SQLFORM.factory(
            Field("USBID", default=session.usuario["usbid"],writable = False),
            Field('Nombres',default=session.usuario["first_name"],writable = False),
            Field('Apellidos', default=session.usuario["last_name"],writable=False),
            readonly=True)

        #Realiza las modificaciones sobre la base de datos en funcion de lo que introduzca el usuario.
        usuarios = db(db.USUARIO).select()
        for raw in usuarios:
            if raw.ci == session.usuario["cedula"]:
                print("SE metio")
                forma=SQLFORM(
                    db.USUARIO,
                    raw,
                    button=['Registrarse'],
                    fields=['telefono','correo_alter'],
                    submit_button='Registrarse',
                    labels={'telefono':'Teléfono', 'correo_alter':'Correo alternativo'})
                break
        if len(request.vars)!=0:
            nuevoTelefono = request.vars.telefono
            nuevoCorreoAlter = request.vars.correo_alter
            db(db.USUARIO.ci == session.usuario["cedula"]).update(telefono=nuevoTelefono, correo_alter=nuevoCorreoAlter)
            redirect(URL('vMenuPrincipal'))        # Redirige al usuario al menu principal.
        return dict(form1 = form, form = forma, admin=get_tipo_usuario())
    else:
        redirect(URL("index"))

def vVerPerfil():
    if session.usuario != None:
	if session.usuario["tipo"] == "Bloqueado":
	    redirect(URL("index"))		 
        admin = 4
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0
        tlf = None
        correo_a = None
        correo_i = None
        usuarios = db(db.USUARIO).select()
        for raw in usuarios:
            if raw.ci == session.usuario["cedula"]:
                tlf = raw.telefono
                correo_a = raw.correo_alter
                correo_i = raw.correo_inst
        form = SQLFORM.factory(
            Field("USBID", default=session.usuario["usbid"],writable = False),
            Field('Nombres',default=session.usuario["first_name"],writable = False),
            Field('Apellidos', default=session.usuario["last_name"],writable=False),
            Field('Correo_Institucional', default=correo_i,writable=False),
            Field('Telefono',label = "Teléfono", default=tlf,writable=False),
            Field('Correo_Alternativo', default=correo_a,writable=False),
            readonly=True)
        return dict(form1 = form,admin = admin)
    else:
        redirect(URL("index"))
        
def vMenuPrincipal():
    if session.usuario != None:
        admin = 4
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0
        return dict(admin = admin)
    else:
        redirect(URL("index"))

def vMenuDex():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
            admin = 4
            if(session.usuario["tipo"] == "DEX"):
                admin = 2
            elif(session.usuario["tipo"] == "Administrador"):
                admin = 1
            else:
                admin = 0
            return dict(admin = admin)
        else:
            redirect(URL("vMenuPrincipal"))
    else:
        redirect(URL("index"))

def vEditarPerfil():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0
        form = SQLFORM.factory(
            Field("USBID", default=session.usuario["usbid"],writable = False),
            Field('Nombres',default=session.usuario["first_name"],writable = False),
            Field('Apellidos', default=session.usuario["last_name"],writable=False),
            readonly=True)
        usuarios = db(db.USUARIO).select()
        # Modificar datos del perfil.
        for raw in usuarios:
            if raw.ci == session.usuario["cedula"]:
                forma=SQLFORM(
                    db.USUARIO,
                    record=raw,
                    button=['Actualizar'],
                    fields=['telefono','correo_alter'],
                    submit_button='Actualizar',
                    labels={'telefono':'Teléfono', 'correo_alter':'Correo alternativo'})
        if len(request.vars)!=0:
            nuevoTelefono = request.vars.telefono
            nuevoCorreoAlter = request.vars.correo_alter
            db(db.USUARIO.ci == session.usuario["cedula"]).update(telefono=nuevoTelefono, correo_alter=nuevoCorreoAlter)
            redirect(URL('vVerPerfil'))

        return dict(form1 = form, form = forma, admin = admin)
    else:
        redirect(URL("index"))

##########################################################################################################
###################################  FUNCIONES GESTIONAR USUARIO  ########################################
##########################################################################################################

def vMenuAdmin():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            session.message = ""
            return response.render(admin = get_tipo_usuario())
        else:
            redirect(URL("vMenuPrincipal"))
    else:
        redirect(URL("index"))

def vGestionarUsuarios():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            message = session.message
            session.message = ""
            aux = db(db.USUARIO).select(db.USUARIO.usbid,db.USUARIO.nombres,db.USUARIO.apellidos,db.USUARIO.tipo)
            return dict(usuarios = aux,message = message, admin=get_tipo_usuario())
        else:
            redirect(URL("vMenuPrincipal"))
    else:
        redirect(URL("index"))
    
def vAgregarUsuario():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            message = ""
            datosCompAux = ["","","","","","","",""]    # En esta lista guardaremos todos los datos que seran extraidos del LDAP para crear el nuevo usuario
            forma=SQLFORM(                              # Se hace un formulario para introducir un USBID.
                db.USUARIO,
                button=['Agregar'],
                fields=['usbid','tipo','telefono','correo_alter'],
                submit_button='Agregar',
                labels={'usbid':'USBID','telefono':'Teléfono', 'correo_alter':'Correo alternativo','tipo':'Tipo'})
            # Si el largo de request.vars es mayor a cero, quiere decir que de introdujo informacion en el formulario.
            if len(request.vars)!=0:
                # En usbidAux almacenamos el usbid proporcionado por el administrador
                # En imprimir1 almacenamos la informacion del LDAP con grep
                usbidAux = request.vars.usbid
                user = get_ldap_data(usbidAux)
                telefonoAux = request.vars.telefono
                correo_alterAux = request.vars.correo_alter
                tipoAux = request.vars.tipo
                if(len(tipoAux) < 3):
                    message = T("Debe Especificar un Tipo")
                    redirect(URL("vAgregarUsuario"))
                imprimir1 = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ usbidAux +" | grep '^givenName\|^personalId\|^sn\|^uid:\|^mail\|^studentId\|^career\|^gidNumber'")
                
                # Recorremos cada linea del archivo para realizar las asignaciones correspondientes de acuerdo a la informacion proporcionada por el LDAP
                for line in imprimir1.readlines():
                    line = line.split(':')        # Separamos los campos por los dos puntos.
                    if line[0] == "uid":          # Primera Posicion: Carnet con guion.
                        datosCompAux[0] = line[1]
                    elif line[0] == "givenName":  # Segunda Posicion: Nombre(s) del usuario.
                        datosCompAux[1] = line[1]
                    elif line[0] == "sn":         # Tercera Posicion: Apellido(s) del usuario.
                        datosCompAux[2] = line[1]
                    elif line[0] == "personalId": # Cuarta Posicion: Cedula de identidad del usuario.
                        datosCompAux[3] = line[1]
                    elif line[0] == "gidNumber":  # Quinta Posicion: Rol del usuario (Profesor, estudiante, etc.).
                        datosCompAux[4] = line[1]
                    elif line[0] == "mail":       # Sexta Posicion: Email del usuario.
                        datosCompAux[5] = line[1]
                    elif line[0] == "career":     # Septima posicion: Carrera del usuario.
                        datosCompAux[6] = line[1]
                    elif line[0] == "studentId":  # Octava posicion: Carnet sin guion.
                        datosCompAux[7] = line[1]
                
                # Si datosCompAux esta vacio, quiere decir que no se el carnet no esta en LDAP
                print(datosCompAux)
                if datosCompAux[0]=="":
                    message = T("El usuario no se encuentra asociado al CAS")
                    #return dict(message = response.flash)
                # En caso contrario, el usuario debe ser agregado a la base de datos de la universidad.
                else:
                    # Primero verificamos que el usuario que intenta agregarse no esta en la base de datos
                    if db(db.USUARIO.usbid == usbidAux).isempty():
                        # Lo insertamos en la base de datos.
                        db.USUARIO.insert(ci=user["cedula"],
                                usbid=usbidAux,
                                nombres=datosCompAux[1],
                                apellidos=datosCompAux[2],
                                correo_inst=user["email"],
                                telefono = telefonoAux,
                                correo_alter = correo_alterAux,
                                tipo = tipoAux)
                        
                        # Luego de insertar al usuario, mostramos un formulario al administrador con los datos de la persona agregada
                        form = SQLFORM.factory(
                            Field("USBID", default=datosCompAux[0],writable = False),
                            Field('Nombres',default=datosCompAux[1],writable = False),
                            Field('apellidos', default=datosCompAux[2],writable=False),
                            readonly=True)
                        return dict(form = form, message = message, bool = 1, admin=get_tipo_usuario())
                    else:
                        message= T("El usuario ya esta registrado")
                        #return dict(message = response.flash)
            return dict(form = forma,message = message, admin=get_tipo_usuario())
        else:
            redirect(URL("vMenuPrincipal"))
    else:
        redirect(URL("index"))
        
def vEliminarUsuario():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            if len(request.args)!=0 :
                if request.args[0] != session.usuario["usbid"]:
                    session.message = ""
                    if (not db(db.USUARIO.usbid == request.args[0]).isempty()):
                        db(db.USUARIO.usbid == request.args[0]).delete()
                        redirect(URL('vGestionarUsuarios'))
                else:
                    session.message = T("Para eliminar su cuenta, por favor comuníquese con un administrador")
                    redirect(URL('vGestionarUsuarios'))
        else:
            redirect(URL("vMenuPrincipal"))
    else:
        redirect(URL("index"))

def vModificarRol():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            message= ""
            form = SQLFORM.factory(
                            Field("USBID", default=request.args[0],writable = False),
                            readonly=True)
            forma=SQLFORM(        
                    db.USUARIO,
                    button=['Actualizar'],
                    fields=['tipo'],
                    submit_button='Actualizar',
                    labels={'tipo':'TIPO'})
            if len(request.vars)!=0:
                if (not db(db.USUARIO.usbid == request.args[0]).isempty()):
                    if(request.args[0] != session.usuario["usbid"]): 
                        db(db.USUARIO.usbid == request.args[0]).update(tipo = request.vars.tipo)
                        redirect(URL('vGestionarUsuarios'))
                    else:
                        message = T("Para cambiar sus permisos, por favor comuníquese con un administrador")
                else:
                    message = T("El Usuario no se encuentra registrado")

            return dict(forma = form, form = forma, message = message, admin=get_tipo_usuario())
        else:
            redirect(URL("vMenuPrincipal"))
    else:
        redirect(URL("index"))
        
def setVista():
    session.vista = int(request.args[0])
    
    if session.vista == 0:
        redirect(URL(c='actividad', f='gestionar.html'))
    elif session.vista == 1:
        redirect(URL(c='tipo_actividad', f='gestionar.html'))
    elif session.vista == 2:
        redirect(URL(c='default', f='vGestionarUsuarios.html'))
    else:
        print('NO JUEGUES CON MI SISTEMA')
        
    return dict(admin = get_tipo_usuario())

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

def cambiar_colores():

    session.template = int(request.vars['color'])
    print(session.template)
    if request.env.http_referer:
        redirect(request.env.http_referer)

    return dict()
