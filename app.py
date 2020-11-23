from cassandra.cluster import Cluster
from flask import *
import requests, csv
from database import registroC, inicio
from QR import makeQR, readQR

#Conectamos con la BD
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect("bdis")

#Configuramos la app de flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Funciones de cada vista
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form["b1"]=="Iniciar sesion":
            u = request.form['user']
            p = request.form['pass']
            ans, tp = inicio(u, p)
            if ans:
                return redirect(url_for('main'))
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
            pass
        elif select_tipo == "ES":
            pass
    return render_template('register_select.html')

@app.route('/register_civil', methods=['GET','POST'])
def register_civil():
    if request.method == 'POST':
        #Tipo 1 corresponde a civil
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
        p = request.form['password']
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

@app.route('/main', methods=['GET','POST'])
def main():
    return render_template('main.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
