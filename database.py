from cassandra.cluster import Cluster
import datetime as dt

cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
sessionDB = cluster.connect("bdis")

def inicio(usr,pasw):
	"""
	Entrada:Un string usr el cual hace referencia al usuername que el usuaria introduce en el sistema, pasw es un
			un string el cual hace referencia a la contraseña que el usuario introduce en el sistema
	Salida: un booleano ans el cual define si el usuario logró entrar en el sistema, un entero tp el cual dependiendo del tipo
			de usuario que hizo login el sistema este cambia (0: admin, 1: civil, 2:establecimiento publico, 3: establecimiento de salud,
			-1: si no se hace login)
	Funcionamiento: utilizando CQL se hace una query en la tabla usuarios para obtener la contraseña y el tipo de usuario dependiendo del
					username en cuestion, una vez teniendo eso se valida si el usuario existe, de ser asi se valida si la contraseña ingresada
					es igual a la contraseña alamcenada en la base de datos, y con base en eso se da un veredicto
	"""
	tp = -1
	person = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	if person.one() == None or person.one().password != pasw: ans = False
	else:ans,tp = True, person.one().tipo
	return ans,tp

def registroC(usr,pasw,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,sex,tdoc,tel):
	"""
	Entrada:usr que es username, pasw que es password, ndoc que es numero de documento, ape que es apellidos, bar que es barrio, cor que es correo,
			dep que es departamento, dire que es direccion, mun que es municipio, nac que es fecha de nacimiento, nom que es nombres, sex que es el
			genero,tdoc que es el tipo de documento y tel que es telefono
	Salida:
	Funcionamiento:Se toman cada una de los valores que llegan a la funcion y utlizando sentencias CQL se ingresan los datos en la tabla civil, ademas
				   se insertan tambien el username, la contraseña y el tipo de usuario en la tabla usuarios, en este caso a ser civil el tipo es 1
	"""
	person1 = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	person2 = sessionDB.execute("SELECT password from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(ndoc,tdoc))
	if person1.one() == None and person2.one() == None:
		sessionDB.execute("INSERT INTO civil (username,ndocumento,apellidos,barrio,correo,departamento,direccion,municipio,nacimiento,nombres,password,sexo,tdocumento,telefono) VALUES('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}',{13})".format(usr,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,pasw,sex,tdoc,tel))
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,1))
	return

def registroS(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel):
	ent1 = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	ent2 = sessionDB.execute("SELECT username, Nit from salud WHERE Nit = {0} allow filtering".format(n))
	if ent1.one() == None and ent2.one() == None:
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,2))
		if len(tel) == 3:
			sessionDB.execute("INSERT INTO salud (username,Nit,barrio,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],tel[2]))
		elif len(tel) == 2:
			sessionDB.execute("INSERT INTO salud (username,Nit,barrio,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1]))
		else:
			sessionDB.execute("INSERT INTO salud (username,Nit,barrio,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},NULL,NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0]))
	return

def registroP(usr,n,bar,cat,cor,dep,dir,mun,pasw,rsol,tel):
	ent1 = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	ent2 = sessionDB.execute("SELECT username, Nit from publica WHERE Nit = {0} allow filtering".format(n))
	if ent1.one() == None and ent2.one() == None:
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,2))
		if len(tel) == 3:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{12}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],tel[2],cat))
		elif len(tel) == 2:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{11}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],cat))
		else:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{10}','{3}','{4}','{5}','{6}','{7}','{8}',{9},NULL,NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],cat))
	return

