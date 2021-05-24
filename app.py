from cassandra.cluster import Cluster
from flask import *
import requests, csv, sys, os
from database import inicio, registroC, registroP, registroS, getNd, getTd, getTipo, editC, hVisitas, hExamenes, hExamenesS
from database import getNitP, getNitS, regVisita, hVisitasP, getCatRsol, editS, editP, getCorC, getCorP, getCorS, getPass
from database import fVisitasC, allVisitas, allExamenes, registroA, deleteU, regExam, getRsolS, editA, regVDestiempo, regResExam
from database import fExamenesC, fVisitasP, fExamenesS, getEdad, getEstrato, salidas_recientes
from download_files import download_csv, download_pdf
from QR import makeQR, readQR
from cryption import encriptar, decriptar
from correo import enviar_correo
from extra_functions import calcular_riesgo

#Configuramos la app de flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

#VISTA DE LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form["b1"]=="Iniciar sesion":
            u = request.form['user']
            p = encriptar(request.form['pass'])
            ans, tp = inicio(u, p)
            if ans:
                session['user'] = request.form['user']
                if tp == 0:
                    return redirect(url_for('main_admin'))
                if tp == 1:
                    return redirect(url_for('main_civil'))
                if tp == 2:
                    return redirect(url_for('main_salud'))
                if tp == 3:
                    return redirect(url_for('main_publico'))
            else:
                flash("Usuario o contraseña incorrecta")
        elif request.form["b1"]=="Registrarse":
            return redirect(url_for('register_select'))
        elif request.form["b1"]=="Recordar Contraseña":
            return redirect(url_for('recuperar_contra'))
    return render_template('login.html')

#VISTA SELECCIONAR TIPO DE REGISTRO
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

#VISTA REGISTRO DEL CIVIL
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
        ans = registroC(u, p, int(numDoc), apellidos_, barrio_, email, dept, dire, mun, fecha_, nombres_, genero_, tipoDoc, int(tel))
        if ans == True:
            data = {}
            data["Nombre"] = nombres_
            data["Apellido"] = apellidos_
            data["Tipo Documento"] = tipoDoc
            data["Numero Documento"] = numDoc
            #Se crea el codigo qr del civil
            makeQR(data)
        return redirect(url_for('login'))
    return render_template('register_civil.html')

#VISTA REGISTRO DE ENTIDAD PUBLICA
@app.route('/register_publico', methods=['GET','POST'])
def register_publico():
    if request.method == 'POST':
        nit_ = request.form['NIT']
        cat = str(request.form.get('categoria'))
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
        #Registro de la entidad publica en la base de datos
        registroP(u, int(nit_), barrio_, cat, email, dept_, dir_, mun_, p, razon_, tels)
        m = ""
        m += "La entidad publica identificada con el NIT " + nit_ + " se acaba de registrar en el sistema"
        enviar_correo("gerentebbgm@gmail.com", "Registro entidad publica", m)
        return redirect(url_for('login'))
    return render_template('register_publico.html')

#VISTA REGISTRO ENTIDAD DE SALUD
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
        m = ""
        m += "La entidad de salud identificada con el NIT " + nit_ + " se acaba de registrar en el sistema"
        enviar_correo("gerentebbgm@gmail.com", "Registro entidad de salud", m)
        return redirect(url_for('login'))
    return render_template('register_salud.html')

#VISTA MAIN ADMIN
@app.route('/main_admin', methods=['GET','POST'])
def main_admin():
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_admin'))
            elif request.form["btn"] == "Borrar Perfil":
                return redirect(url_for('borrar_perfil'))
            elif request.form["btn"] == "Historial Visitas":
                return redirect(url_for('hv_admin'))
            elif request.form["btn"] == "Historial Pruebas":
                return redirect(url_for('hc_admin'))
            elif request.form["btn"] == "Registrar Admin":
                return redirect(url_for('agregar_admin'))
    return render_template('main_admin.html', usuario=usuario)

#VISTA HISTORIALES VISITAS DE CIVILES (ADMIN)
@app.route('/hv_admin', methods=['GET','POST'])
def hv_admin():
    fields = ['Establecimiento Publico', 'Tipo Documento', 'Numero Documento', 'Fecha Entrada', 'Hora Entrada', 'Veredicto', 'Razón']
    usuario = session['user']
    hist_completo = allVisitas()
    if request.method == 'POST':
        if request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 1)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 1)
    return render_template('vista_adminHV.html', usuario=usuario, hist_completo=hist_completo)

