# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from gluon import current
import os

'''
  Define funciones principales para enviar notificaciones via correo electronico
  en el sistema.

  Cuenta donde seran enviadas las notificaciones:
        email: usbsiradex@gmail.com
        pass:  SiradexUSB2016
'''

'''
    Envia un correo que indica que una producto fue validado.
    Parametros:
        mail     = configuracion de web2py de correo.
        usuario  = {email, nombres}
        producto = {nombre}
'''

def enviar_correo_validacion(mail, usuario, producto):

    email  = usuario['email']
    asunto = '[SIRADEX] Producto Aprobado'

    # Mensaje del Correo

    mensaje  = '''<h1>Estimado/a %(nombres)s:</h1>
                  <p>Nos complace indicarle que su Producto de Extensión
                        <b> %(nombreProducto)s</b>
                        fue aprobado satisfactoriamente por el Decanato de Extensión.
                  </p>
                  <p>
                     Recuerde que siempre puede ver el estado de este y sus otros productos
                     iniciando sesión en el <a href="https://siradex.dex.usb.ve/SiraDex">SIDADEX.</a>
                  </p>
                  <p> Saludos cordiales.</p>
               '''  % {'nombres': usuario['nombres'], 'nombreProducto' : producto['nombre']}

    body   =  get_plantilla_html(mensaje)

    mail.send(email, asunto, body)

'''
    Envia un correo que indica si una producto fue rechazado.
    Parametros:
        Usuario  = [email, nombre]
        Producto = [nombre]
        Razon    = ''
'''
def enviar_correo_rechazo():
    pass


# Define la plantilla html del correo electronico.
# con el campo mensaje dependiendo del tipo sdel correo que se quiere.
def get_plantilla_html(mensaje):

    usb_logo_url = os.path.join(current.request.folder, 'static/images','usblogo.png')

    plantilla = '''
        <html>
          <head>
            <meta charset = "UTF-8">
            <style>

              header, body, footer {
                display: block;
                font-family: "Helvetica";
              }

              header {
                color: black;
              }

              hr {
                color: #333333;
                margin-top: 15px;
              }

              img {
                  float: none;
                  width: 100px;
               }
               h1 {
                 font-size: 20px;
                 margin: 2px;
               }
               h2 {
                 font-size: 15px;
                 margin: 2px;
               }

               .bottom-msg {
                    margin-top: 20px;
                    font: 10px verdana, arial, helvetica, sans-serif;
                    color: black;
               }

               footer{
                 background-color: #333333;
                 padding-top: 3px;
                 padding-bottom: 3px;
                 font: 10px verdana, arial, helvetica, sans-serif;
                 color: #FFFFFF;
               }
            </style>
          </head>

          <header>
            <center>
              <img src='%(urlimg)s'>
              <h1>Universidad Simón Bolívar</h1>
              <h2>Decanato de Extensión</h2>
              <h2>Sistema de Registro de Actividades de Extensión SIRADEX</h2>
            </center>
            <hr>
          </header>

          <body>
            %(mensaje)s

            <div class='bottom-msg'>
                <center>
                    <p> Este mensaje fue enviado de manera automatica por el Sistema SIRADEX</p>
                    <p> Por favor no responda a este correo. En caso de duda o comentarios póngase en contacto con el Decanato de Extensión.</p>
                </center>
            </div>
          </body>

          <footer>
            <center>
              <p>Sartenejas, Baruta, Edo. Miranda - Apartado 89000 Cable Unibolivar Caracas Venezuela. Teléfono +58 0212-9063111</p>
              <p>Litoral. Camurí Grande, Edo. Vargas Parroquia Naiguatá. Teléfono +58 0212-9069000</p>
            </center>
          </footer>
        </html>
    ''' % {'urlimg' : usb_logo_url, 'mensaje': mensaje}

    return plantilla
