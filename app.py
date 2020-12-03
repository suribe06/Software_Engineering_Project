from cassandra.cluster import Cluster
from flask import *
import requests, csv
from database import inicio, registroC, registroP, registroS, getNd, getTd, getTipo, editC, hVisitas, hExamenes, getNitP, getNitS
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
                session['user'] = request.form['user']
                if tp == 1:
                    return redirect(url_for('main_civil'))
                if tp == 2:
                    return redirect(url_for('main_salud'))
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
        razon_ = request.form['razon']
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
            elif request.form["btn"] == "Código QR":
                return redirect(url_for('vista_qr'))
            elif request.form["btn"] == "Historial de visitas":
                return redirect(url_for('vista_historiales'))
            elif request.form["btn"] == "Resultados COVID-19":
                return redirect(url_for('vista_covid'))
            elif request.form["btn"] == "Contáctanos":
                return redirect(url_for('contacto'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_civil'))
    return render_template('main_civil2.html', usuario=usuario)

@app.route('/main_salud', methods=['GET','POST'])
def main_salud():
    usuario = None
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))
            #elif request.form["btn"] == "Contáctanos":
                #return redirect(url_for('contacto'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_salud'))
            elif request.form["btn"] == "Historial pruebas COVID-19":
                return redirect(url_for('vista_pruebas_covid'))
            elif request.form["btn"] == "Registro prueba COVID-19":
                return redirect(url_for('vista_registro_prueba_covid'))
    return render_template('main_salud.html', usuario=usuario)

@app.route('/qr', methods=['GET','POST'])
def vista_qr():
    usuario = session['user']
    ndu = getNd(usuario)
    qr = "QR_{0}.png".format(str(ndu))
    return render_template('vista_qr.html', usuario=usuario, qr=qr)

@app.route('/historiales', methods=['GET','POST'])
def vista_historiales():
    usuario = session['user']
    ndu = getNd(usuario)
    tdu = getTd(usuario)
    hist_completo = hVisitas(ndu, tdu)
    return render_template('vista_historiales.html', usuario=usuario, hist_completo=hist_completo)

@app.route('/pruebas_covid', methods=['GET','POST'])
def vista_covid():
    usuario = session['user']
    ndu = getNd(usuario)
    tdu = getTd(usuario)
    hist_completo = hExamenes(ndu, tdu)
    return render_template('vista_covid.html', usuario=usuario, hist_completo=hist_completo)

@app.route('/contacto_civil', methods=['GET','POST'])
def contacto():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Enviar":
                td_ = request.form['TD']
                nd_ = request.form['ND']
                nombres_ = request.form['nombres']
                apellidos_ = request.form['apellidos']
                email = request.form['correo']
                comentarios_ = request.form['comentarios']
                #que hacer con esta info?
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_civil'))
    return render_template('contacto_civil.html', usuario=usuario)

@app.route('/edit_perfil', methods=['GET','POST'])
def editar_perfil_civil():
    usuario = session['user']
    td = getTd(usuario)
    nd = getNd(usuario)
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Guardar":
                if len(request.form['nombres']) != 0: nombres_ = request.form['nombres']
                else: nombres_ = None
                if len(request.form['apellidos']) != 0: apellidos_ = request.form['apellidos']
                else: apellidos_ = None
                if request.form.get('genero') != None: genero_ = str(request.form.get('genero'))
                else: genero_ = None
                if len(request.form['T']) != 0: tel_ = int(request.form['T'])
                else: tel_ = None
                if len(request.form['fecha']) != 0: fecha_ = request.form['fecha']
                else: fecha_ = None
                if len(request.form['correo']) != 0: email = request.form['correo']
                else: email = None
                if request.form.get('departamento') != None: dept_ = str(request.form.get('departamento'))
                else: dept_ = None
                if request.form.get('municipio') != None: mun_ = str(request.form.get('municipio'))
                else: mun_ = None
                if request.form.get('barrio') != None: barrio_ = str(request.form.get('barrio'))
                else: barrio_ = None
                if len(request.form['direccion']) != 0: dir_ = request.form['direccion']
                else: dir_ = None
                if len(request.form['contraseña']) != 0: p = encriptar(request.form['contraseña'])
                else: p = None
                editC(usuario, p, int(nd), apellidos_, barrio_, email, dept_, dir_, mun_, fecha_, nombres_, genero_, td, tel_)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_civil'))
    return render_template('editar_perfil_civil.html', usuario=usuario)

@app.route('/edit_perfil_salud', methods=['GET','POST'])
def editar_perfil_salud():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Volver":
                return redirect(url_for('main_salud'))
    return render_template('editar_perfil_salud.html', usuario=usuario)

@app.route('/histo_covid', methods=['GET','POST'])
def vista_pruebas_covid():
    usuario = session['user']
    hist_completo = []
    return render_template('vista_historial_p_covid.html', usuario=usuario, hist_completo=hist_completo)

@app.route('/registro_p_covid', methods=['GET','POST'])
def vista_registro_prueba_covid():
    usuario = session['user']
    return render_template('vista_registro_p_covid.html', usuario=usuario)

if __name__ == "__main__":
    app.debug = True
    app.run()
