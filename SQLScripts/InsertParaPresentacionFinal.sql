/*Insercion de Programas*/

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Educación Permanente','EP','Encargada de los programas de formación no conducentes a grado académico, mediante cursos, diplomados, talleres, foros, seminarios y otras actividades complementarias de actualización, perfeccionamiento y capacitación para el trabajo productivo, dirigidos tanto a profesionales y técnicos como a la comunidad y al público en general.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Fomento y proyección artística, cultural y deportiva','CD','Este programa tiene como objetivo impulsar la participacion de la comunidad universitaria en la organización de eventos recreacionales, en las actividades culturales y/o artisticas, en la organización de agrupaciones culturales, artisticas y deportivas en representación de la USB.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Divulgación y promoción del quehacer universitario','QU','Este programa tiene como objetivo promover la participación de la comunidad universitaria en comites y comisiones de carácter cientifico, humanistico, cultural, artistico, educativo o deportivo. Además de la publicación de articulos, libros o material audiovisual de divulgacion del quehacer universitario.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Igualdad de Oportunidades','IO','Este progarma tiene como objetivo brindar oportunidades para el ingreso a la USB a todos aquellos estudiantes cursantes del último año de la Educación Media Diversificadadel sector oficial, que rtengan dentro de sus aspiraciones vocacionales estudiar alguna carrera que ofrece la institucion.','f');

INSERT INTO programa values(nextval('programa_id_programa_seq'),'Emprendimiento y seguimiento de Egresados','EGMLEMUE','Este programa tiene como objetivo contribuir a la formacion integral del estudiante y recien egresado, y apoyar el desarrollo de futuros líderes y empresarios competentes, creativos y emprendedores.','f');

/*Insercion de tipos de actividad*/

/*Tipos de actividad del programa Educacion Permanente(EP) 1*/

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-C1','Diseño de talleres y cursos de extensión','R','Diseño curricular del Programa del taller o curso(incluye talleres y cursos de Desarrollo Profesoral)','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-C2','Dictado de talleres y cursos de extensión finalizados, por cohorte','R','Listado final del curso con registro de asistencia o calificaciones (por cohorte).Incluye talleres y cursos de Desarrollo Profesoral.','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-P1','Diseño de Programas de cursos de extensión','R','Diseño curricular del programa','1','True');

--------------------------------------------------------------------Complemento----------------------------------------------------------------

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-P2','Gestión de Programas de cursos de extensión','R','Informe de avance o cierre del programa','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-P3','Dictado de contenidos de Programas de Cursos de Extensión por cohorte','R','Listado final del curso dictado por cohorte','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-D1','Diseño y propuesta de nuevos Diplomados','P','Diseño curricular aprobado del Diplomado','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-D2','Evaluación de propuesta de Diplomados','R','Formato de evaluación de la propuesta recibido por la Coordinación ','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-D3','Gestión de Diplomados','R','Informe de avance o de cierre del Diplomado(Responsable académico).','1','True');

INSERT INTO tipo_actividad values(nextval('tipo_actividad_id_tipo_seq'),'EPR-D4','Dictado de contenidos de Diplomados finalizados, por cohorte','R','Listado final del contenido respectivo con calificaciones (por cohorte).','1','True');

-----------------------------------------------------------------------------------------------------------------------------------------------

