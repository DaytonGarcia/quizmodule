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
    project = db(db.project.creador==idproject).select().first()  
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
    return dict(periodo = period, course=project, period=periodo)

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
def getJsonQuiz():
    import redis
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    ide = request.vars['id']
    lista = db(db.tb_metadata_quiz.id_quiz==ide).select(
        db.tb_metadata_quiz.creador, 
        db.tb_metadata_quiz.curso)

    creador = 0
    curso = 0

    for quiz in lista:
        creador = quiz.creador
        curso = quiz.curso
    cadenaRedis = 'uid:'+str(creador)+':curso:'+str(curso)+':quiz:'+str(ide)
    r.hget('preguntas',cadenaRedis)
    return r