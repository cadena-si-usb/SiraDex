################################################################################
                      INSTALACION EN AMBIENTE DE DESSARROLLO
################################################################################

0. CONSIDERACIONES
################################################################################

  - SISTEMA OPERATIVO: Linux.
  - PYTHON: Python 2.7
  - PIP: Para python v2.
  - WEB2PY: Ultima version de la pagina https://www.web2py.com/
  - BASE DE DATOS: PostgreSQL


1. WEB2PY
################################################################################

Bajar y descomprimir web2py en el directorio de preferencia.

Copiar el contenido del repositorio en el directorio web2py/applications/ dentro
de una nueva carpeta llamada SiraDex.


2. REQUERIMIENTOS PYTHON
################################################################################

Asegurarse de tener python 2.7 y la version de pip para python 2.7

    $ pip -v
    // Algunas veces tambien esta instalado pip para python 3, en este caso
    // probar con pip2

Ir al directorio SiraDex e instalar las librerias con

    $ sudo pip install -r requirements.txt.sls

3. BASE DE DATOS
################################################################################

Instalar PostgreSQL desde el terminal.

    $ sudo apt-get install postgresql postgresql-client

Dirigirse al directorio SiraDex/SQLScripts. Verificar que existen los archivos:

    - dropSIRADEX.sql
    - schemaSIRADEX.sql

Iniciar sesion como usuario postgres y crear la base de datos Siradex

    $ sudo -su postgres
    $ createdb Siradex

Crear el usuario Siradex y garantizar el acceso a la base de datos.

    $ psql
    $ CREATE USER "Siradex" WITH PASSWORD 'Siradex';
    $ GRANT ALL PRIVILEGES ON DATABASE "Siradex" to "Siradex";

Salir y entrar en la base de datos Siradex como usuario Siradex

    $ \q
    $ psql -d Siradex -U Siradex (recordar que el password es: Siradex)

    ###########################################################
    NOTA IMPORTANTE:
    Si este paso da error de Autenticacion con PEER,
    leer el punto de Errores al final de estas instrucciones
    antes de continuar.
    ###########################################################

Cargar los scrips de la base de datos:

    #Si se esta creando la base de datos por primera vez:

    $ \i schemaSIRADEX.sql

    #Si se esta actualizando/reinicializando por errores etc:

    $ \i dropSIRADEx.sql
    $ \i schemaSIRADEx.sql

Verificar que todas las tablas se han creado:

    $ \d (listara todas las tablas)

Hasta ahora, las tablas que deben aparecer son:

                          List of relations
    Schema |              Name               |   Type   |  Owner
    --------+---------------------------------+----------+---------
    public | act_posee_campo                 | table    | Siradex
    public | actividad                       | table    | Siradex
    public | actividad_id_actividad_seq      | sequence | Siradex
    public | campo                           | table    | Siradex
    public | campo_catalogo                  | table    | Siradex
    public | campo_catalogo_id_campo_cat_seq | sequence | Siradex
    public | campo_id_campo_seq              | sequence | Siradex
    public | catalogo                        | table    | Siradex
    public | catalogo_id_catalogo_seq        | sequence | Siradex
    public | catalogo_tiene_campo            | table    | Siradex
    public | gestiona_catalogo               | table    | Siradex
    public | gestiona_tipo_act               | table    | Siradex
    public | log_siradex                     | table    | Siradex
    public | participa_act                   | table    | Siradex
    public | programa                        | table    | Siradex
    public | programa_id_programa_seq        | sequence | Siradex
    public | tiene_campo                     | table    | Siradex
    public | tipo_actividad                  | table    | Siradex
    public | tipo_actividad_id_tipo_seq      | sequence | Siradex
    public | usbid                           | table    | Siradex
    public | usuario                         | table    | Siradex
    public | valores_campo_catalogo          | table    | Siradex



Nos salimos de postgres
	$ \q
	$ exit

Instalamos ldap
	$ sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils
	$ pip install ldap

	Si la linea anterior da error probar: sudo pip install python-ldap

Instalamos pygal
	$ pip install pygal

Revisar el nombre de la carpeta
  El nombre TIENE que ser SiraDex, si no es asi hacer:
    mv <nombre_actual>/ SiraDex/


################################################################################
################################# IMPORTANTE ###################################
################################################################################
Si estas trabajando en local:
    En controllers/default:
      Comentar la linea de URL_RETORNO del servidor y descomentar la del entorno
      de desarroll0: 
          # URLS DE RETORNO PARA EL CAS ##
          # PARA EL SERVIDOR:
          # URL_RETORNO = "http%3A%2F%2Fsiradex.dex.usb.ve%2Fdefault%2Flogin_cas"
          # PARA DESSARROLLO. Cambiar el puerto 8000 si es necesario.
          URL_RETORNO = "http%3A%2F%2Flocalhost%3A8000%2FSiraDex%2Fdefault%2Flogin_cas"

    En views/layoutSIRADEXloged.html:
      Comentar el enlace del servidor y descomentar el del desarrollo:
          <!-- EN SERVIDOR -->
                    <!--<a  id = login
                      class ='btn btn-xs'
                      href='http://secure.dst.usb.ve/login?service=http%3A%2F%2Fsiradex.dex.usb.ve%2Fdefault%2Flogin_cas'> -->
          <!-- EN DESARROLLO -->
                    <a  class ='btn btn-xs '
                      href='http://secure.dst.usb.ve/login?service=http%3A%2F%2Flocalhost%3A8000%2FSiraDex%2Fdefault%2Flogin_cas'> 

4. EJECUCION
################################################################################

Ir al directorio web2py y ejecutar:

    $ python web2py.py

Si no hay errores, el sistema empezara a correr en:

    http://127.0.0.1:8000/SiraDex/

Verificar cualquier error y reportarlo como Issue en el repo de GitHub:

    https://github.com/cadena-si-usb/SIRADEX/issues/

5. ERRORES FRECUENTES
################################################################################

ERROR:

  FATAL: Peer authentication failed for user "Siradex"

SOL:
  a. Crear password para postgres:

        $ sudo -su postgres
        $ psql (EN ESTE PASO TOMAR NOTA DE LA VERSION DE POSTGRES, Ej. 9.3)
        $ ALTER USER postgres WITH PASSWORD 'tupassword';

  b. Salir de postgres y editar el archivo 'pg_hba.conf'

        $ sudo gedit /etc/postgresql/X.X/main/pg_hba.conf
          (Donde X.X e la version de postres, Ej. 9.3)

     cambiar en el archivo las siguientes lineas:

       local    all   postgres    peer
       local    all   all         peer

     por:

       local    all   postgres    md5
       local    all   all         md5

      y guardar el archivo.

   c. Reiniciar Postgres.

        $ sudo service postgresql restart

################################################################################
Ult. Modificacion: 28/09/2016
por Leonardo Martinez (martinezazuaje@gmail.com)
################################################################################
