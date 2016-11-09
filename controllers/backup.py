import os

def index():

	backups = db(db.BACKUP).select()

	return locals()

def generar_backup():

	id_backup = db.BACKUP.insert(nombre=archivo,
						fecha=,
						descripcion=)


	archivo = "backup_" + id_backup + ".sql"
	comando = "pg_dump -d Siradex -U Siradex -h localhost -w > " + archivo
	resp = os.system(comando)


def restaurar_backup():

	id_backup = request.args[0]

	archivo = "backup_" + id_backup + ".sql"

	comando = "pg_dump -d Siradex -U Siradex -h localhost -w < " + archivo

	resp = os.system(comando)
	

