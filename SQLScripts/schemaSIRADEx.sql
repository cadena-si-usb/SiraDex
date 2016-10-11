CREATE TABLE USUARIO(
  ci             VARCHAR(10)   NOT NULL,
  usbid          VARCHAR(20)   NOT NULL,
  nombres        VARCHAR(50),
  apellidos      VARCHAR(50),
  telefono       VARCHAR(15),
  correo_inst    VARCHAR(50),
  correo_alter   VARCHAR(50),
  tipo           VARCHAR(15),

  CONSTRAINT PK_USUARIO
             PRIMARY KEY (ci)
);

CREATE TABLE USBID(
  ci_usuario  VARCHAR(10) NOT NULL,
  usbid       VARCHAR(20) NOT NULL,

  CONSTRAINT PK_USBID
             PRIMARY KEY (ci_usuario),
  CONSTRAINT FK_USBID_CI_USUARIO
             FOREIGN KEY (ci_usuario)
             REFERENCES  USUARIO(ci)
);

CREATE TABLE JEFE_DEPENDENCIA(
  id_jefe      SERIAL      NOT NULL,
  ci_usuario   VARCHAR(10) NOT NULL,

  CONSTRAINT PK_JEFE_DEPENDENCIA
             PRIMARY KEY (id_jefe),
  CONSTRAINT FK_JEFE_DEPENDENCIA_CI_USUARIO
             FOREIGN KEY (ci_usuario)
             REFERENCES  USUARIO(ci)
);

CREATE TABLE PROGRAMA(
  id_programa  SERIAL        NOT NULL,
  nombre       VARCHAR(256)  NOT NULL,
  descripcion  Varchar(2048) NOT NULL,

  CONSTRAINT PK_PROGRAMA
             PRIMARY KEY (id_programa)

);

CREATE TABLE TIPO_ACTIVIDAD(
  id_tipo             SERIAL        NOT NULL,
  nombre              VARCHAR(128)  NOT NULL,
  tipo_p_r            VARCHAR(1)    NOT NULL,
  descripcion         VARCHAR(2048) NOT NULL,
  id_programa         INT           NOT NULL,
  validacion          VARCHAR(128)  NOT NULL,
  producto            VARCHAR(256),
  nro_campos          INT,
  id_jefe_creador     INT,
  ci_usuario_propone  VARCHAR(10),
  papelera            BOOLEAN NOT NULL DEFAULT FALSE,

  CONSTRAINT PK_TIPO_ACTIVIDAD
             PRIMARY KEY (id_tipo),
  CONSTRAINT FK_TIPO_ACTIVIDAD_CI_USUARIO_PROPONE
             FOREIGN KEY (ci_usuario_propone)
             REFERENCES  USUARIO(ci),
  CONSTRAINT FK_TIPO_ACTIVIDAD_ID_JEFE_CREADOR
             FOREIGN KEY (id_jefe_creador)
             REFERENCES  JEFE_DEPENDENCIA(id_jefe),
  CONSTRAINT FK_TIPO_ACTIVIDAD_ID_PROGRAMA
             FOREIGN KEY (id_programa)
             REFERENCES  PROGRAMA(id_programa)
);

CREATE TABLE PRODUCTO(
  id_producto         SERIAL NOT NULL,
  id_tipo             INT,
  nombre              VARCHAR(128),
  descripcion         VARCHAR(256),
  estado          VARCHAR DEFAULT 'En Espera',
  evaluacion_criterio VARCHAR(256),
  evaluacion_valor    VARCHAR(256),
  modif_fecha         DATE,
  ci_usu_modificador  VARCHAR(10),
  ci_usu_creador      VARCHAR(10),

  CONSTRAINT PK_PRODUCTO
             PRIMARY KEY (id_producto),
  CONSTRAINT FK_PRODUCTO_CI_USU_CREADOR
             FOREIGN KEY (ci_usu_creador)
             REFERENCES  USUARIO(ci),
  CONSTRAINT FK_PRODUCTO_CI_USU_MODIFICADOR
             FOREIGN KEY (ci_usu_modificador)
             REFERENCES USUARIO(ci),
  CONSTRAINT FK_PRODUCTO_ID_TIPO
             FOREIGN KEY (id_tipo)
             REFERENCES  TIPO_ACTIVIDAD(id_tipo)
);

CREATE TABLE PERMISOS_TIPO_ACT(
  permiso   VARCHAR(256),
  id_tipo   INT,

  CONSTRAINT PK_PERMISOS_TIPO_ACT
             PRIMARY KEY (permiso,id_tipo),
  CONSTRAINT FK_PERMISOS_TIPO_ACT_ID_TIPO
             FOREIGN KEY (id_tipo)
             REFERENCES  TIPO_ACTIVIDAD(id_tipo)
);

CREATE TABLE CATALOGO(
  id_catalogo   SERIAL NOT NULL,
  nro_campos    INT,
  nombre        VARCHAR(128),

  CONSTRAINT PK_CATALOGO
             PRIMARY KEY (id_catalogo)
);


