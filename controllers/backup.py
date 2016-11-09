import os
import datetime
from gluon import *


def get_tipo_usuario():

    # Session Actual
    if session.usuario != None:
      if session.usuario["tipo"] == "DEX" or session.usuario["tipo"] == "Administrador":
        if(session.usuario["tipo"] == "DEX"):
          admin = 2
        elif(session.usuario["tipo"] == "Administrador"):
          admin = 1
        else:
          admin = 0
      else:
        admin = -10
    else:
      admin = -1
    return admin


def index():
	admin = get_tipo_usuario()
	backups = db(db.BACKUP).select()

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

def construir_formulario_generar_backup():

    formulario_generar_backup = SQLFORM.factory(
                        Field('Descripcion', type="text",
                              requires = [IS_NOT_EMPTY(error_message='La descripción del backup no puede quedar vacía.'),
                                          IS_LENGTH(256)]),
                        submit_button = 'Agregar',
                        labels = {'Descripcion' : 'Descripción'}
                )
    return formulario_generar_backup