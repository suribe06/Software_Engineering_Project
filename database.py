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
	ans = False
	if person1.one() == None and person2.one() == None:
		ans = True
		sessionDB.execute("INSERT INTO civil (username,ndocumento,apellidos,barrio,correo,departamento,direccion,municipio,nacimiento,nombres,password,sexo,tdocumento,telefono) VALUES('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}',{13})".format(usr,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,pasw,sex,tdoc,tel))
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,1))
	return ans

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
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,3))
		if len(tel) == 3:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{12}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],tel[2],cat))
		elif len(tel) == 2:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{11}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],cat))
		else:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{10}','{3}','{4}','{5}','{6}','{7}','{8}',{9},NULL,NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],cat))
	return

def regExam(n,td,nd,rsol):
    """
    Entrada: un entero n el cual hace referencia al NIT de la entidad de salud, td el cual es un string que hace referencia al tipo de
             documento del civil al que se le va a registar el examen de COVID-19, y un entero nd el cual hace referencia al numero de
             documento del civil al que se le va a registar el examen de COVID-19.
    """
    exa = sessionDB.execute("SELECT COUNT(*) from examenes WHERE ndocumento = {0} and tdocumento = '{1}' and nit = {2} allow filtering".format(nd,td,n))
    i = int(exa.one().count)+1
    dia = dt.datetime.today()
    sessionDB.execute("INSERT INTO examenes (id,nit,ndocumento,efecha,resultado,rfecha,tdocumento,rsocial) VALUES({6},{0},{1},'{2}-{3}-{4}','Evaluando',NULL,'{5}','{7}')".format(n,nd,dia.year,dia.strftime("%m"),dia.strftime("%d"),td,i,rsol))
    return

def regResExam(id,n,nd,res,td):
    e = sessionDB.execute("SELECT ndocumento from examenes WHERE id = {0} and ndocumento = {1} and nit = {2} and tdocumento = '{3}'".format(id,nd,n,td))
    if e.one() != None:
        dia = dt.datetime.now()
        sessionDB.execute("UPDATE examenes SET rfecha = '{0}-{1}-{2}', resultado = '{6}' WHERE id = {3} and Nit = {4} and ndocumento = {5} and tdocumento = '{7}'".format(dia.year,dia.strftime("%m"),dia.strftime("%d"),id,n,nd,res,td))
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
	if pasw != None:
		exe+= "password = '{0}',".format(pasw)
		sessionDB.execute("UPDATE usuarios SET password = '{1}' WHERE username = '{0}'".format(usr,pasw))
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
		print(exe)
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

def regVisita(ni,nd,td,nom,ape,tem,tap,rsol,cat):
    person = sessionDB.execute("SELECT nombres,apellidos from civil WHERE ndocumento = {0} and tdocumento = '{1}'allow filtering".format(nd,td))
    if person.one() != None:
        visi = sessionDB.execute("SELECT COUNT(*) from visitas WHERE ndocumento = {0} and nit = {2} and tdocumento = '{1}'allow filtering".format(nd,td,ni))
        i = int(visi.one().count) + 1
        cuar,enfer = cuarentena(nd,td)
        dia = dt.datetime.now()
        temperatura = tem <= 37
        ans = tap and temperatura and not(cuar) and not(enfer)
        if ans == True:
            sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{15}','{4}-{5}-{6}','{12}:{13}:{14}','{7}','NA','{11}',{8},'{9}',{10},True)".format(i,ni,nd,ape,dia.year,dia.strftime("%m"),dia.strftime("%d"),nom,tap,td,tem,rsol,dia.hour,dia.minute,dia.second,cat))
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
            sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{16}','{4}-{5}-{6}','{13}:{14}:{15}','{7}','{8}','{12}',{9},'{10}',{11},False)".format(i,ni,nd,ape,dia.year,dia.strftime("%m"),dia.strftime("%d"),nom,razon,tap,td,tem,rsol,dia.hour,dia.minute,dia.second,cat))
    return

