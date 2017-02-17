import os
import datetime
from funciones_siradex import get_tipo_usuario
from log import insertar_log
import time

def index():
    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

    backups = os.listdir("./applications/SiraDex/backup")

    # form = 

    # if form.process(formname = "form", table_name='archivos').accepted:

    #     print form.vars.backup
    # #        comando = "psql -d Siradex -U Siradex -h localhost -w < ./applications/SiraDex/backup/" + archivo

    # #        resp = os.system(comando)

        redirect(URL('index'))

    elif form.errors:
        session.flash = 'el formulario tiene errores'


    return locals()

def generar_backup():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))


    fecha = time.asctime(time.localtime(time.time()))
    archivo = "_".join(fecha.split()[1:]).replace(":","") + ".sql"
    comando = "pg_dump --dbname=postgres://Siradex:Siradex@localhost/Siradex -w > ./applications/SiraDex/backup/backup_" + archivo
    resp = os.system(comando)
    session.flash = "Backup generado exitosamente"
    insertar_log(db, 'BACKUP', datetime.datetime.now(), request.client, 'GENERACION DE BACKUP EXITOSA', session.usuario['usbid'])
    redirect(URL('index'))

def restaurar_backup():

    admin = get_tipo_usuario(session)

    if (admin==0 or admin==2):
        redirect(URL(c ="default",f="index"))

    archivo = request.args[0]

    comando = "psql --dbname=postgres://Siradex:Siradex@localhost/Siradex -w < ./applications/SiraDex/SQLScripts/dropSIRADEx.sql && psql --dbname=postgres://Siradex:Siradex@localhost/Siradex -w < ./applications/SiraDex/backup/" + archivo

    resp = os.system(comando)
    #resp = 0
    if (resp == 0):
        insertar_log(db, 'BACKUP', datetime.datetime.now(), request.client, 'RESTAURACION DEL SISTEMA DESDE DE BACKUP EXITOSA', session.usuario['usbid'])
        session.flash="Restaurado."
    else:
        insertar_log(db, 'BACKUP', datetime.datetime.now(), request.client, 'RESTAURACION DEL SISTEMA DESDE DE BACKUP FALLIDA', session.usuario['usbid'])
        session.flash="No se pudo restaurar."

    redirect(URL('index'))



def download():
    return response.download(request, db)

def eliminar():
    archivo = request.args[0]
    comando = "rm ./applications/SiraDex/backup/" + archivo
    resp = os.system(comando)
    insertar_log(db, 'BACKUP', datetime.datetime.now(), request.client, 'ELIMINACION DE BACKUP', session.usuario['usbid'])
    session.flash="Backup eliminado exitosamente"
    redirect(URL('index'))


def descargar_backup():
    nombre_archivo = str(request.args[0])
    direccion = os.path.join('applications','SiraDex','backup',nombre_archivo)
    response.headers['ContentType'] ="application/octet-stream"
    response.headers['Content-Disposition']= "attachment; filename=" + nombre_archivo
    insertar_log(db, 'BACKUP', datetime.datetime.now(), request.client, 'DESCARGA DE BACKUP', session.usuario['usbid'])
    return response.stream(open(direccion),chunk_size=4096)
