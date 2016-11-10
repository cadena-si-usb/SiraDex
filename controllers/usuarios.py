import os
import datetime
import re
from notificaciones import *
from usbutils import get_ldap_data, random_key
import urllib2
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

def gestionar():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            message = session.message
            session.message = ""
            aux = db(db.USUARIO).select(db.USUARIO.usbid,db.USUARIO.nombres,db.USUARIO.apellidos,db.USUARIO.tipo)

            form_editar=SQLFORM(
                    db.USUARIO,
                    button=['Actualizar'],
                    fields=['tipo'],
                    labels={'tipo':'TIPO'})
            form_editar.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
            form_editar.element(_type='submit')['_value']="Actualizar"

            ## Formulario para colocar el mensaje.
            formulario_contactar = SQLFORM.factory(
                                        Field('asunto', type="string"),
                                        Field('mensaje', type="text"),
                                        Field('usbid', type="string"),
                                        submit_button = 'Enviar')
            if formulario_contactar.accepts(request.vars, session, formname="formulario_contactar"):
                usbid = request.vars.usbid
                asunto = request.vars.asunto
                mensaje = request.vars.mensaje

                ## Obtenemos el usuario al que deseamos contactar.
                usuario = db(db.USUARIO.usbid == usbid).select().first()

                ## parseamos los datos para la notificacion
                datos_usuario = {'nombres' : usuario.nombres}
                if usuario.correo_alter != None:
                     datos_usuario['email'] = usuario.correo_alter
                else:
                     datos_usuario['email'] = usuario.correo_inst

                ## Enviamos la notificacion
                enviar_correo_contacto(mail, datos_usuario, asunto, mensaje)

                redirect(URL('gestionar'))


            if len(request.vars)!=0:
                if (not db(db.USUARIO.usbid == request.args[0]).isempty()):
                    if(request.args[0] != session.usuario["usbid"]):
                        db(db.USUARIO.usbid == request.args[0]).update(tipo = request.vars.tipo)
                        redirect(URL('gestionar'))
                    else:
                        message = T("Para cambiar sus permisos, por favor comuníquese con un administrador")
                else:
                    message = T("El Usuario no se encuentra registrado")

            return dict(form_editar=form_editar, formulario_contactar=formulario_contactar,usuarios = aux,message = message, admin=get_tipo_usuario())
        else:
            redirect(URL("perfil"))
    else:
        redirect(URL("index"))

def agregar():
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
            # Estilo del boton
            forma.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
            forma.element(_type='submit')['_value']="Agregar"

            # Si el largo de request.vars es mayor a cero, quiere decir que de introdujo informacion en el formulario.
            if len(request.vars) != 0:
                # En usbidAux almacenamos el usbid proporcionado por el administrador
                # En buscarUser revisamos si el usuario a agregar efectivamente esta en el CAS
                usbidAux = request.vars.usbid
                buscasUser = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ usbidAux +" |grep numEntries")

                if buscasUser.read() == '':
                    message = T("El usuario no esta registrado en el CAS")
                else:
                    user = get_ldap_data(usbidAux)
                    telefonoAux = request.vars.telefono
                    correo_alterAux = request.vars.correo_alter
                    tipoAux = request.vars.tipo
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

                    # Primero verificamos que el usuario que intenta agregarse no esta en la base de datos
                    if db(db.USUARIO.usbid == usbidAux).isempty():
                        # Luego de insertar al usuario, mostramos un formulario al administrador con los datos de la persona agregada
                        form = SQLFORM.factory(
                            Field("USBID", default=datosCompAux[0],writable = False),
                            Field('Nombres',default=datosCompAux[1],writable = False),
                            Field('apellidos', default=datosCompAux[2],writable=False),
                            readonly=True)
                        if len(tipoAux) >= 3:
                        # Lo insertamos en la base de datos.
                            db.USUARIO.insert(ci=user["cedula"],
                                    usbid=usbidAux,
                                    nombres=datosCompAux[1],
                                    apellidos=datosCompAux[2],
                                    correo_inst=user["email"],
                                    telefono = telefonoAux,
                                    correo_alter = correo_alterAux,
                                    tipo = tipoAux)
                            return dict(form = form, message = message, bool = 1, admin=get_tipo_usuario())
                        else:
                            message = T("Debe Especificar un Tipo")

                    else:
                        message= T("El usuario ya esta registrado")
            return dict(form = forma,message = message, admin=get_tipo_usuario())
        else:
            redirect(URL("perfil"))
    else:
        redirect(URL("index"))

def eliminar():
    if session.usuario != None:
        if session.usuario["tipo"] == "Bloqueado":
            redirect(URL("index"))
        if session.usuario["tipo"] == "Administrador":
            if len(request.args)!=0 :
                if request.args[0] != session.usuario["usbid"]:
                    session.message = ""
                    print request.args[0]
                    if (not db(db.USUARIO.usbid == request.args[0]).isempty()):
                        db(db.USUARIO.usbid == request.args[0]).delete()
                        redirect(URL('gestionar'))
                else:
                    session.message = T("Para eliminar su cuenta, por favor comuníquese con un administrador")
                    redirect(URL('gestionar'))
        else:
            redirect(URL("perfil"))
    else:
        redirect(URL("index"))

def modificar():
    admin = get_tipo_usuario()

    if admin == 1:
        message= ""
        form = SQLFORM.factory(
                        Field("USBID", default=request.args[0],writable = False),
                        readonly=True)

        forma=SQLFORM(
                db.USUARIO,
                button=['Actualizar'],
                fields=['tipo'],
                labels={'tipo':'TIPO'})
        forma.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
        forma.element(_type='submit')['_value']="Actualizar"

        if len(request.vars)!=0:
            if (not db(db.USUARIO.usbid == request.args[0]).isempty()):
                if(request.args[0] != session.usuario["usbid"]):
                    db(db.USUARIO.usbid == request.args[0]).update(tipo = request.vars.tipo)
                    redirect(URL('gestionar'))
                else:
                    message = T("Para cambiar sus permisos, por favor comuníquese con un administrador")
            else:
                message = T("El Usuario no se encuentra registrado")

        return dict(forma = form, form = forma, message = message, admin=get_tipo_usuario())
    else:
        redirect(URL(c ="default",f="perfil"))

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
            redirect(URL(c ="default",f="perfil"))
    else:
        redirect(URL(c ="default",f="index"))

    return admin
