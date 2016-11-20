import os
import datetime
from funciones_siradex import get_tipo_usuario
import time

url = 'http://localhost:8000/SiraDex'

def index():

    admin = get_tipo_usuario(session)
    
    if (admin==0 || admin==2):
      redirect(url)
      

	admin = get_tipo_usuario(session)
	backups = os.listdir("./applications/SiraDex/backup")

	form = formulario_restaurar_backup()

	if form.process(formname = "form", table_name='archivos').accepted:

		print form.vars.backup
#		comando = "psql -d Siradex -U Siradex -h localhost -w < ./applications/SiraDex/backup/" + archivo

#		resp = os.system(comando)

		redirect(URL('index'))

	elif form.errors:
		response.flash = 'el formulario tiene errores'


	return locals()

def generar_backup():

    admin = get_tipo_usuario(session)
    
    if (admin==0 || admin==2):
      redirect(url)
      

	fecha = time.asctime(time.localtime(time.time()))

	archivo = fecha.split()[4:19] + ".sql"

	comando = "pg_dump -d Siradex -U Siradex -h localhost -w ./applications/SiraDex/backup/ > " + archivo
	resp = os.system(comando)

def formulario_restaurar_backup():

    admin = get_tipo_usuario(session)
    
    if (admin==0 || admin==2):
      redirect(url)
      

	fields = []

	fields.append(Field("backup", 'upload',uploadfield=True, uploadfolder='./applications/SiraDex/backup/'))

	form=SQLFORM.factory(*fields) 
	form.element(_type='submit')['_class']="btn blue-add btn-block btn-border"
	form.element(_type='submit')['_value']="Agregar"

	return form

def restaurar_backup():

    admin = get_tipo_usuario(session)
    
    if (admin==0 || admin==2):
      redirect(url)
      
	archivo = request.args[0]

	#comando = "psql -d Siradex -U Siradex -h localhost -w < " + archivo

	#resp = os.system(comando)
	resp = 0
	if (resp == 0):
		response.flash="Restaurado."
	else:
		response.flash="No se pudo restaurar."

	redirect(URL('index'))
