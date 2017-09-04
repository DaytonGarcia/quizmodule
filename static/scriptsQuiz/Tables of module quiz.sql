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