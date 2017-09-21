@auth.requires_login()
@auth.requires(auth.has_membership('Student') or auth.has_membership('Teacher') or auth.has_membership('Super-Administrator') or auth.has_membership('Academic') or auth.has_membership('Ecys-Administrator'))

def home_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = request.vars['period']
    project = request.vars['project']
    return dict(ecys_var = ecys_var, periodo = period, course=project, period=periodo)

def create_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    project = db(db.project.id==idproject).select().first()  
    idPregunta = 1
    return dict(ecys_var = ecys_var, periodo = period, idPregunta = idPregunta, project=project, idperiodoc=idperiodoc, idproject=idproject)

def consult_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    print idproject
    project = db(db.project.id==idproject).select().first()  
    userid = auth.user.id
    cursoid = project.project_id
    cadena = 'uid:'+str(userid)+':curso:'+str(cursoid)+':quiz:*'
    import redis
    r = redis.StrictRedis()
    a = r.keys(cadena)
    cuestionarios = a
    lista = db(db.project.project_id==cursoid).select(
        db.tb_metadata_quiz.ALL, 
        db.auth_user.first_name, 
        db.auth_user.last_name, 
        db.project.name, 
        join=[
            db.auth_user.on(
                db.tb_metadata_quiz.creador == db.auth_user.id
                ), 
            db.project.on(
                db.project.project_id == db.tb_metadata_quiz.curso)]
                )
    #lista = db(db.tb_metadata_quiz.id == db.auth_user.id).select()
    print lista
    return dict(ecys_var = ecys_var, periodo = period, project=project, idperiodoc=idperiodoc, idproject=idproject,a=a,lista=lista)

def consultar_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    project = db(db.project.id==idproject).select().first()  
    idPregunta = 1
    return dict(ecys_var = ecys_var, periodo = period, project=project)

@auth.requires_login()
def aumentarPregunta():
    idQuestion += 1
    return idQuestion

@auth.requires_login()
def obtenerQuiz():
    import redis
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    r.incr("idquiz")
    idq = '{"value":"'+r.get("idquiz")+'"}'
    return idq

@auth.requires_login()
def GuardarQuiz():
    import redis
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    ide = request.vars['id']
    preguntas = request.vars['jsonquiz']
    curso = request.vars['project']
    uid = request.vars['uid']
    title = request.vars['title']
    a = r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"preguntas",preguntas)
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"ejecuciones",0)
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"ganados",0)
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"perdidos",0)
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"state",0)
    db.tb_metadata_quiz.insert(
        id_quiz = ide, 
        nombre= title, 
        fecha_creacion = datetime.datetime.now(), 
        creador=uid, 
        curso=curso)
    db.commit()
    return a


def GetQuiz():
    import redis
    r = redis.StrictRedis()
    a = r.get(34)
    return a

@auth.requires_login()
def take_quiz():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = request.vars['period']
    project = request.vars['project']
    return dict(periodo = period, course=project, period=periodo)

@auth.requires_login()
def reportes():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = request.vars['period']
    project = request.vars['project']
    #project = db(db.project.id==idproject).select().first()  

    myquery = (db.project.id==project) & (db.course_activity.semester==period)


    programaciones = db(myquery).select(
        db.tb_quiz_actividad.id,
		db.tb_quiz_actividad.id_actividad,
		db.tb_quiz_actividad.id_quiz,
		db.tb_quiz_actividad.fecha,
		db.tb_quiz_actividad.inicio,
		db.tb_quiz_actividad.duracion,
		db.tb_quiz_actividad.finalizado,
		db.tb_quiz_actividad.private,
		db.tb_quiz_actividad.keyword,
		db.tb_metadata_quiz.nombre,
		db.tb_metadata_quiz.fecha_creacion,
		db.tb_metadata_quiz.creador,
		db.tb_metadata_quiz.id,
		db.tb_metadata_quiz.curso, 
		db.project.name,
		db.auth_user.id,
		db.auth_user.first_name, 
        db.auth_user.last_name,
		db.course_activity_category.category,
		db.activity_category.description,
		db.course_activity.name,
		db.course_activity.semester,
        join=[
            db.tb_metadata_quiz.on(
                db.tb_metadata_quiz.id_quiz == db.tb_quiz_actividad.id_quiz    
            ),
            db.project.on(
                db.project.project_id == db.tb_metadata_quiz.curso    
            ),
            db.auth_user.on(
                db.auth_user.id == db.tb_metadata_quiz.creador    
            ),
            db.course_activity.on(
                db.course_activity.id == db.tb_quiz_actividad.id_actividad    
            ),
            db.course_activity_category.on(
                db.course_activity_category.id == db.course_activity.course_activity_category    
            ),
            db.activity_category.on(
                db.activity_category.id == db.course_activity_category.category    
            )
        ]
    )

    print programaciones
    return dict(periodo = period, course=project, period=periodo, programaciones=programaciones)

