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

def backup_aut():
    dia = request.vars.dias_automatizar
    hora = request.vars.hora
    activar = request.vars.activar
    modo = request.vars.modo

    fecha = time.asctime(time.localtime(time.time()))
    archivo = "_".join(fecha.split()[1:]).replace(":","") + ".sql"

    if activar == None:
        os.system("crontab -r")
    else:
        comando = "pg_dump --dbname=postgres://Siradex:Siradex@localhost/Siradex -w > ./applications/SiraDex/backup/backup_" + archivo

        if modo == "mensual":
            crontab_line = "* " + str(hora) + " 1 * * " + comando

        elif modo == "diario":
            crontab_line = "* " + str(hora) + " * * * " + comando

        else:
            crontab_line = "* " + str(hora) + " " + str(dia) + " * * " + comando



        echo_crontab_file = "echo \"" + crontab_line + "\" > ./applications/SiraDex/backup/auto_backup_file.txt"
        print echo_crontab_file
        os.system(echo_crontab_file)
        os.system("crontab ./applications/SiraDex/backup/auto_backup_file.txt")

    redirect(URL('index'))