#VISTA HISTORIALES PRUEBAS COVID-19 CIVILES (ADMIN)
@app.route('/hc_admin', methods=['GET','POST'])
def hc_admin():
    fields = fields = ['Establecimiento de Salud', 'Tipo Documento', 'Numero Documento', 'Fecha de Realización', 'Fecha Obtención Resultado', 'Resultado']
    usuario = session['user']
    hist_completo = allExamenes()
    if request.method == 'POST':
        if request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 2)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 2)
    return render_template('vista_adminHC.html', usuario=usuario, hist_completo=hist_completo)

#VISTA BORRAR PERFIL (ADMIN)
@app.route('/borrar_perfil', methods=['GET','POST'])
def borrar_perfil():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Eliminar":
            u = request.form['usuario']
            t = getTipo(u)
            if t == 1:
                ndu = getNd(u)
                scriptPath = sys.path[0]
                UPLOAD_PATH = os.path.join(scriptPath, 'static/images/')
                filename = "QR_{0}.png".format(ndu)
                os.remove('{0}{1}'.format(UPLOAD_PATH, filename))
            deleteU(u)
    return render_template('vista_borrarPerfil.html', usuario=usuario)

#VISTA AGREGAR ADMIN (ADMIN)
@app.route('/agregar_admin', methods=['GET','POST'])
def agregar_admin():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Agregar":
            nombres_ = request.form['nombres']
            apellidos_ = request.form['apellidos']
            u = request.form['usuario']
            registroA(u, encriptar("admin"), nombres_, apellidos_)
    return render_template('vista_agregar_admin.html', usuario=usuario)

#VISTA EDITAR PERFIL ADMIN
@app.route('/editar_perfil_admin', methods=['GET','POST'])
def editar_perfil_admin():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Guardar":
            if len(request.form['nombres']) != 0: nombres_ = request.form['nombres']
            else: nombres_ = None
            if len(request.form['apellidos']) != 0: apellidos_ = request.form['apellidos']
            else: apellidos_ = None
            if len(request.form['contraseña']) != 0: p = encriptar(request.form['contraseña'])
            else: p = None
            editA(usuario,p,nombres_,apellidos_)
        elif request.form["btn"] == "Volver":
            return redirect(url_for('main_admin'))
    return render_template('editar_perfil_admin.html', usuario=usuario)

#VISTA MAIN CIVIL
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
            elif request.form["btn"] == "Calcular Riesgo":
                return redirect(url_for('vista_riesgo'))
    return render_template('main_civil2.html', usuario=usuario)

#VISTA MAIN ENTIDAD DE SALUD
@app.route('/main_salud', methods=['GET','POST'])
def main_salud():
    usuario = None
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))
            elif request.form["btn"] == "Contáctanos":
                return redirect(url_for('contacto_salud'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_salud'))
            elif request.form["btn"] == "Historial pruebas COVID-19":
                return redirect(url_for('vista_pruebas_covid'))
            elif request.form["btn"] == "Registro prueba COVID-19":
                return redirect(url_for('vista_registro_prueba_covid'))
            elif request.form["btn"] == "Registro resultado prueba COVID-19":
                return redirect(url_for('reg_res_exam'))
    return render_template('main_salud.html', usuario=usuario)

#VISTA MAIN ENTIDAD PUBLICA
@app.route('/main_publico', methods=['GET','POST'])
def main_publico():
    usuario = None
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))
            elif request.form["btn"] == "Registro Asíncrono":
                return redirect(url_for('registro_falla'))
            elif request.form["btn"] == "Registro Visita":
                return redirect(url_for('registro_visita'))
            elif request.form["btn"] == "Historial de visitas":
                return redirect(url_for('vista_historiales_visitas'))
            elif request.form["btn"] == "Contáctanos":
                return redirect(url_for('contacto_publico'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_publico'))
    return render_template('main_publico.html', usuario=usuario)

#VISTA PARA CALCULAR RIESGO PARA CIVIL
@app.route('/riesgo', methods=['GET','POST'])
def vista_riesgo():
    usuario = session['user']
    mensaje_riesgo = ''
    if request.method == 'POST':
        if request.form["btn"] == "Calcular Riesgo":
            estrato = 6 #getEstrato(usuario)
            ndu = getNd(usuario)
            tdu = getTd(usuario)
            num_salidas_recientes = salidas_recientes(ndu, tdu)
            edad = getEdad(usuario)
            riesgo = calcular_riesgo(edad, estrato, num_salidas_recientes)
            mensaje_riesgo = "{0}, tu factor de riesgo de infección es: {1}".format(usuario, riesgo)
        elif request.form["btn"] == "Volver":
            return redirect(url_for('main_civil'))

    return render_template('vista_riesgo.html', usuario=usuario, mensaje_riesgo=mensaje_riesgo)

#VISTA DEL CODIGO QR PARA EL CIVIL
@app.route('/qr', methods=['GET','POST'])
def vista_qr():
    usuario = session['user']
    ndu = getNd(usuario)
    qr = "QR_{0}.png".format(str(ndu))
    return render_template('vista_qr.html', usuario=usuario, qr=qr)

#VISTA HISTORIALES DE VISITAS PARA EL CIVIL
@app.route('/historiales', methods=['GET','POST'])
def vista_historiales():
    fields = ['Establecimiento Publico', 'Categoria', 'Fecha Entrada', 'Hora Entrada', 'Veredicto', 'Razón']
    usuario = session['user']
    ndu = getNd(usuario)
    tdu = getTd(usuario)
    hist_completo = hVisitas(ndu, tdu)
    if request.method == 'POST':
        if request.form["btn"] == "Filtrar":
            if len(request.form['fi']) != 0: fi_ = request.form['fi']
            else: fi_ = None
            if len(request.form['ff']) != 0: ff_ = request.form['ff']
            else: ff_ = None
            if request.form.get('categoria') != None: cat_ = str(request.form.get('categoria'))
            else: cat_ = None
            nd_ = getNd(usuario)
            td_ = getTd(usuario)
            hist_completo = fVisitasC(nd_,td_,cat_,fi_,ff_)
        elif request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 1)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 1)
    return render_template('vista_historiales.html', usuario=usuario, hist_completo=hist_completo)

