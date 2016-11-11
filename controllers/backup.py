import os
import datetime
from funciones_siradex import get_tipo_usuario
import time

def index():
	admin = get_tipo_usuario(session)
	backups = db(db.BACKUP).select()

	form = restaurar_backup()

	if form.process().accepted:

		print form.vars.backup

		redirect(URL('index'))

	elif form.errors:
		response.flash = 'el formulario tiene errores'

#		comando = "psql -d Siradex -U Siradex -h localhost -w < ./applications/SiraDex/backup/" + archivo

#		resp = os.system(comando)

	return locals()

def generar_backup():

	fecha = time.asctime(time.localtime(time.time()))

	archivo = fecha.split()[4:19] + ".sql"

	comando = "pg_dump -d Siradex -U Siradex -h localhost -w ./applications/SiraDex/backup/ > " + archivo
	resp = os.system(comando)

def restaurar_backup():

	fields = []

	fields.append(Field("backup", 'upload', autodelete=True, uploadfolder="./applications/SiraDex/backup/", label=''))

	form=SQLFORM.factory(*fields,upload=URL('download')) 
	form.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
	form.element(_type='submit')['_value']="Agregar"



		#archivo = "backup_" + id_backup + ".sql"

		#comando = "psql -d Siradex -U Siradex -h localhost -w < " + archivo

		#resp = os.system(comando)

	return form

def download():
    return response.download(request, db)