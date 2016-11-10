import os
import datetime
from funciones_siradex import get_tipo_usuario

def construir_formulario_generar_backup():

    formulario_generar_backup = SQLFORM.factory(
                        Field('Descripcion', type="text",
                              requires = [IS_NOT_EMPTY(error_message='La descripción del backup no puede quedar vacía.'),
                                          IS_LENGTH(256)]),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción'}
                )
    return formulario_generar_backup

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

	formulario_generar_backup = construir_formulario_generar_backup()

	archivo = "backup_" + id_backup + ".sql"

	if formulario_generar_backup.accepts(request.vars, session,formname="formulario_generar_backup"):

		id_backup = db.BACKUP.insert(nombre=archivo,
						fecha=datetime.date.today(),
						descripcion=request.vars.Descripcion)



		comando = "pg_dump -d Siradex -U Siradex -h localhost -w > " + archivo
		resp = os.system(comando)

def restaurar_backup():

	id_backup = request.args[0]

	archivo = "backup_" + id_backup + ".sql"

	comando = "pg_dump -d Siradex -U Siradex -h localhost -w < " + archivo

	resp = os.system(comando)