def hVisitas(nd,td):
    v = sessionDB.execute("SELECT * from visitas WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
    visi = []
    for obj in v:
        if obj.veredict == True: b = "Aceptado"
        else: b = "Denegado"
        a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
        c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
        pub = sessionDB.execute("SELECT rsocial from publica WHERE nit = {0} allow filtering".format(obj.nit))
        pers = [pub.one().rsocial,obj.categoria,a,c,b,obj.reason]
        visi.append(pers)
    return visi

def hExamenes(nd,td):
    e = sessionDB.execute("SELECT * from examenes WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
    exa = []
    for obj in e:
        a = str(obj.efecha.date().year)+"-"+str(obj.efecha.date().month)+"-"+str(obj.efecha.date().day)
        if obj.rfecha != None: b = str(obj.rfecha.date().year)+"-"+str(obj.rfecha.date().month)+"-"+str(obj.rfecha.date().day)
        else: b = "NA"
        pers = [obj.rsocial,a,b,obj.resultado]
        exa.append(pers)
    return exa

def hExamenesS(n):
    e = sessionDB.execute("SELECT * from examenes WHERE nit = {0} allow filtering".format(n))
    exa = []
    for obj in e:
        a = str(obj.efecha.date().year)+"-"+str(obj.efecha.date().month)+"-"+str(obj.efecha.date().day)
        if obj.rfecha != None: b = str(obj.rfecha.date().year)+"-"+str(obj.rfecha.date().month)+"-"+str(obj.rfecha.date().day)
        else: b = "NA"
        pers = [obj.id,obj.ndocumento,a,b,obj.resultado]
        exa.append(pers)
    return exa

def hVisitasP(n):
    v = sessionDB.execute("SELECT * from visitas WHERE nit = {0} allow filtering".format(n))
    visi = []
    for obj in v:
        if obj.veredict == True: b = "Aceptado"
        else: b = "Denegado"
        a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
        c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
        pers = [obj.tdocumento,obj.ndocumento,a,c,b,obj.reason]
        visi.append(pers)
    return visi

def getNitP(usr):
    person = sessionDB.execute("SELECT Nit from Publica where username = '{0}'".format(usr))
    return person.one().nit

def getNitS(usr):
    person = sessionDB.execute("SELECT Nit from salud where username = '{0}'".format(usr))
    return person.one().nit

def getCatRsol(usr):
    person = sessionDB.execute("SELECT rsocial, categoria from publica where username = '{0}'".format(usr))
    return person.one().rsocial,person.one().categoria

def editS(usr,n,bar,cor,dep,dire,mun,pasw,rsol,tel1,tel2,tel3):
	exe = "UPDATE salud SET "
	exe1 = " WHERE username = '{0}' and nit = {1}".format(usr,n)
	if bar != None:	exe+= "bar = '{0}',".format(pasw)
	if cor != None: exe+= "correo = '{0}',".format(cor)
	if dep != None: exe+="departamento = '{0}',".format(dep)
	if dire != None: exe+="direccion = '{0}',".format(dire)
	if mun != None: exe+="municipio = '{0}',".format(mun)
	if pasw != None:
		sessionDB.execute("UPDATE usuarios SET password = '{1}' WHERE username = '{0}'".format(usr,pasw))
		exe+="password = '{0}',".format(pasw)
	if rsol != None: exe+="rsocial = '{0}',".format(rsol)
	if tel1 != None: exe+="telefono1 = {0},".format(tel1)
	if tel2 != None: exe+="telefono2 = {0},".format(tel2)
	if tel3 != None: exe+="telefono3 = {0},".format(tel3)
	if len(exe) > 17:
		exe = exe[:len(exe)-1]
		exe+= exe1
		sessionDB.execute(exe)
	return

def editP(usr,n,bar,cor,dep,dire,mun,pasw,rsol,tel1,tel2,tel3):
	exe = "UPDATE publica SET "
	exe1 = " WHERE username = '{0}' and nit = {1}".format(usr,n)
	if bar != None: exe+= "barrio = '{0}',".format(bar)
	if cor != None: exe+= "correo = '{0}',".format(cor)
	if dep != None: exe+="departamento = '{0}',".format(dep)
	if dire != None: exe+="direccion = '{0}',".format(dire)
	if mun != None: exe+="municipio = '{0}',".format(mun)
	if pasw != None:
		sessionDB.execute("UPDATE usuarios SET password = '{1}' WHERE username = '{0}'".format(usr,pasw))
		exe+="password = '{0}',".format(pasw)
	if rsol != None: exe+="rsocial = '{0}',".format(rsol)
	if tel1 != None: exe+="telefono1 = {0},".format(tel1)
	if tel2 != None: exe+="telefono2 = {0},".format(tel2)
	if tel3 != None: exe+="telefono3 = {0},".format(tel3)
	if len(exe) > 19:
		exe = exe[:len(exe)-1]
		exe+= exe1
		sessionDB.execute(exe)
	return

def getCorC(usr):
    person = sessionDB.execute("SELECT correo from civil where username = '{0}'".format(usr))
    return person.one().correo

def getCorP(usr):
    person = sessionDB.execute("SELECT correo from publica where username = '{0}'".format(usr))
    return person.one().correo

def getCorS(usr):
    person = sessionDB.execute("SELECT correo from salud where username = '{0}'".format(usr))
    return person.one().correo

def getPass(usr):
    person = sessionDB.execute("SELECT password from usuarios where username = '{0}'".format(usr))
    return person.one().password

def fVisitasC(nd,td,cat,fi,ff):
    exe = "SELECT * from visitas where ndocumento = {0} and tdocumento = '{1}' ".format(nd,td)
    exe1 = "allow filtering"
    if fi != None: exe += "and fent >= '{0}' ".format(fi)
    if ff != None: exe += "and fent <= '{0}' ".format(ff)
    if cat != None: exe += "and categoria = '{0}' ".format(cat)
    exe += exe1
    v = sessionDB.execute(exe)
    visi = []
    for obj in v:
        if obj.veredict == True: b = "Aceptado"
        else: b = "Denegado"
        a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
        c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
        pers = [obj.rsocial,obj.categoria,a,c,b,obj.reason]
        visi.append(pers)
    return visi

def allVisitas():
    """
    Entrada:
    Salida:Una lista con todas las vistas registradas en el sistema
    """
    v = sessionDB.execute("SELECT * from visitas")
    visi = []
    for obj in v:
        if obj.veredict == True: b = "Aceptado"
        else: b = "Denegado"
        a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
        c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
        pub = sessionDB.execute("SELECT rsocial from publica WHERE nit = {0} allow filtering".format(obj.nit))
        pers = [pub.one().rsocial,obj.tdocumento,obj.ndocumento,a,c,b,obj.reason]
        visi.append(pers)
    return visi

def allExamenes():
    """
    Entrada:
    Salida:Una lista con todas los examenes registrados en el sistema
    """
    e = sessionDB.execute("SELECT * from examenes")
    exa = []
    for obj in e:
        a = str(obj.efecha.date().year)+"-"+str(obj.efecha.date().month)+"-"+str(obj.efecha.date().day)
        if obj.rfecha != None: b = str(obj.rfecha.date().year)+"-"+str(obj.rfecha.date().month)+"-"+str(obj.rfecha.date().day)
        else: b = "NA"
        sal = sessionDB.execute("SELECT rsocial from salud WHERE nit = {0} allow filtering".format(obj.nit))
        pers = [sal.one().rsocial,obj.tdocumento,obj.ndocumento,a,b,obj.resultado]
        exa.append(pers)
    return exa

def registroA(usr,pasw,nom,ape):
    u = sessionDB.execute("SELECT tipo from usuarios WHERE username = '{0}'".format(usr))
    if u.one() == None:
        sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,0))
        sessionDB.execute("INSERT INTO admins (username, password, nombres, apellidos) VALUES ('{0}','{1}','{2}','{3}')".format(usr,pasw,nom,ape))
    return

