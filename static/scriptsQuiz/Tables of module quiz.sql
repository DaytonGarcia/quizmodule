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