#VISTA HISTORIALES DE PRUEBAS COVID PARA CIVIL
@app.route('/pruebas_covid', methods=['GET','POST'])
def vista_covid():
    fields = ['Establecimiento de Salud', 'Fecha de Realización', 'Fecha Obtención Resultado', 'Resultado']
    usuario = session['user']
    ndu = getNd(usuario)
    tdu = getTd(usuario)
    hist_completo = hExamenes(ndu, tdu)
    if request.method == 'POST':
        if request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 2)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 2)
        elif request.form["btn"] == "Filtrar":
            if len(request.form['fi']) != 0: fi_ = request.form['fi']
            else: fi_ = None
            if len(request.form['ff']) != 0: ff_ = request.form['ff']
            else: ff_ = None
            if request.form.get('categoria') != None: cat_ = str(request.form.get('categoria'))
            else: cat_ = None
            nd_ = getNd(usuario)
            td_ = getTd(usuario)
            hist_completo = fExamenesC(nd_,td_,cat_,fi_,ff_)
    return render_template('vista_covid.html', usuario=usuario, hist_completo=hist_completo)

#VISTA CONTACTO PARA EL CIVIL
@app.route('/contacto_civil', methods=['GET','POST'])
def contacto():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Enviar":
                td_ = str(request.form.get('TD'))
                nd_ = request.form['ND']
                nombres_ = request.form['nombres']
                apellidos_ = request.form['apellidos']
                email = request.form['correo']
                comentarios_ = request.form['comentarios']
                m1 = ""
                m1 += nombres_ + " " + apellidos_ + " identificado con " + td_ + " " + nd_ + " te envio los siguientes comentarios " + comentarios_ + ". Responder al correo " + email
                enviar_correo("gerentebbgm@gmail.com", "Solicitud de contacto", m1)
                m2 = "Tus comentarios fueron enviados con exito. Pronto te responderemos."
                enviar_correo(email, "Envio Solicitud de Contacto", m2)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_civil'))
    return render_template('contacto_civil.html', usuario=usuario)

#VISTA CONTACTO PARA ENTIDAD PUBLICA
@app.route('/contacto_publico', methods=['GET','POST'])
def contacto_publico():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Enviar":
                nit_ = request.form['NIT']
                email = request.form['correo']
                comentarios_ = request.form['comentarios']
                m1 = ""
                m1 += "La entidad publica identificada con el NIT " + nit_ + " te envio los siguientes comentarios " + comentarios_ + ". Responder al correo " + email
                enviar_correo("gerentebbgm@gmail.com", "Solicitud de contacto", m1)
                m2 = "Tus comentarios fueron enviados con exito. Pronto te responderemos."
                enviar_correo(email, "Envio Solicitud de Contacto", m2)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_publico'))
    return render_template('contacto_publica.html', usuario=usuario)

