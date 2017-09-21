#Metadata del quiz
create table tb_metadata_quiz 
(
	id 			int 		auto_increment 		primary key,
	id_quiz 	int 		not null,
	nombre 		varchar(50) not null,
	fecha_creacion 	date 	not null,
	creador 	int 		not null,
	curso 		varchar(50) not null
);

#Equivalencia entre actividades y quiz
create table equivalencia_quiz_category(
id int AUTO_INCREMENT not null primary key,
categorie int not null unique,
description varchar(100),
FOREIGN KEY (categorie)
      REFERENCES activity_category(id)
)

#Usuarios de pruebas
select * from auth_user where username = '11769'
select * from auth_user where username = '200915754'

#Password Conocido
#pbkdf2(1000,20,sha512)$851658f698b517fd$094c6882a47b8952e4d25b6cd37e41ac8664b8cf

#Tabla con fechas limite
#update student_control_period set date_finish = '2017-09-15 00:00:00' where id =11

#Cambiar pass a usuarios
update auth_user 
set password = 'pbkdf2(1000,20,sha512)$851658f698b517fd$094c6882a47b8952e4d25b6cd37e41ac8664b8cf'
where username = '11769'

####*********************************Cosas*******
select * from course_activity order by id desc;
select * from activity_category;


create table equivalencia_quiz_category(
id int AUTO_INCREMENT not null primary key,
categorie int not null unique,
description varchar(100),
FOREIGN KEY (categorie)
      REFERENCES activity_category(id)
);

select * from equivalencia_quiz_category;

insert into equivalencia_quiz_category (categorie, description) values(9, 'Examenes Cortos, estos se pueden hacer en linea');
insert into equivalencia_quiz_category (categorie, description) values(16, 'Los examenes Finales se pueden hacer en linea');

select * from course_activity A
inner join course_activity_category B on B.id = A.course_activity_category
inner join activity_category C on C.id = B.category
inner join equivalencia_quiz_category D on D.categorie = C.id
where A.assignation = 1 
and A.laboratory = 'T' 
and A.semester = 8
and B.category = 9;

select A.id, A.name from course_activity A
inner join course_activity_category B on B.id = A.course_activity_category
where A.assignation = 1 
and A.laboratory = 'T' 
and A.semester = 8
and B.category = 9;


select * from `course_activity_category` order by id desc;


select A.id, A.category from activity_category A
inner join equivalencia_quiz_category B on B.categorie = A.id;

select * from period_year;
select * from period;

create table tb_quiz_actividad(
id 					int 		auto_increment 		primary key,
id_actividad 		int 		not null			unique,
id_quiz 			int			not null,
fecha				date		not null,
inicio 				time		not null,
duracion 			int			not NULL,
finalizado			boolean 	not null
)


Alter table tb_quiz_actividad
ADD COLUMN private boolean null;

Alter table tb_quiz_actividad
ADD COLUMN keyword varchar(256) null;

programaciones = db.executesql( 
                                        select 	A.id,
                                        A.id_actividad,
                                        A.id_quiz,
                                        A.fecha,
                                        A.inicio,
                                        A.duracion,
                                        A.finalizado,
                                        A.private,
                                        A.keyword,
                                        B.nombre as nombre_quiz,
                                        B.fecha_creacion as creacion_quiz,
                                        B.creador as id_creador,
                                        C.id as id_project,
                                        B.curso as id_curso, 
                                        C.name as nombre_curso,
                                        D.id as id_programador,
                                        CONCAT(D.first_name, ' ', D.last_name) as nombre_programador,
                                        F.category as id_categoria,
                                        G.description as nombre_categoria,
                                        E.name as actividad_nombre,
                                        E.semester as semestre
                                from tb_quiz_actividad A
                                inner join tb_metadata_quiz B on B.id_quiz = A.id_quiz
                                inner join project C on C.project_id = B.curso
                                inner join auth_user D on D.id = B.creador
                                inner join course_activity E on E.id = A.id_actividad
                                inner join course_activity_category F on F.id = E.course_activity_category
                                inner join activity_category G on G.id = F.category
                                where 	C.id = %d
                            
    ,
     1)


#Alumnos
201113895
200212984