/*Tipos de actividad del programa Fomento y proyeccion artistica, cultural y deportiva(CD) 2*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O1','Participación en la organización de eventos culturales y/o artísticos en representación de la USB','P','Informe de gestión de la organización','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-O1','Participación en la organización de eventos culturales y/o artísticos en representación de la USB','R','Validación o constancia impresa o electrónica de la Unidad organizadora del evento','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O2','Participación en la organización de eventos deportivos en representación de la USB','P','Informe de gestión de la organización','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-O2','Participación en la organización de eventos deportivos en representación de la USB','R','Reporte de Participación','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O3','Participación en la organización de eventos recreacionales en representación de la USB','P','Informe de gestión de la organización','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O4','Participación en la organización de agrupaciones deportivas en representación de la USB','P','Informe de gestión de la organización','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDP-O5','Participación en la organización de agrupaciones culturales y/o artísticas en representación de la USB','P','Informe de gestión de la organización','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-P1','Participación en delegaciones o selecciones deportivas en representación de la USB','R','Informe de gestión del encargado de la delegación','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-P2','Participación en Grupos Estables adscritos a la Dirección de Cultura','R','Informe de participación en grupos estables','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-P3','Participación en actividades culturales y/o artísticas en representación de la USB','R','Informe de participación en actividades culturales','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-P4','Participación como asesor de agrupaciones y organizaciones estudiantiles de la USB','R','Informe anual de gestión o de asesoría','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-F1','Diseño y propuesta de talleres y cursos de Formación Complementaria General de programas de estudios en las áreas respectivas','R','Diseño curricular del curso','2','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'CDR-F2','Dictado de talleres y cursos de Formación Complementaria General de programas de estudios en las áreas respectivas','R','Acta final de notas del curso dictado','2','True');

/*Tipos de actividad del programa Divulgacion y promocion del quehacer universitario(QU) 3*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUP-C1','Participación en comités y comisiones ad-hoc científicos,humanísticos,culturales,artísticos,educativos o deportivos','P','Informe final de la comisión o comité','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-C2','Participación en la organización de foros, congresos y simposios,internos o externos','P','Informe de gestión de la organización','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-C3','Participación Juntas Directivas de Asociaciones científicas,humanísticas,culturales,artísticas,educativas,deportivas o gremiales','R','Informe de gestión aprobado en Asamblea','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-C4','Participación en jurados de premios y concursos nacionales e internacionales','R','Veredicto del jurado','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D1','Participación en muestras, conciertos, exposiciones, eventos deportivos y culturales','R','Informe de gestión, avance o resultados de la organización o documento probatorio de la participación y de la ejecución de la actividad y de la filiación del profesor a la USB','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUP-D2','Participación como autor de artículo o reportaje escrito de opinión del quehacer universitario en medios impresos o digitales','P','Artículo publicado','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D3','Participación como entrevistado en artículo de opinión del quehacer universitario en medios impresos o digitales','R','Artículo publicado','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUP-D4','Publicación de libro de divulgación del quehacer universitario en medios impresos o digitales','P','Libro publicado','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D5','Presentación en conferencia, intervención en seminarios, foros y mesas de trabajo vinculados con la extensión universitaria','R','Trabajo, ponencia, poster, artículo','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D6','Participación como presentador,entrevistado o ponente en programas de opinión en medios radiales, televisivos o digitales','R','Reseña de entrevista en medio de comunicación social o copia del archivo audiovisual en formato digital','3','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'QUR-D7','Trabajo editorial o de arbitraje de publicaciones, tanto internas en la USB como externas en representación de la USB','R','Informe de arbitraje o de evaluación','3','True');

/*Tipos de actividad del programa Igualdad de Oportunidades(IO) 4*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOP-A1','Diseño de programas de formación y nivelación académica preuniversitaria en representación de la USB','P','Diseño curricular de los programas','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A2','Responsable académico de la ejecución de programas de nivelación académica preuniversitaria en representación de la USB','R','Informe de gestión del programa','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A3','Diseño de cursos de nivelación académica preuniversitaria en representación de la USB','R','Diseño curricular de cursos','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A4','Dictado de cursos,talleres y conferencias en la UEUSB y otras instituciones de educación media y diversificada','R','Listado final del curso dictado por cohorte','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOR-A5','Organización de actividades de apoyo a programas y cursos de nivelación académica preuniversitaria en representación de la USB','R','del evento','4','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'IOI-S1','Participación en la administración de los exámenes de admisión de la Universidad Simón Bolívar y de diagnóstico del PIO','R','No generan productos de extensión. Se reconocen parcialmente como actividades de  extensión sin generación de productos académicos, pero equivalentes a una fracción (1/4) de un producto tipo “R”','4','True');

/*Tipos de actividad del programa Emprendimiento y seguimiento de Egresados(EG/ML/EM/UE) 5*/

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'EGR-R1','Organización de actividades y eventos de apoyo al Seguimiento de los Egresados de la USB','P','Informe de gestión de la organización','5','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'MLR-R1','Organización de actividades y eventos de Información Ocupacional e Investigación del Mercado Laboral a estudiantes y egresados','P','Informe de gestión de la organización ','5','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'EMR-P1','Organización de actividades y eventos de Promoción del Emprendimiento en estudiantes,profesores,egresados,empleados y/u obreros','P','Informe de gestión de la organización ','5','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'EMR-P2','Participación en la creación e incubación de empresas desde la USB','P','Documento de registro mercantil de la empresa creada o en incubación','5','True');

INSERT INTO tipo_actividad values (nextval('tipo_actividad_id_tipo_seq'),'VUR-E1','Promotor o responsable del desarrollo y ejecución de convenios y mecanismos de vinculación entre universidad y sector productivo','P','Convenios, acuerdos, contratos con organizaciones/empresas requirentes de vinculación con la Universidad','5','True');