#VISTA CONTACTO PARA ENTIDAD DE SALUD
@app.route('/contacto_salud', methods=['GET','POST'])
def contacto_salud():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Enviar":
                nit_ = request.form['NIT']
                email = request.form['correo']
                comentarios_ = request.form['comentarios']
                m1 = ""
                m1 += "La entidad de salud identificada con el NIT " + nit_ + " te envio los siguientes comentarios " + comentarios_ + ". Responder al correo " + email
                enviar_correo("gerentebbgm@gmail.com", "Solicitud de contacto", m1)
                m2 = "Tus comentarios fueron enviados con exito. Pronto te responderemos."
                enviar_correo(email, "Envio Solicitud de Contacto", m2)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_salud'))
    return render_template('contacto_salud.html', usuario=usuario)

#VISTA EDITAR PERFIL PARA EL CIVIL
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

#VISTA EDITAR PERFIL PARA ENTIDAD PUBLICA
@app.route('/edit_perfil_publico', methods=['GET','POST'])
def editar_perfil_publico():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Guardar":
                if len(request.form['razon']) != 0: razon_ = request.form['razon']
                else: razon_ = None
                if len(request.form['T1']) != 0: tel1_ = int(request.form['T1'])
                else: tel1_ = None
                if len(request.form['T2']) != 0: tel2_ = int(request.form['T2'])
                else: tel2_ = None
                if len(request.form['T3']) != 0: tel3_ = int(request.form['T3'])
                else: tel3_ = None
                if request.form.get('departamento') != None: dept_ = str(request.form.get('departamento'))
                else: dept_ = None
                if request.form.get('municipio') != None: mun_ = str(request.form.get('municipio'))
                else: mun_ = None
                if request.form.get('barrio') != None: barrio_ = str(request.form.get('barrio'))
                else: barrio_ = None
                nit_ = getNitP(usuario)
                editP(usuario, nit_, barrio_, None, dept_, None, mun_, None, razon_, tel1_, tel2_, tel3_)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_publico'))
    return render_template('editar_perfil_publico.html', usuario=usuario)

#VISTA EDITAR PERFIL PARA ENTIDAD DE SALUD
@app.route('/edit_perfil_salud', methods=['GET','POST'])
def editar_perfil_salud():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Guardar":
                if len(request.form['razon']) != 0: razon_ = request.form['razon']
                else: razon_ = None
                if len(request.form['T1']) != 0: tel1_ = int(request.form['T1'])
                else: tel1_ = None
                if len(request.form['T2']) != 0: tel2_ = int(request.form['T2'])
                else: tel2_ = None
                if len(request.form['T3']) != 0: tel3_ = int(request.form['T3'])
                else: tel3_ = None
                if request.form.get('departamento') != None: dept_ = str(request.form.get('departamento'))
                else: dept_ = None
                if request.form.get('municipio') != None: mun_ = str(request.form.get('municipio'))
                else: mun_ = None
                if request.form.get('barrio') != None: barrio_ = str(request.form.get('barrio'))
                else: barrio_ = None
                nit_ = getNitS(usuario)
                editS(usuario, nit_, barrio_, None, dept_, None, mun_, None, razon_, tel1_, tel2_, tel3_)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_salud'))
    return render_template('editar_perfil_salud.html', usuario=usuario)

#VISTA HISTORIALES PRUEBAS COVID ENTIDAD DE SALUD
@app.route('/histo_covid', methods=['GET','POST'])
def vista_pruebas_covid():
    fields = ["Persona", "Fecha de Realización", "Fecha Resultado", "Resultado"]
    usuario = session['user']
    nitus = getNitS(usuario)
    hist_completo = hExamenesS(nitus)
    if request.method == 'POST':
        if request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 2)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 2)
        elif request.form["btn"] == "Filtrar":
            if len(request.form['fi']) != 0: fi_ = request.form['fi']
            else: fi_ = None
            if len(request.form['ff']) != 0: ff_ = request.form['ff']
            else: ff_ = None
            if request.form.get('categoria') != None: cat_ = str(request.form.get('categoria'))
            else: cat_ = None
            nit_ = getNitS(usuario)
            hist_completo = fExamenesS(nit_, cat_, fi_, ff_)
    return render_template('vista_historial_p_covid.html', usuario=usuario, hist_completo=hist_completo)

#VISTA REGISTRO PRUEBA COVID ENTIDAD DE SALUD
@app.route('/registro_p_covid', methods=['GET','POST'])
def vista_registro_prueba_covid():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Registrar Examen":
            td_ = str(request.form.get('TD'))
            nd_ = request.form['ND']
            nit_ = getNitS(usuario)
            rsol = getRsolS(usuario)
            regExam(nit_,td_,nd_,rsol)
    return render_template('vista_registro_p_covid.html', usuario=usuario)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#VISTA REGISTRO VISITA CON QR PARA ENTIDAD PUBLICA
