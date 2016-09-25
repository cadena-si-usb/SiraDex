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


2. WEB2PY
################################################################################

Bajar y descomprimir web2py en el directorio de preferencia.

Copiar el contenido del repositorio en la carpeta web2py/applications/ dentro
de un nuevo directorio llamado SiraDex.


3. REQUERIMIENTOS PYTHON
################################################################################

Asegurarse de tener python 2.7 y la version de pip para python 2.7

    $ pip -v
    // Algunas veces tambien esta instalado pip para python 3, en este caso
    // probar con pip2

Ir al directorio SiraDex e instalar las librerias con

    $ sudo pip install -r requirements.txt

1. BASE DE DATOS
################################################################################

Instalar PostgreSQL desde el terminal.

    $ sudo apt-get install postgresql postgresql-client

Iniciar sesion como usuario postgres y crear la base de datos Siradex

    $ sudo -su postgres
    $ createdb Siradex

Crear el usuario Siradex y garantizar el acceso a la base de datos.

    $ psql
    $ CREATE USER Siradex WITH PASSWORD 'Siradex';
    $ GRANT ALL PRIVILEGES ON DATABASE "Siradex" TO "Siradex";

Cuando este listo el script SQL, se subira el esquema. Mientras tanto, se usan
las definiciones directas de web2py. Antes del paso 4, primero borrar todos los
archivos .table que se encuentren en SiraDex/databases.
Luego del paso cuatro, ingresar en postgress y verificar que las tablas esten
creadas.

    $ psql
    $ \c Siradex
    $ \d (listara todas las tablas)

Hasta ahora, las tablas que deben aparecer son:

                    List of relations
    Schema |          Name          |   Type   |  Owner
    --------+------------------------+----------+---------
    public | act_posee_campo        | table    | Siradex
    public | actividad              | table    | Siradex
    public | auth_cas               | table    | Siradex
    public | auth_cas_id_seq        | sequence | Siradex
    public | auth_event             | table    | Siradex
    public | auth_event_id_seq      | sequence | Siradex
    public | auth_group             | table    | Siradex
    public | auth_group_id_seq      | sequence | Siradex
    public | auth_membership        | table    | Siradex
    public | auth_membership_id_seq | sequence | Siradex
    public | auth_permission        | table    | Siradex
    public | auth_permission_id_seq | sequence | Siradex
    public | auth_user              | table    | Siradex
    public | auth_user_id_seq       | sequence | Siradex
    public | campo                  | table    | Siradex
    public | campo_catalogo         | table    | Siradex
    public | catalogo               | table    | Siradex
    public | catalogo_tiene_campo   | table    | Siradex
    public | gestiona_catalogo      | table    | Siradex
    public | gestiona_tipo_act      | table    | Siradex
    public | jefe_dependencia       | table    | Siradex
    public | log_siradex            | table    | Siradex
    public | participa_act          | table    | Siradex
    public | permisos_tipo_act      | table    | Siradex
    public | tiene_campo            | table    | Siradex
    public | tipo_actividad         | table    | Siradex
    public | usbid                  | table    | Siradex
    public | usuario                | table    | Siradex
    public | valores_campo_catalogo | table    | Siradex

4. EJECUCION
################################################################################

Ir al directorio web2py y ejecutar:

    $ python web2py.py

Si no hay errores, el sistema empezara a correr en:

    http://127.0.0.1:8000/SiraDex/

Verificar cualquier error y revisar la Base de Datos para ver si las tablas
estan correctamente creadas.

################################################################################
Ult. Modificacion: 25/09/2016
por Leonardo Martinez (martinezazuaje@gmail.com)
################################################################################
