
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
             PRIMARY KEY (usbid)
);

CREATE TABLE PROGRAMA(
  id_programa         SERIAL        NOT NULL,
  nombre              VARCHAR(256)  NOT NULL,
  abreviacion         VARCHAR(10)   NOT NULL,
  descripcion         Varchar(2048) NOT NULL,
  papelera            BOOLEAN       NOT NULL DEFAULT FALSE,
  modif_fecha         DATE,
  usbid_usu_modificador  VARCHAR(20),

  CONSTRAINT PK_PROGRAMA
             PRIMARY KEY (id_programa),
  CONSTRAINT FK_PROGRAMA_USBID_USU_MODIFICADOR
             FOREIGN KEY (usbid_usu_modificador)
             REFERENCES USUARIO(usbid)

);

CREATE TABLE TIPO_ACTIVIDAD(
  id_tipo             SERIAL        NOT NULL,
  codigo              VARCHAR(10)   NOT NULL,
  nombre              VARCHAR(128)  NOT NULL,
  tipo_p_r            VARCHAR(1)    NOT NULL,
  descripcion         VARCHAR(2048) NOT NULL,
  id_programa         INT           NOT NULL,
  producto            VARCHAR(256),
  nro_campos          INT,
  papelera            BOOLEAN NOT NULL DEFAULT FALSE,
  modif_fecha         DATE,

  CONSTRAINT PK_TIPO_ACTIVIDAD
             PRIMARY KEY (id_tipo),
  CONSTRAINT FK_TIPO_ACTIVIDAD_ID_PROGRAMA
             FOREIGN KEY (id_programa)
             REFERENCES  PROGRAMA(id_programa)
);

CREATE TABLE PRODUCTO(
  id_producto         SERIAL NOT NULL,
  id_tipo             INT,
  nombre              VARCHAR(128),
  descripcion         VARCHAR(256),
  estado              VARCHAR DEFAULT 'Por Validar',
  fecha_realizacion   DATE,
  fecha_modificacion  DATE,
  lugar               VARCHAR(50),
  usbid_usu_creador      VARCHAR(20),

  CONSTRAINT PK_PRODUCTO
             PRIMARY KEY (id_producto),
  CONSTRAINT FK_PRODUCTO_USBID_USU_CREADOR
             FOREIGN KEY (usbid_usu_creador)
             REFERENCES  USUARIO(usbid),
  CONSTRAINT FK_PRODUCTO_ID_TIPO
             FOREIGN KEY (id_tipo)
             REFERENCES  TIPO_ACTIVIDAD(id_tipo)
);

CREATE TABLE COMPROBANTE(
  id_comprobante    SERIAL NOT NULL,
  archivo           VARCHAR(256) NOT NULL,
  descripcion       VARCHAR(100),
  producto          INT,

  CONSTRAINT  PK_COMPROBANTE
              PRIMARY KEY (id_comprobante),

  CONSTRAINT  FK_PRODUCTO_PRODUCTO
              FOREIGN KEY (producto)
              REFERENCES PRODUCTO(id_producto)
              MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE

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
  id_prod        INT,
  id_campo       INT,
  valor_campo    VARCHAR(512),

  CONSTRAINT PK_TIENE_CAMPO
             PRIMARY KEY (id_prod, id_campo),
  CONSTRAINT FK_TIENE_CAMPO_ID_PRODUCTO
             FOREIGN KEY (id_prod)
             REFERENCES  PRODUCTO(id_producto),
  CONSTRAINT FK_TIENE_CAMPO_ID_CAMPO
             FOREIGN KEY (id_campo)
             REFERENCES  CAMPO(id_campo)
);


CREATE TABLE PARTICIPA_PRODUCTO(
  usbid_usuario    VARCHAR(20),
  id_producto   INT,

  CONSTRAINT PK_PARTICIPA_ACT
             PRIMARY KEY (usbid_usuario,id_producto),
  CONSTRAINT FK_PARTICIPA_ACT_USBID_USUARIO
             FOREIGN KEY (usbid_usuario)
             REFERENCES  USUARIO(usbid),
  CONSTRAINT FK_PARTICIPA_ACT_ID_PRODUCTO
             FOREIGN KEY (id_producto )
             REFERENCES  PRODUCTO(id_producto)
);


CREATE TABLE LOG_SIRADEX(
  accion        TEXT,
  accion_fecha  DATE,
  accion_ip     VARCHAR(256),
  descripcion   TEXT,
  usbid_usuario    VARCHAR(20),

  CONSTRAINT PK_LOG
             PRIMARY KEY (accion,accion_fecha,accion_ip),
  CONSTRAINT FK_LOG_USBID_USUARIO
             FOREIGN KEY (usbid_usuario)
             REFERENCES  USUARIO(usbid)
);