def deleteU(usr):
    u = sessionDB.execute("SELECT * from usuarios WHERE username = '{0}'".format(usr))
    if u.one() != None:
        tipo = getTipo(usr)
        sessionDB.execute("DELETE FROM usuarios WHERE username = '{0}'".format(usr))
        if tipo == 0:
            sessionDB.execute("DELETE FROM admins WHERE username = '{0}'".format(usr))
        elif tipo == 1:
            td = getTd(usr)
            nd = getNd(usr)
            sessionDB.execute("DELETE FROM civil WHERE username = '{0}' and ndocumento = {1} and tdocumento = '{2}'".format(usr,nd,td))
        elif tipo == 2:
            n = getNitS(usr)
            sessionDB.execute("DELETE FROM salud WHERE username = '{0}' and nit = {1}".format(usr,n))
        elif tipo == 3:
            n = getNitP(usr)
            sessionDB.execute("DELETE FROM publica WHERE username = '{0}' and nit = {1}".format(usr,n))
    return

def getRsolS(usr):
    person = sessionDB.execute("SELECT rsocial from salud where username = '{0}'".format(usr))
    return person.one().rsocial

def editA(usr,pasw,nom,ape):
    exe = "UPDATE admins SET "
    exe1 = " WHERE username = '{0}'".format(usr)
    if pasw != None:
        sessionDB.execute("UPDATE usuarios SET password = '{1}' WHERE username = '{0}'".format(usr,pasw))
        exe+="password = '{0}',".format(pasw)
    if nom != None: exe+="nombres = '{0}',".format(nom)
    if ape != None: exe+="apellidos = '{0}',".format(ape)
    if len(exe) > 18:
        exe = exe[:len(exe)-1]
        exe+= exe1
        sessionDB.execute(exe)
    return

