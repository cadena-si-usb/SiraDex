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
from funciones_siradex import get_tipo_usuario

def gestionar():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

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
                                Field('asunto', type="string", requires=[IS_LENGTH(50)]),
                                Field('mensaje', type="text", requires=[IS_NOT_EMPTY(error_message='El mensaje no puede estar vacio')]),
                                Field('usbid', type="string"),
                                submit_button = 'Enviar')

    hayErrores = {}

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

        session.message = 'Correo enviado satisfactoriamente'
        redirect(URL('gestionar'))

    # En caso de que el formulario no sea aceptado
    elif formulario_contactar.errors:
          hayErrores = formulario_contactar.errors

    return dict(form_editar=form_editar, hayErrores=hayErrores, formulario_contactar=formulario_contactar,usuarios = aux,message = message, admin=get_tipo_usuario(session))

def agregar():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

    message = ""
    forma=SQLFORM.factory(
        Field('usbid',
               requires=[IS_NOT_EMPTY(error_message='El USBID no puede quedar vacío.')]),
        Field('telefono',
               requires=[IS_NOT_EMPTY(error_message='El teléfono no puede quedar vacío.'),
                         IS_LENGTH(20),
                         IS_MATCH('^[0-9]+$', error_message="Use sólo números.")]),
        Field('correo_alter',
               requires=[IS_NOT_EMPTY(error_message='El correo no puede quedar vacío.'),
                         IS_MATCH('^[A-z0-9À-ÿŸ\s-]*$', error_message="Use solo letras, el caracter '-' y números.")]),
        Field('tipo',
               requires=IS_IN_SET({'Usuario':'Usuario', 'DEX':'DEX', 'Administrador':'Administrador', 'Bloqueado':'Bloqueado'},
                                                    zero=T('Seleccione...'),
                                                    error_message = 'Debes elegir un tipo de usuario')),
        submit_button='Agregar',
        labels={'usbid':'USBID','telefono':'Teléfono', 'correo_alter':'Correo alternativo','tipo':'Tipo'}
        )
    
    """
    forma=SQLFORM(                              # Se hace un formulario para introducir un USBID.
        db.USUARIO,
        button=['Agregar'],
        fields=['usbid','tipo','telefono','correo_alter'],
        submit_button='Agregar',
        labels={'usbid':'USBID','telefono':'Teléfono', 'correo_alter':'Correo alternativo','tipo':'Tipo'})
    """
    
    # Estilo del boton
    forma.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    forma.element(_type='submit')['_value']="Agregar"
    
    if forma.accepts(request.vars, session,formname="forma"):
        
        # En usbidAux almacenamos el usbid proporcionado por el administrador
        # En buscarUser revisamos si el usuario a agregar efectivamente esta en el CAS
        usbidAux = request.vars.usbid
        buscasUser = os.popen("ldapsearch -x -h ldap.usb.ve -b \"dc=usb,dc=ve\" uid="+ usbidAux +" |grep numEntries")
        
        if buscasUser.read() == '':
            message = T("El usuario no esta registrado en el CAS")
        else:
            user = get_ldap_data(usbidAux)
            print(user)
            print("----\n")
            telefonoAux = request.vars.telefono
            correo_alterAux = request.vars.correo_alter
            tipoAux = request.vars.tipo
            
            
            # Primero verificamos que el usuario que intenta agregarse no esta en la base de datos
            if db(db.USUARIO.usbid == usbidAux).isempty():
                # Luego de insertar al usuario, mostramos un formulario al administrador con los datos de la persona agregada
                form = SQLFORM.factory(
                    Field("USBID", default=usbidAux,writable = False),
                    Field('Nombres',default=user["first_name"],writable = False),
                    Field('Apellidos', default=user["last_name"],writable=False),
                    readonly=True)
                if len(tipoAux) >= 3:
                # Lo insertamos en la base de datos.
                    db.USUARIO.insert(ci=user["cedula"],
                            usbid=usbidAux,
                            nombres=user["first_name"],
                            apellidos=user["last_name"],
                            correo_inst=user["email"],
                            telefono = telefonoAux,
                            correo_alter = correo_alterAux,
                            tipo = tipoAux)
                    return dict(form = form, message = message,errores=forma.errors, bool = 1, admin=get_tipo_usuario(session))
                else:
                    message = T("Debe Especificar un Tipo")
                
            else:
                message= T("El usuario ya esta registrado")
        
    else:
        print("ERRORES: ",forma.errors)
            
    return dict(form = forma,message = message,errores=forma.errors, admin=get_tipo_usuario(session))


def eliminar():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

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

def modificar():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

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

    return dict(forma = form, form = forma, message = message, admin=get_tipo_usuario(session))
