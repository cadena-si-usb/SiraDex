# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os
import datetime
import re
from usbutils import get_ldap_data, random_key
import urllib2
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

## URLS DE RETORNO PARA EL CAS ##
## Solo descomentar segun sea el caso.
## PARA EL SERVIDOR:
URL_RETORNO = "http%3A%2F%2Fsiradex.dex.usb.ve%2Fdefault%2Flogin_cas"
## PARA DESSARROLLO. Cambiar el puerto 8000 si es necesario.
#URL_RETORNO = "http%3A%2F%2Flocalhost%3A8000%2FSiraDex%2Fdefault%2Flogin_cas"

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
            redirect(URL(c ="default",f="perfil"))
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
        "&service=" + URL_RETORNO

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
        print '~~>',usbid

        usuario = get_ldap_data(usbid) #Se leen los datos del CAS
        print '~~>',usuario

        tablaUsuarios = db.USUARIO

        session.usuario = usuario
        session.usuario['usbid'] = usbid
        #print '~>',usuario['tipo']
        try:
            print usuario['carrera']
        except:
            print('Es una esceocion')
        if not db(tablaUsuarios.usbid == usbid).isempty():
            datosUsuario = db(tablaUsuarios.usbid==usbid).select()[0]
            session.usuario['tipo'] = datosUsuario.tipo
            session.usuario['alternativo'] = datosUsuario.correo_alter

            session.usuario['phone'] = datosUsuario.telefono

            
            if datosUsuario.tipo == "Bloqueado":
                response.flash = T("Usuario bloqueado")
                redirect(URL(c = "default",f="index"))
            else:
                redirect(URL('perfil'))
        else:
            session.usuario['tipo'] = "Usuario"
            session.usuario['alternativo'] = None

            db.USUARIO.insert(ci=session.usuario["cedula"],  # Lo insertamos en la base de datos.
            usbid=session.usuario["usbid"],
            nombres=session.usuario["first_name"],
            apellidos=session.usuario["last_name"],
            correo_inst=session.usuario["email"],
            correo_alter= None,
            telefono=session.usuario["phone"],
            tipo = "Usuario")
            redirect(URL('vRegistroUsuario'))

def logout_cas():
    session.usuario = None
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
            redirect(URL('perfil'))        # Redirige al usuario al menu principal.
        return dict(form1 = form, form = forma, admin=get_tipo_usuario())
    else:
        redirect(URL("index"))

def perfil():
    if session.usuario != None:

    	if session.usuario["tipo"] == "Bloqueado":
    	    redirect(URL("index"))

        print session.usuario
        admin = 4
        if(session.usuario["tipo"] == "DEX"):
            admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
            admin = 1
        else:
            admin = 0

        correo_i = session.usuario["usbid"]+"@usb.ve"

        form = SQLFORM.factory(
            Field("USBID", default=session.usuario["usbid"],writable = False),
            Field('Nombres',default=session.usuario["first_name"],writable = False),
            Field('Apellidos', default=session.usuario["last_name"],writable=False),
            Field('Correo_Institucional', default=correo_i,writable=False),
            Field('Telefono',label = "Teléfono", default=session.usuario["phone"],writable=False),
            Field('Correo_Alternativo', default=session.usuario["alternativo"],writable=False),
            readonly=True)

        rows = db(db.PRODUCTO.ci_usu_creador==session.usuario['cedula']).select()
        productos = {
                    "Validados":[],
                    "Rechazados":[],
                    "En espera":[]
                    }

        grafica = URL('default','grafica')

        for row in rows:
            if row.estado == "Validada":
                productos["Validados"] += [row]
            elif row.estado == "Rechazada":
                productos["Rechazados"]+= [row]
            else:
                productos["En espera"] += [row]

        return locals()
    else:
        redirect(URL("index"))

def grafica():

        query = "select programa.nombre, programa.abreviacion, count(producto.nombre)" + \
        " from ((programa inner join tipo_actividad on programa.id_programa=tipo_actividad.id_programa)" + \
        " inner join producto on producto.id_tipo=tipo_actividad.id_tipo and producto.ci_usu_creador=\'"+ session.usuario["cedula"] +\
        "\' and producto.estado=\'Validada\') group by programa.nombre, programa.abreviacion;"

        query2 = "select count(producto.nombre) from producto where producto.ci_usu_creador=\'"+ session.usuario["cedula"]+"\' and producto.estado=\'Validada\';"

        datos = db.executesql(query)
        num_productos = db.executesql(query2)[0][0]

        import pygal
        pie_chart = pygal.Pie(height=300, width=400,background = 'red')
        #pie_chart.title = 'Productos del usuario'
        for producto in datos:
            porcentaje = (producto[2]*100)//num_productos
            pie_chart.add(producto[1],[{'value':porcentaje, 'label':producto[0]}])
        return pie_chart.render()

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
            redirect(URL("perfil"))
    else:
        redirect(URL("index"))

def EditarPerfil():
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
        

        # Modificar datos del perfil
        usuario = db(db.USUARIO.ci==session.usuario['cedula']).select().first()

        forma=SQLFORM(
            db.USUARIO,
            record=usuario,
            
            fields=['telefono','correo_alter'],

            
            labels={'telefono':'Teléfono', 'correo_alter':'Correo alternativo'})
        forma.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
        forma.element(_type='submit')['_value']="Actualizar"

        
        if request.vars:
            nuevoTelefono = request.vars.telefono
            nuevoCorreoAlter = request.vars.correo_alter
            
            valor_telefono = None if ((nuevoTelefono == "") | (nuevoTelefono== None)) else nuevoTelefono
            session.usuario["phone"] = valor_telefono

            valor_correo = None if ((nuevoCorreoAlter == "") | (nuevoCorreoAlter== None)) else nuevoCorreoAlter
            session.usuario["alternativo"] = valor_correo
            
            db(db.USUARIO.ci == session.usuario["cedula"]).update(telefono=valor_telefono, correo_alter=valor_correo)
            
            print "\n\nEl nuevo usuario quedo: "
            print session.usuario
            redirect(URL('perfil'))

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
            redirect(URL("perfil"))
    else:
        redirect(URL("index"))

def index():
    if session.usuario != None:
      if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
        if(session.usuario["tipo"] == "DEX"):
          admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
          admin = 1
        else:
          admin = 0
      else:
        admin = -1
    else:
      admin = -1
    
    now = datetime.datetime.now()
    if now.month < 10 :
        mes = "-0" +  str(now.month)
    else:
        mes = "-" +  str(now.month)
    if now.day < 10 :
        dia = "-0" +  str(now.day)
    else:
        dia = "-" +  str(now.month)
    fecha = str(now.year) + mes + dia
    rows = db(db.PROGRAMA.papelera == False).select().as_list()
    rowsT = db(db.TIPO_ACTIVIDAD.papelera == False).select().as_list()
    return locals()

def obtener_actividades():

    if request.vars.Programa=="all":
        tiposA = db(db.TIPO_ACTIVIDAD).select()
    else:
        tiposA = db(db.TIPO_ACTIVIDAD.id_programa==int(request.vars.Programa)).select()
    
    concat = '<option value="all" selected="">--cualquiera--</option>'

    for tipo in tiposA:
        option = tipo.nombre
        concat += '<option value="'+str(tipo.id_tipo)+'">'+option+'</option>'

    return "jQuery('#lista_tipos').empty().append('"+concat+"')"

