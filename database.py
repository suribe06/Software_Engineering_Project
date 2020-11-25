from cassandra.cluster import Cluster
import datetime as dt

cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect("bdis")

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
	person = session.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	if person.one() == None or person.one().password != pasw: ans = False
	else:ans,tp = True, person.one().tipo
	return ans,tp

def registroC(usr,pasw,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,sex,tdoc,tel):
	"""
	Entrada:usr que es username, pasw que es password, ndoc que es numero de documento, ape que es apellidos, bar que es barrio, cor que es correo,
			dep que es departamento, dire que es direccion, mun que es municipio, nac que es fecha de nacimiento, nom que es nombres, sex que es el
			genero,tdoc que es el tipo de documento y tel que es telefono
	Salida:
	Funcionamiento: Se toman cada una de los valores que llegan a la funcion y utlizando sentencias CQL se ingresan los datos en la tabla civil, ademas
				   se insertan tambien el username, la contraseña y el tipo de usuario en la tabla usuarios, en este caso a ser civil el tipo es 1
	"""
	person1 = session.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	person2 = session.execute("SELECT password from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(ndoc,tdoc))
	if person1.one() == None and person2.one() == None:
		session.execute("INSERT INTO civil (username,ndocumento,apellidos,barrio,correo,departamento,direccion,municipio,nacimiento,nombres,password,sexo,tdocumento,telefono) VALUES('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}',{13})".format(usr,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,pasw,sex,tdoc,tel))
		session.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,1))
	return

def RegistroS(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel):
	ent1 = session.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	ent2 = session.execute("SELECT username, Nit from salud WHERE Nit = {0} allow filtering".format(n))
	if ent1.one() == None and ent2.one() == None:
		session.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,2))
		if len(tel) == 3:
			session.execute("INSERT INTO salud (username,Nit,barrio,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],tel[2]))
		elif len(tel) == 2:
			session.execute("INSERT INTO salud (username,Nit,barrio,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1]))
		else:
			session.execute("INSERT INTO salud (username,Nit,barrio,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},NULL,NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0]))
	return

def RegistroP(usr,n,bar,cat,cor,dep,dir,mun,pasw,rsol,tel):
	ent1 = session.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	ent2 = session.execute("SELECT username, Nit from publica WHERE Nit = {0} allow filtering".format(n))
	if ent1.one() == None and ent2.one() == None:
		session.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,2))
		if len(tel) == 3:
			session.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{12}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],tel[2],cat))
		elif len(tel) == 2:
			session.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{11}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],cat))
		else:
			session.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{10}','{3}','{4}','{5}','{6}','{7}','{8}',{9},NULL,NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],cat))
	return


def regExam(id,n,td,nd):
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
	sal = session.execute("SELECT username,nit from salud WHERE nit = {0} allow filtering".format(n))
	person = session.execute("SELECT * from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
	if person.one() != None and	sal.one() != None:
		dia = dt.datetime.today()
		session.execute("INSERT INTO examenes (id,nit,ndocumento,efecha,resultado,rfecha,tdocumento) VALUES({6},{0},{1},'{2}-{3}-{4}','Evaluando',NULL,'{5}')".format(n,nd,dia.year,dia.month,dia.day,td,id))
	return

def regResultExam(id,n,nd,res):	
	e = session.execute("SELECT ndocumento from examenes WHERE Id = {0}".format(id))
	if e.one() != None:
		dia = dt.datetime.today()
		session.execute("UPDATE examenes SET rfecha = '{0}-{1}-{2}', resultado = '{6}' WHERE Id = {3} and Nit = {4} and ndocumento = {5}".format(dia.year,dia.month,dia.day,id,n,nd,res))
	return