@app.route('/registro_visita', methods=['GET','POST'])
def registro_visita():
    scriptPath = sys.path[0]
    UPLOAD_PATH = os.path.join(scriptPath, 'static/images/uploads/')
    usuario = session['user']
    data =  None
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Registrar":
                tapabocas_ = str(request.form.get('tapabocas'))
                temperatura = request.form['temp']
                filename = None
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = file.filename
                    file.save('{0}{1}'.format(UPLOAD_PATH, filename))
                    data = readQR(filename)
                nitus = getNitP(usuario)
                rsol, cat = getCatRsol(usuario)
                tap = None
                if tapabocas_ == "Si": tap = True
                else: tap = False
                regVisita(nitus, int(data[3]), data[2], data[0], data[1], int(temperatura), tap, rsol, cat)
                os.remove('{0}{1}'.format(UPLOAD_PATH, filename))
                return redirect(url_for('registro_visita'))
    return render_template('vista_registro_visita.html', usuario=usuario)

#VISTA REGISTRO VISITA POST FALLA ENTIDAD PUBLICA
@app.route('/registro_falla', methods=['GET','POST'])
def registro_falla():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Registrar":
            nombres_ = request.form['nombres']
            apellidos_ = request.form['apellidos']
            td_ = str(request.form.get('TD'))
            nd_ = request.form['ND']
            temp_ = request.form['temp']
            if str(request.form.get('tapabocas')) == "Si": tap_= True
            else: tap_ = False
            fecha_ = request.form['fecha']
            hora_ = request.form['hora']
            nit_ = getNitP(usuario)
            rsol, cat = getCatRsol(usuario)
            regVDestiempo(nit_,int(nd_),td_,nombres_,apellidos_,int(temp_),tap_,rsol,cat,fecha_,hora_)
    return render_template('vista_registro_visita_NE.html', usuario=usuario)

#VISTA HISTORIALES DE VISITA ENTIDAD PUBLICA
@app.route('/historiales_visitas', methods=['GET','POST'])
def vista_historiales_visitas():
    fields = ["Tipo Documento", "Numero Documento", "Fecha Entrada", "Hora Entrada", "Veredicto", "Razón"]
    usuario = session['user']
    nitus = getNitP(usuario)
    hist_completo = hVisitasP(nitus)
    if request.method == 'POST':
        if request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 1)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 1)
        elif request.form["btn"] == "Filtrar":
            if len(request.form['fi']) != 0: fi_ = request.form['fi']
            else: fi_ = None
            if len(request.form['ff']) != 0: ff_ = request.form['ff']
            else: ff_ = None
            if request.form.get('categoria') != None: cat_ = str(request.form.get('categoria'))
            else: cat_ = None
            if cat_ == "Denegado": c = False
            else: c = True
            nit_ = getNitP(usuario)
            hist_completo = fVisitasP(nit_, c, fi_, ff_)
    return render_template('vista_historial_visitas.html', usuario=usuario, hist_completo=hist_completo)

#VISTA REGISTRO RESULTADO PRUEBA COVID
@app.route('/reg_res_exam', methods=['GET','POST'])
def reg_res_exam():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Registrar":
            td_ = str(request.form.get('TD'))
            nd_ = request.form['ND']
            id_examen = request.form['idExamen']
            res = str(request.form.get('resultado'))
            nit_ = getNitS(usuario)
            regResExam(int(id_examen),nit_,int(nd_),res,td_)
    return render_template('vista_registroRes.html', usuario=usuario)

#VISTA RECUPERAR CONTRASEÑA
@app.route('/recuperar', methods=['GET','POST'])
def recuperar_contra():
    mensaje = ""
    if request.method == 'POST':
        if request.form["btn"] == "Recuperar":
            usr = request.form['usuario']
            email = request.form['correo']
            usr_email = None
            t = getTipo(usr)
            if t == 1: usr_email = getCorC(usr)
            elif t == 2: usr_email = getCorS(usr)
            elif t == 3: usr_email = getCorP(usr)
            if usr_email == email:
                p = getPass(usr)
                m = "Tu contrasena es {0}".format(decriptar(p))
                enviar_correo(usr_email, "Recuperacion contrasena", m)
                mensaje = "Tu contrasena ha sido enviada a tu correo"
            else:
                mensaje = "El correo que ingresaste no esta asociado al usuario ingresado"
    return render_template('recuperar_contrasena.html', mensaje=mensaje)

if __name__ == "__main__":
    app.debug = True
    app.run()