def regVDestiempo(ni,nd,td,nom,ape,tem,tap,rsol,cat,fecha,hora):
    person = sessionDB.execute("SELECT nombres,apellidos from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
    if person.one() != None:
        visi = sessionDB.execute("SELECT COUNT(*) from visitas WHERE ndocumento = {0} and tdocumento = '{1}' and nit = {2} allow filtering".format(nd,td,ni))
        i = int(visi.one().count)+1
        temperatura = tem <= 37
        ans = temperatura and tap
        if ans:
            sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{11}','{4}','{10}:00','{5}','NA','{9}',{6},'{7}',{8},True)".format(i,ni,nd,ape,fecha,nom,tap,td,tem,rsol,hora,cat))
        else:
            razon = ''
            if not(tap):
                razon = razon + '- No porta tapabocas '
            if not(temperatura):
                razon = razon + '- Temperatura elevada '
            sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{11}','{4}','{10}:00','{5}','{12}','{9}',{6},'{7}',{8},False)".format(i,ni,nd,ape,fecha,nom,tap,td,tem,rsol,hora,cat,razon))
    return

def fExamenesC(nd,td,result,fi,ff):
    exe = "SELECT * from examenes where ndocumento = {0} and tdocumento = '{1}' ".format(nd,td)
    exe1 = "allow filtering"
    if fi != None: exe += "and efecha >= '{0}' ".format(fi)
    if ff != None: exe += "and efecha <= '{0}' ".format(ff)
    if result != None: exe += "and resultado = '{0}' ".format(result)
    exe += exe1
    e = sessionDB.execute(exe)
    exa = []
    for obj in e:
        a = str(obj.efecha.date().year)+"-"+str(obj.efecha.date().month)+"-"+str(obj.efecha.date().day)
        if obj.rfecha != None: b = str(obj.rfecha.date().year)+"-"+str(obj.rfecha.date().month)+"-"+str(obj.rfecha.date().day)
        else: b = "NA"
        sal = sessionDB.execute("SELECT rsocial from salud WHERE nit = {0} allow filtering".format(obj.nit))
        pers = [sal.one().rsocial,a,b,obj.resultado]
        exa.append(pers)
    return exa

def fVisitasP(ni,ver,fi,ff):
    exe = "SELECT * from visitas where nit = {0} ".format(ni)
    exe1 = "allow filtering"
    if fi != None: exe += "and fent >= '{0}' ".format(fi)
    if ff != None: exe += "and fent <= '{0}' ".format(ff)
    if ver != None: exe += "and veredict = {0} ".format(ver)
    exe += exe1
    v = sessionDB.execute(exe)
    visi = []
    for obj in v:
        if obj.veredict == True: b = "Aceptado"
        else: b = "Denegado"
        a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
        c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
        pers = [obj.ndocumento,obj.tdocumento,a,c,b,obj.reason]
        visi.append(pers)
    return visi

def fExamenesS(ni,result,fi,ff):
    exe = "SELECT * from examenes where nit = {0} ".format(ni)
    exe1 = "allow filtering"
    if fi != None: exe += "and efecha >= '{0}' ".format(fi)
    if ff != None: exe += "and efecha <= '{0}' ".format(ff)
    if result != None: exe += "and resultado = '{0}' ".format(result)
    exe += exe1
    e = sessionDB.execute(exe)
    exa = []
    for obj in e:
        a = str(obj.efecha.date().year)+"-"+str(obj.efecha.date().month)+"-"+str(obj.efecha.date().day)
        if obj.rfecha != None: b = str(obj.rfecha.date().year)+"-"+str(obj.rfecha.date().month)+"-"+str(obj.rfecha.date().day)
        else: b = "NA"
        pers = [obj.id,obj.ndocumento,a,b,obj.resultado]
        exa.append(pers)
    return exa

def getEdad(usr):
	today_date = dt.datetime.now().date()
	person = sessionDB.execute("SELECT nacimiento from civil where username = '{0}'".format(usr))
	birth_date = person.one().nacimiento.date()
	age = today_date - birth_date
	return int((age.days)/365)

def getEstrato(usr):
	person = sessionDB.execute("SELECT estrato from civil where username = '{0}'".format(usr))
	return person.one().estrato

def salidas_recientes(nd, td):
	"""
	Esta funcion retorna el numero de visitas de un usuario en el rango de un mes
	"""
	dia = dt.datetime.now()
	dia -= dt.timedelta(days = 31)
	v = sessionDB.execute("SELECT * from visitas WHERE ndocumento = {0} and tdocumento = '{1}' and fent >= '{2}-{3}-{4}' allow filtering".format(nd,td,dia.year,dia.strftime("%m"),dia.strftime("%d")))
	ans = 0
	for obj in v:
		ans += 1
	return ans
