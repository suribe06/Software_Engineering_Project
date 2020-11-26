from cassandra.cluster import Cluster
from flask import *
import requests, csv
from database import inicio, registroC, registroP, registroS
from QR import makeQR, readQR
from cryption import encriptar

#Configuramos la app de flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

#Funciones de cada vista
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form["b1"]=="Iniciar sesion":
            u = request.form['user']
            p = encriptar(request.form['pass'])
            ans, tp = inicio(u, p)
            if ans:
                if tp == 1:
                    session['user'] = request.form['user']
                    return redirect(url_for('main_civil'))
            else:
                flash("Usuario o contraseña incorrecta")
        elif request.form["b1"]=="Registrarse":
            return redirect(url_for('register_select'))

    return render_template('login.html')

@app.route('/register_select', methods=['GET','POST'])
def register_select():
    if request.method == 'POST':
        select_tipo = str(request.form.get('tipoR'))
        if select_tipo == "C":
            return redirect(url_for('register_civil'))
        elif select_tipo == "EP":
            return redirect(url_for('register_publico'))
        elif select_tipo == "ES":
            return redirect(url_for('register_salud'))
    return render_template('register_select.html')

@app.route('/register_civil', methods=['GET','POST'])
def register_civil():
    if request.method == 'POST':
        nombres_ = request.form['nombres']
        apellidos_ = request.form['apellidos']
        fecha_ = request.form['fecha']
        tipoDoc = request.form['tipoDocumento']
        numDoc = request.form['numeroDocumento']
        dept = request.form['departamento']
        mun = request.form['municipio']
        barrio_ = request.form['barrio']
        dire = request.form['direccion']
        genero_ = request.form['genero']
        tel = request.form['telefono']
        email = request.form['correo']
        u = request.form['username']
        p = encriptar(request.form['password'])
        #Registro del civil en la base de datos
        registroC(u, p, int(numDoc), apellidos_, barrio_, email, dept, dire, mun, fecha_, nombres_, genero_, tipoDoc, int(tel))
        data = {}
        data["Nombre"] = nombres_
        data["Apellido"] = apellidos_
        data["Tipo Documento"] = tipoDoc
        data["Numero Documento"] = numDoc
        #Se crea el codigo qr del civil
        makeQR(data)
        return redirect(url_for('login'))
    return render_template('register_civil.html')

@app.route('/register_publico', methods=['GET','POST'])
def register_publico():
    if request.method == 'POST':
        nit_ = request.form['NIT']
        razon_ = str(request.form.get('razon'))
        dept_ = str(request.form.get('departamento'))
        mun_ = str(request.form.get('municipio'))
        barrio_ = str(request.form.get('barrio'))
        dir_ = request.form['direccion']
        tels = []
        t1 = request.form['T1']
        tels.append(int(t1))
        t2 = request.form['T2']
        if len(t2) != 0: tels.append(int(t2))
        t3 = request.form['T3']
        if len(t3) != 0: tels.append(int(t3))
        email = request.form['correo']
        u = request.form['username']
        p = encriptar(request.form['password'])
        #Registro de la entidad publica en la base de datos
        registroP(u, int(nit_), barrio_, razon_, email, dept_, dir_, mun_, p, razon_, tels)
        return redirect(url_for('login'))
    return render_template('register_publico.html')

@app.route('/register_salud', methods=['GET','POST'])
def register_salud():
    if request.method == 'POST':
        nit_ = request.form['NIT']
        razon_ = str(request.form.get('razon'))
        dept_ = str(request.form.get('departamento'))
        mun_ = str(request.form.get('municipio'))
        barrio_ = str(request.form.get('barrio'))
        dir_ = request.form['direccion']
        tels = []
        t1 = request.form['T1']
        tels.append(int(t1))
        t2 = request.form['T2']
        if len(t2) != 0: tels.append(int(t2))
        t3 = request.form['T3']
        if len(t3) != 0: tels.append(int(t3))
        email = request.form['correo']
        u = request.form['username']
        p = encriptar(request.form['password'])
        #Registro de la entidad salud en la base de datos
        registroS(u, int(nit_), barrio_, email, dept_, dir_, mun_, p, razon_, tels)
        return redirect(url_for('login'))
    return render_template('register_salud.html')

@app.route('/main_civil', methods=['GET','POST'])
def main_civil():
    usuario = None
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))

    return render_template('main_civil.html', usuario=usuario)

if __name__ == "__main__":
    app.debug = True
    app.run()
