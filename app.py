from cassandra.cluster import Cluster
from flask import *
import requests, csv
from database import registroC, inicio

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
        u = request.form['user']
        p = request.form['pass']
        ans, tp = inicio(u, p)
        if ans:
            return render_template('main.html')
        else:
            flash("Usuario o contraseña incorrecta")

    return render_template('login.html')

@app.route('/main', methods=['GET','POST'])
def main():
    return render_template('main.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #Se obtienen los datos del formulario
        tipoS = request.form['tipoRegistro']
        tipo = None
        if tipoS == "C":
            tipo = 1
        elif tipoS == "EP":
            tipo = 2
        elif tipoS == "ES":
            tipo = 3
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

        if tipo == 1:
            registroC(u, p, int(numDoc), apellidos_, barrio_, email, dept, dire, mun, fecha_, nombres_, genero_, tipoDoc, int(tel))

        return render_template('login.html')

    return render_template('register.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