CREATE TABLE CAMPO_CATALOGO(
  id_campo_cat  SERIAL NOT NULL,
  id_catalogo   INT,
  nombre        VARCHAR(256),
  tipo_campo    VARCHAR(64),
  obligatorio   BOOLEAN DEFAULT FALSE,

  CONSTRAINT PK_CAMPO_CATALAGO
             PRIMARY KEY (id_campo_cat),
  CONSTRAINT FK_CAMPO_CATALOGO_ID_CATALOGO
             FOREIGN KEY (id_catalogo)
             REFERENCES  CATALOGO(id_catalogo)
);

CREATE TABLE CAMPO(
  id_campo      SERIAL NOT NULL,
  id_catalogo   INT,
  nombre        VARCHAR(256),
  tipo_campo    VARCHAR(64),
  obligatorio   BOOLEAN DEFAULT FALSE,

  CONSTRAINT PK_CAMPO
             PRIMARY KEY (id_campo),
  CONSTRAINT FK_CAMPO_ID_CATALOGO
             FOREIGN KEY(id_catalogo)
             REFERENCES CATALOGO(id_catalogo)
);

CREATE TABLE ACT_POSEE_CAMPO(
  id_tipo_act  INT,
  id_campo     INT,

  CONSTRAINT PK_ACT_POSEE_CAMPO
             PRIMARY KEY (id_tipo_act,id_campo),
  CONSTRAINT FK_ACT_POSEE_CAMPO_ID_TIPO_ACT
             FOREIGN KEY (id_tipo_act)
             REFERENCES  TIPO_ACTIVIDAD(id_tipo),
  CONSTRAINT FK_ACT_POSEE_CAMPO_ID_CAMPO
             FOREIGN KEY (id_campo)
             REFERENCES  CAMPO(id_campo)
);

CREATE TABLE PRODUCTO_TIENE_CAMPO(
  id_producto    INT,
  id_campo       INT,
  nombre         VARCHAR(256),
  valor_campo    VARCHAR(512),

  CONSTRAINT PK_TIENE_CAMPO
             PRIMARY KEY (id_producto, id_campo),
  CONSTRAINT FK_TIENE_CAMPO_ID_PRODUCTO
             FOREIGN KEY (id_producto)
             REFERENCES  PRODUCTO(id_producto),
  CONSTRAINT FK_TIENE_CAMPO_ID_CAMPO
             FOREIGN KEY (id_campo)
             REFERENCES  CAMPO(id_campo)
);


CREATE TABLE PARTICIPA_PRODUCTO(
  ci_usuario    VARCHAR(10),
  id_producto   INT,

  CONSTRAINT PK_PARTICIPA_ACT
             PRIMARY KEY (ci_usuario,id_producto),
  CONSTRAINT FK_PARTICIPA_ACT_CI_USUARIO
             FOREIGN KEY (ci_usuario)
             REFERENCES  USUARIO(ci),
  CONSTRAINT FK_PARTICIPA_ACT_ID_PRODUCTO
             FOREIGN KEY (id_producto )
             REFERENCES  PRODUCTO(id_producto)
);

CREATE TABLE GESTIONA_TIPO_ACT(
  id_jefe      INT,
  id_tipo_act  INT,

  CONSTRAINT PK_GESTIONA_TIPO_ACT
             PRIMARY KEY (id_jefe, id_tipo_act),
  CONSTRAINT FK_GESTIONA_TIPO_ACT_ID_JEFE
             FOREIGN KEY (id_jefe)
             REFERENCES JEFE_DEPENDENCIA(id_jefe),
  CONSTRAINT FK_GESTIONA_TIPO_ACT_ID_TIPO_ACT
             FOREIGN KEY (id_tipo_act)
             REFERENCES TIPO_ACTIVIDAD(id_tipo)
);

CREATE TABLE GESTIONA_CATALOGO(
  id_jefe      INT,
  id_catalogo  INT,

  CONSTRAINT PK_GESTIONA_CATALOGO
             PRIMARY KEY (id_jefe, id_catalogo),
  CONSTRAINT FK_GESTIONA_CATALOGO_ID_JEFE
             FOREIGN KEY (id_jefe)
             REFERENCES  JEFE_DEPENDENCIA(id_jefe),
  CONSTRAINT FK_GESTIONA_CATALOGO_ID_CATALOGO
             FOREIGN KEY (id_catalogo)
             REFERENCES  CATALOGO(id_catalogo)
);

CREATE TABLE LOG_SIRADEX(
  accion        TEXT,
  accion_fecha  DATE,
  accion_ip     VARCHAR(256),
  descripcion   TEXT,
  ci_usuario    VARCHAR(10),

  CONSTRAINT PK_LOG
             PRIMARY KEY (accion,accion_fecha,accion_ip),
  CONSTRAINT FK_LOG_CI_USUARIO
             FOREIGN KEY (ci_usuario)
             REFERENCES  USUARIO(ci)
);
