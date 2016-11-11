import os
import datetime
from funciones_siradex import get_tipo_usuario
import time

def index():
	admin = get_tipo_usuario(session)
	backups = db(db.BACKUP).select()

	form = construir_formulario_generar_backup()

	if form.accepts(request.vars, session,formname="form"):

		id_backup = db.BACKUP.insert(fecha=str(datetime.date.today()),
						descripcion=request.vars.Descripcion)
		archivo = "backup_" + str(id_backup["id_backup"]) + ".sql"



		comando = "pg_dump -d Siradex -U Siradex -h localhost -w > ./applications/SiraDex/backup/" + archivo
		comando2 = "pwd"
		resp2 = os.system(comando2)
		resp = os.system(comando)

	return locals()

def generar_backup():

	fecha = time.asctime(time.localtime(time.time()))

	archivo = fecha.split()[4:19] + ".sql"

	comando = "pg_dump -d Siradex -U Siradex -h localhost -w > " + archivo
	resp = os.system(comando)

def restaurar_backup():

	fields = []

	fields.append(Field("backup", 'upload', autodelete=True, uploadfolder=os.path.join(request.folder,'uploads'), label=''))

	form=SQLFORM.factory(*fields, upload=url) 
    form.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
    form.element(_type='submit')['_value']="Agregar"

    if form.process().accepted:

    	print form.vars.backup.filename

        redirect(URL('index'))

    elif form.errors:
        response.flash = 'el formulario tiene errores'

	#archivo = "backup_" + id_backup + ".sql"

	#comando = "pg_dump -d Siradex -U Siradex -h localhost -w < " + archivo

	#resp = os.system(comando)

	return locals()