def regExam(id,n,td,nd,rsol):
    """
    Entrada: un entero n el cual hace referencia al NIT de la entidad de salud, td el cual es un string que hace referencia al tipo de
             documento del civil al que se le va a registar el examen de COVID-19, y un entero nd el cual hace referencia al numero de
             documento del civil al que se le va a registar el examen de COVID-19.
    Salida:
    Funcionamiento: Mediante el uso de CQL se hacen 2 queries, la primera para obtener la entidad de salud con respecto a su NIT, y así verificar que
                    esta entidad existe, la segunda query es para obtener el civil con el numero de documento indicado y el tipo de documento ingresado
                    esta registrado en el sistema, de ser así se toma la fecha del día en el que se está registrando el examen y se registra la nit del
                    establecimiento de salud, la fecha en la que se realiza el registro, el resultado (antes de obtener un veredicto se guarda como Evaluando)
                    la fecha en la que se entrega el resultado (antes de obtener el veredicto se guarda como NULL), y el numero y tipo de documento del civil en cuestion
    """
    sal = sessionDB.execute("SELECT username,nit from salud WHERE nit = {0} allow filtering".format(n))
    person = sessionDB.execute("SELECT * from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
    if person.one() != None and    sal.one() != None:
        dia = dt.datetime.now()
        sessionDB.execute("INSERT INTO examenes (id,nit,ndocumento,efecha,resultado,rfecha,tdocumento,rsocial) VALUES({6},{0},{1},'{2}-{3}-{4}','Evaluando',NULL,'{5}','{7}')".format(n,nd,dia.year,dia.strftime("%m"),dia.strftime("%d"),td,id,rsol))
    return

def regResExam(id,n,nd,res,td):
    e = sessionDB.execute("SELECT ndocumento from examenes WHERE Id = {0} and ndocumento = {1} and nit = {2} and tdocumento = '{3}'".format(id,nd,n,td))
    if e.one() != None:
        dia = dt.datetime.now()
        sessionDB.execute("UPDATE examenes SET rfecha = '{0}-{1}-{2}', resultado = '{6}' WHERE Id = {3} and Nit = {4} and ndocumento = {5} and tdocumento = '{7}'".format(dia.year,dia.strftime("%m"),dia.strftime("%d"),id,n,nd,res,td))
    return

def getNd(usr):
    person = sessionDB.execute("SELECT ndocumento from civil where username = '{0}'".format(usr))
    return person.one().ndocumento

def getTd(usr):
    person = sessionDB.execute("SELECT tdocumento from civil where username = '{0}'".format(usr))
    return person.one().tdocumento

def getTipo(usr):
    person = sessionDB.execute("SELECT tipo from usuarios where username = '{0}'".format(usr))
    return person.one().tipo

def editC(usr,pasw,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,sex,tdoc,tel):
    exe = "UPDATE civil SET "
    exe1 = " WHERE username = '{0}' and ndocumento = {1} and tdocumento = '{2}'".format(usr,ndoc,tdoc)
    if pasw != None: exe+= "password = '{0}',".format(pasw)
    if ape != None: exe+="apellidos = '{0}',".format(ape)
    if bar != None: exe+="barrio = '{0}',".format(bar)
    if cor != None: exe+= "correo = '{0}',".format(cor)
    if dep != None: exe+="departamento = '{0}',".format(dep)
    if dire != None: exe+="direccion = '{0}',".format(dire)
    if mun != None: exe+="municipio = '{0}',".format(mun)
    if nac != None: exe+="nacimiento = '{0}',".format(nac)
    if nom != None: exe+="nombres = '{0}',".format(nom)
    if sex != None: exe+="sexo = '{0}',".format(sex)
    if tel != None: exe+="telefono = {0},".format(tel)
    if len(exe) > 17:
        exe = exe[:len(exe)-1]
        exe+= exe1
        sessionDB.execute(exe)
    return

def cuarentena(nd,td):
    cuar = False
    enfer = False
    dia = dt.datetime.now()
    dia -= dt.timedelta(days = 14)
    sinres = sessionDB.execute("SELECT * from examenes where ndocumento = {0} and tdocumento = '{1}' and efecha >= '{2}-{3}-{4}' and resultado = 'Evaluando' allow filtering".format(nd,td,dia.year,dia.strftime("%m"),dia.strftime("%d")))
    conres = sessionDB.execute("SELECT * from examenes where ndocumento = {0} and tdocumento = '{1}' and rfecha >= '{2}-{3}-{4}' and resultado = 'Positivo' allow filtering".format(nd,td,dia.year,dia.strftime("%m"),dia.strftime("%d")))
    if sinres.one() != None: cuar = True
    if conres.one() != None: enfer = True
    return cuar, enfer

def regVisita(i,ni,nd,td,nom,ape,tem,tap,rsol):
    person = sessionDB.execute("SELECT nombres,apellidos from civil WHERE ndocumento = {0} and tdocumento = '{1}'allow filtering".format(nd,td))
    if person.one() != None:
        cuar,enfer = cuarentena(nd,td)
        dia = dt.datetime.now()
        temperatura = tem <= 37
        ans = tap and temperatura and not(cuar) and not(enfer)
        if ans == True:
            sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,fent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{4}-{5}-{6}','{7}','NA','{11}',{8},'{9}',{10},True)".format(i,ni,nd,ape,dia.year,dia.strftime("%m"),dia.strftime("%d"),nom,tap,td,tem,rsol))
        else:
            razon = ''
            if not(tap):
                razon = razon + '- No porta tapabocas '
            if not(temperatura):
                razon = razon + '- Temperatura elevada '
            if enfer:
                razon = razon + '- Positivo por COVID-19 '
            if cuar:
                razon = razon + '- En cuarentena por examen '
            sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,fent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{4}-{5}-{6}','{7}','{8}','{12}',{9},'{10}',{11},False)".format(i,ni,nd,ape,dia.year,dia.strftime("%m"),dia.strftime("%d"),nom,razon,tap,td,tem,rsol))
    return

def hVisitas(nd,td):
    v = sessionDB.execute("SELECT * from visitas WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
    visi = []
    for obj in v:
        if obj.veredict == True: b = "Aceptado"
        else: b = "Denegado"
        a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
        pers = [obj.rsocial,a,b,obj.reason]
        visi.append(pers)
    return visi
