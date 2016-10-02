# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('postgres://Siradex:Siradex@localhost/Siradex', pool_size = 10)
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
#raise HTTP(404)

tipo_campos = ['fecha', 'participante', 'ci', 'comunidad', 'telefono', 'texto','documento', 'imagen', 'cantidad entera', 'cantidad decimal']

#db.usuario.drop()
db.define_table('USUARIO',
    Field('ci',type='string',length=8, notnull=True,required=True, unique=True),
    Field('usbid', type='string', unique=True,notnull=True),
    Field('nombres',type='string',length=50,required=True),
    Field('apellidos',type='string',length=50,required=True),
    Field('telefono',type='string',length=15),
    Field('correo_inst', type='string',notnull=True),
    Field('correo_alter', type='string'),
    Field('tipo',type='string',length=15,requires=IS_IN_SET(['Usuario', 'DEX', 'Administrador','Bloqueado'])),
    primarykey=['ci'],
    migrate=False,
);

db.define_table('USBID',
    Field('ci_usuario',db.USUARIO.ci),
    Field('usbid',type='string',length=20, notnull=True, unique=True),
    primarykey=['ci_usuario'],
    migrate=False
);

db.define_table('JEFE_DEPENDENCIA',
    Field('id_jefe', type='id'),
    Field('ci_usuario',db.USUARIO.ci),
    primarykey=['id_jefe'],
    migrate=False
);

db.define_table('PROGRAMA',
    Field('id_programa', type='id'),
    Field('nombre',type='string',length=256, notnull=True, unique=True),
    Field('descripcion',type='string',length=2048, notnull=True, unique=True),
    primarykey=['id_programa'],
    migrate=False
);

db.define_table('TIPO_ACTIVIDAD',
    Field('id_tipo', type='id'),
    Field('nombre',type='string',length=128, notnull=True,unique=True,
           requires=[IS_LENGTH(128,error_message='Tamaño máximo de 128 caracteres')]),
    Field('tipo_p_r',type='string', length=1, notnull=True, requires=IS_IN_SET(["P", "R"]), default="P"),
    Field('descripcion',type='string',length=2048, notnull=True,
           requires=[IS_LENGTH(2048,error_message='Tamaño máximo de 2048 caracteres')]),
    Field('id_programa',db.PROGRAMA.id_programa),
    Field('validacion',type='string', length=128, notnull=True, default='True'),
    Field('producto', type='string', length=256,
           requires=[IS_NOT_EMPTY(error_message='No puede ser vacía'),
                     IS_LENGTH(256,error_message='El nombre no pude ser más de 256 caracteres')]),
    Field('nro_campos', type='integer', requires=IS_NOT_EMPTY(error_message='No puede ser vacía')),
    Field('id_jefe_creador',db.JEFE_DEPENDENCIA.id_jefe),
    Field('ci_usuario_propone',db.USUARIO.ci),
    Field('papelera', type='boolean', notnull = True, default=False),
    primarykey=['id_tipo'],
    migrate=False
);

db.define_table('PRODUCTO',
    Field('id_producto',  type='id'),
    Field('id_tipo', db.TIPO_ACTIVIDAD.id_tipo),
    Field('validacion',type='string',default='En espera'),
    Field('estado',type='string'),
    Field('evaluacion_criterio',type='string',length=256),
    Field('evaluacion_valor',type='string', length=256),
    Field('modif_fecha', type='date'),
    Field('ci_usu_modificador', db.USUARIO.ci),
    Field('ci_usu_creador', db.USUARIO.ci),
    primarykey=['id_producto'],
    migrate=False
);

db.define_table('PERMISOS_TIPO_ACT',
    Field('permiso',type='string',length=256),
    Field('id_tipo', db.TIPO_ACTIVIDAD.id_tipo),
    primarykey=['permiso','id_tipo'],
    migrate=False

);

db.define_table('CATALOGO',
    Field('id_catalogo', type='id'),
    Field('nro_campos',type='integer'),
    Field('nombre',type='string',length=128, unique = True),
    primarykey=['id_catalogo'],
    migrate=False
);


db.define_table('CAMPO_CATALOGO',
    Field('id_campo_cat',  type='id'),
    Field('id_catalogo', db.CATALOGO.id_catalogo),
    Field('nombre', type='string', length=256),
    Field('tipo_campo',type='string', length=64,
           requires = [IS_IN_SET(tipo_campos)],
           widget = SQLFORM.widgets.options.widget),
    Field('obligatorio', type='boolean'),
    primarykey=['id_campo_cat'],
    migrate=False
);

db.define_table('CAMPO',
    Field('id_campo', type='id'),
    Field('id_catalogo', db.CATALOGO.id_catalogo),
    Field('nombre',type='string', length=256),
    Field('tipo_campo',type='string', length=64,
           requires = [IS_IN_SET(tipo_campos)],
           widget = SQLFORM.widgets.options.widget),
    Field('obligatorio', type='boolean'),
    primarykey=['id_campo'],
    migrate=False
);

db.define_table('ACT_POSEE_CAMPO',
    Field('id_tipo_act', db.TIPO_ACTIVIDAD.id_tipo),
    Field('id_campo', db.CAMPO.id_campo),
    primarykey=['id_tipo_act', 'id_campo'],
    migrate=False
);

db.define_table('PRODUCTO_TIENE_CAMPO',
    Field('id_producto',db.PRODUCTO.id_producto),
    Field('id_campo', db.CAMPO.id_campo),
    Field('nombre',type='string', length=256),
    Field('valor_campo', type='string', length=512),
    primarykey=['id_producto', 'id_campo'],
    migrate=False
);


db.define_table('PARTICIPA_PRODUCTO',
    Field('ci_usuario',db.USUARIO.ci),
    Field('id_producto',db.PRODUCTO.id_producto),
    primarykey=['ci_usuario','id_producto'],
    migrate=False
);

db.define_table('GESTIONA_TIPO_ACT',
    Field('id_jefe', db.JEFE_DEPENDENCIA.id_jefe),
    Field('id_tipo_act', db.TIPO_ACTIVIDAD.id_tipo),
    primarykey=['id_jefe','id_tipo_act'],
    migrate=False
);


db.define_table('GESTIONA_CATALOGO',
    Field('id_jefe', db.JEFE_DEPENDENCIA.id_jefe),
    Field('id_catalogo',db.CATALOGO.id_catalogo),
    primarykey=['id_jefe','id_catalogo'],
    migrate=False
);

db.define_table('LOG_SIRADEX',
    Field('accion',type='string'),
    Field('accion_fecha',type='date'),
    Field('accion_ip',type='string', length=256),
    Field('descripcion',type='string'),
    Field('ci_usuario',db.USUARIO.ci),
    primarykey=['accion','accion_fecha','accion_ip'],
    migrate=False
);