@auth.requires_login()
def view_reports():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

@auth.requires_login()
def viewer_quiz():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

def viewer_quiz2():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

def viewer_quiz3():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

@auth.requires_login()
def test():
    x = tuple(request.args)
    y = str(''.join(x))
    import redis
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    ide = int(y)
    lista = db(db.tb_metadata_quiz.id_quiz==ide).select(
        db.tb_metadata_quiz.creador, 
        db.tb_metadata_quiz.curso)

    creador = 0
    curso = 0

    #OBTENGO LA ESTRUCTUA JSON DEL QUIZ
    for quiz in lista:
        creador = quiz.creador
        curso = quiz.curso
    cadenaRedis = 'uid:'+str(creador)+':curso:'+str(curso)+':quiz:'+str(ide)
    datos = r.hget(cadenaRedis,'preguntas')

    #OBTENGO LA METADA DEL QUIZ
    lista = db(db.tb_metadata_quiz.id_quiz==ide).select(
        db.tb_metadata_quiz.ALL, 
        db.auth_user.first_name, 
        db.auth_user.last_name, 
        db.project.name, 
        join=[
            db.auth_user.on(
                db.tb_metadata_quiz.creador == db.auth_user.id
                ), 
            db.project.on(
                db.project.project_id == db.tb_metadata_quiz.curso)]
                )

    quiz = datos.replace('{[','{"PREGUNTAS" : [')

    return dict(quiz = quiz, metadata = lista.first()) 

@auth.requires_login()
def programacion_test():
    x = tuple(request.args)
    y = str(''.join(x))
    ide = int(y)
    lista = db(db.tb_metadata_quiz.id_quiz==ide).select(
        db.tb_metadata_quiz.creador, 
        db.tb_metadata_quiz.curso)

    #OBTENGO LA METADA DEL QUIZ
    lista = db(db.tb_metadata_quiz.id_quiz==ide).select(
        db.tb_metadata_quiz.ALL, 
        db.auth_user.first_name, 
        db.auth_user.last_name, 
        db.project.name, 
        join=[
            db.auth_user.on(
                db.tb_metadata_quiz.creador == db.auth_user.id
                ), 
            db.project.on(
                db.project.project_id == db.tb_metadata_quiz.curso)]
                )

    #OBTENGO LOS CODIGOS DE ACTIVIDADES QUE PERENECEN A UN QUIZ

    categorias = db().select(
        db.activity_category.id,
        db.activity_category.category,
        join=[
            db.equivalencia_quiz_category.on(
                db.equivalencia_quiz_category.categorie == db.activity_category.id
            )
        ] 
    )

    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    project = db(db.project.id==idproject).select().first() 

    #Si el periodo actual es igual al periodo recibido en la variable corresponde el quiz
    actual = False
    if(int(period)==int(idperiodoc)):
        actual = True
 


    print categorias
    return dict(metadata = lista.first(), categorias = categorias, periodo = period, project =project) 

@auth.requires_login()
def getActivities():
    periodo = request.vars['period']
    curso = request.vars['project']
    categoria = request.vars['categorie']

    print periodo
    print curso
    print categoria

    	
    myquery = (db.course_activity.assignation==curso) & (db.course_activity.semester==period) & (db.course_activity_category.category==categoria) & (db.course_activity.laboratory==True) & (db.tb_quiz_actividad.id == None)


    actividades = db(myquery).select(
        db.course_activity.id,
        db.course_activity.name,
        join=[
            db.course_activity_category.on(
                db.course_activity_category.id == db.course_activity.course_activity_category    
            )
        ],
        left=[
            db.tb_quiz_actividad.on(
                db.tb_quiz_actividad.id_actividad ==  db.course_activity.id 
            )
        ]
    )
    print "Las actividades son: "
    print actividades

    return response.json(actividades)

def GetNow():
    import datetime
    #ahora = request.utcnow # Obtiene fecha y hora actual
    ahora = datetime.datetime.now()
    print("Fecha y Hora:", ahora)  # Muestra fecha y hora
    return ahora 

