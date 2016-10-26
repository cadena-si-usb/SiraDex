# -*- coding: utf-8 -*-
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
    body   =  get_plantilla_html()

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


def get_plantilla_html():

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
              <img src='http://www.usb.ve/conocer/corporativa/archivos/logos/logo/logo.png'>
              <h1>Universidad Simón Bolívar</h1>
              <h2>Decanato de Extensión</h2>
              <h2>Sistema de Registro de Actividades de Extensión SIRADEX</h2>
            </center>
            <hr>
          </header>

          <body>
            <p> Mensaje </p>
          </body>

          <footer>
            <center>
              <p>Sartenejas, Baruta, Edo. Miranda - Apartado 89000 Cable Unibolivar Caracas Venezuela. Teléfono +58 0212-9063111</p>
              <p>Litoral. Camurí Grande, Edo. Vargas Parroquia Naiguatá. Teléfono +58 0212-9069000</p>
            </center>
          </footer>
        </html>
    '''

    return plantilla
