INSERT INTO programa values(1, 'programa1','descripcion 1');
INSERT INTO programa values(2, 'programa2','descripcion 1');
INSERT INTO programa values(3, 'programa3','descripcion 1');
INSERT INTO programa values(4, 'programa4','descripcion 1');

INSERT INTO tipo_actividad values(1, '1 Actividad programa 1','p', 'descr', 1, 't');
INSERT INTO tipo_actividad values(2, '2 Actividad programa 1','p', 'descr', 1, 't');
INSERT INTO tipo_actividad values(3, '3 Actividad programa 1','p', 'descr', 1, 't');
INSERT INTO tipo_actividad values(4, '4 Actividad programa 2','p', 'descr', 2, 't');
INSERT INTO tipo_actividad values(5, '5 Actividad programa 2','p', 'descr', 2, 't');
INSERT INTO tipo_actividad values(6, '6 Actividad programa 2','p', 'descr', 2, 't');
INSERT INTO tipo_actividad values(7, '7 Actividad programa 3','p', 'descr', 3, 't');
INSERT INTO tipo_actividad values(8, '8 Actividad programa 3','p', 'descr', 3, 't');

INSERT INTO catalogo values(1,1,'catalogo 1');
INSERT INTO catalogo values(2,1,'catalogo 2');

INSERT INTO campo values(1,1,'1 campo catalogo 1','Texto Largo',true);
INSERT INTO campo values(2,1,'2 campo catalogo 1','Texto Largo',true);
INSERT INTO campo values(3,2,'3 campo catalogo 2','Texto Largo',true);

INSERT INTO act_posee_campo values(1,1);
INSERT INTO act_posee_campo values(1,2);
INSERT INTO act_posee_campo values(1,3);


#UPDATE usuario SET tipo='Administrador' WHERE usbid='12-10941';
#INSERT INTO producto VALUES (4,1,'nombre 4','no tiene','Por Validar','','',NULL,'24272072','24272072');