@auth.requires_login()
def test_programacion():

    mensaje = ""
    try:
        pId_actividad = request.vars['id_actividad']
        pId_quiz = request.vars['id_quiz']
        pFecha = request.vars['fecha']
        pInicio = request.vars['inicio']
        pDuracion = request.vars['duracion']

        print 'La actividad es: ' + pId_actividad
        print 'El quiz es: ' + pId_quiz
        print 'La fecha es: ' + pFecha
        print 'La hora de incio es: ' + pInicio
        print 'La duracion es: ' + pDuracion

        db.tb_quiz_actividad.insert(
            id_actividad = pId_actividad,
            id_quiz = pId_quiz,
            fecha = pFecha,
            inicio= pInicio,
            duracion= pDuracion,
            finalizado= 0,
            private = 0
            )
        db.commit()

        metadata = db.executesql("""select 
		                                B.name as curso, 
		                                A.name as actividad, 
                                        D.category as categoria, 
                                        F.nombre as quiz 
                                from course_activity A
                                inner join  project B on B.id = A.assignation
                                inner join  course_activity_category C on A.course_activity_category = C.id
                                inner join  activity_category D on D.id = C.category
                                inner join  tb_quiz_actividad E on E.id_actividad = A.id
                                inner join  tb_metadata_quiz F on F.id_quiz = E.id_quiz
                                where A.id =%d""", int(pId_actividad))

    except Exception, e:
        curso = metadata[0][0]
        pmensaje = "Ha ocurrido un error. Erro: %s" %e
        presultado = "Fallida"
        perror = "%s" %e
        pname = metadata[0][3]
        pactivitie = metadata[0][1]
        pcategorie = metadata[0][2]
        pfecha = pFecha
        pduracion = pDuracion
        phora = pInicio
        pestado = "Error"
        presult = 0

    else:
        curso = metadata[0][0]
        pmensaje = "Se ha programado el la activadad correctamente"
        presultado = "Exitosa"
        perror = None
        pname = metadata[0][3]
        pactivitie = metadata[0][1]
        pcategorie = metadata[0][2]
        pfecha = pFecha
        pduracion = pDuracion
        phora = pInicio
        pestado = "Pendiente de inicio"
        presult = 1
        
    finally:
        return dict(mensaje = pmensaje, resultado = presultado, error = perror, result = presult,  
        name = pname, activitie = pactivitie, categorie = pcategorie, fecha = pfecha, duracion = pduracion, hora = phora, estado = pestado, curso= curso)


@auth.requires_login()
def test_programacion_protegida():
    print "Si llego"
    mensaje = ""
    try:
        pId_actividad = request.vars['id_actividad']
        pId_quiz = request.vars['id_quiz']
        pFecha = request.vars['fecha']
        pInicio = request.vars['inicio']
        pDuracion = request.vars['duracion']
        pClave = request.vars['clave']

        print 'La actividad es: ' + pId_actividad
        print 'El quiz es: ' + pId_quiz
        print 'La fecha es: ' + pFecha
        print 'La hora de incio es: ' + pInicio
        print 'La duracion es: ' + pDuracion
        print 'La clave es: ' + pClave

        db.tb_quiz_actividad.insert(
            id_actividad = pId_actividad,
            id_quiz = pId_quiz,
            fecha = pFecha,
            inicio= pInicio,
            duracion= pDuracion,
            finalizado= 0,
            private=  1,
            keyword= pClave
            )
        db.commit()

        metadata = db.executesql("""select 
		                                B.name as curso, 
		                                A.name as actividad, 
                                        D.category as categoria, 
                                        F.nombre as quiz,
                                        E.keyword as clave 
                                from course_activity A
                                inner join  project B on B.id = A.assignation
                                inner join  course_activity_category C on A.course_activity_category = C.id
                                inner join  activity_category D on D.id = C.category
                                inner join  tb_quiz_actividad E on E.id_actividad = A.id
                                inner join  tb_metadata_quiz F on F.id_quiz = E.id_quiz
                                where A.id =%d""", int(pId_actividad))

    except Exception, e:
        curso = metadata[0][0]
        pmensaje = "Ha ocurrido un error. Erro: %s" %e
        presultado = "Fallida"
        perror = "%s" %e
        pname = metadata[0][3]
        pactivitie = metadata[0][1]
        pcategorie = metadata[0][2]
        pkeyword = metadata[0][4]
        pfecha = pFecha
        pduracion = pDuracion
        phora = pInicio
        pestado = "Error"
        presult = 0

    else:
        curso = metadata[0][0]
        pmensaje = "Se ha programado el la activadad correctamente"
        presultado = "Exitosa"
        perror = None
        pname = metadata[0][3]
        pactivitie = metadata[0][1]
        pcategorie = metadata[0][2]
        pkeyword = metadata[0][4]
        pfecha = pFecha
        pduracion = pDuracion
        phora = pInicio
        pestado = "Pendiente de inicio"
        presult = 1
        
    finally:
        return dict(mensaje = pmensaje, resultado = presultado, error = perror, result = presult,  
        name = pname, activitie = pactivitie, categorie = pcategorie, fecha = pfecha, duracion = pduracion, 
        hora = phora, estado = pestado, curso= curso,
        keyword = pkeyword)
