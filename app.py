from flask import Flask
from flask import render_template, redirect, request, Response, session
#from flask_mysqldb import MySQL, MySQLdb
from Code.Logic.Especialista import Especialista
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(('menu_incial.html'))

@app.route('/contacto')
def contacto():
    with open('Data/datosCentroMedico.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template('informacionCentroMedico.html', data=data['institucion'])

@app.route('/agendar-cita', methods=['POST'])
def agendar_cita():
    especialidad = request.form['especialidad']
    fecha = request.form['fecha']

    especialistas = Especialista.get_especialistas(especialidad)
    return render_template('agendar_cita.html', especialistas=especialistas, especialidad=especialidad, fecha=fecha)  

@app.route('/confirmar-cita', methods=['GET', 'POST'])
def confirmar_cita():
    if request.method == 'POST':
        try:
            rut = request.form['rut']
            especialista = Especialista.get_especialista(rut)
            fecha = request.form['fecha']
            hora = request.form['hora']

            return render_template('confirmar_cita.html', especialidad=especialista.especialidad, fecha=fecha, hora=hora, especialista=especialista, nombre=especialista.nombre)

        except KeyError as e:
            print(f"Error: El campo {e} no se encuentra en el formulario")
            return "Error: Faltan campos en el formulario", 400

    return render_template('agendar_cita.html')

@app.route('/ver-horarios', methods=['GET'])
def ver_horarios():
    return render_template('horarios.html')

@app.route("/consulta-horarios", methods=["POST"])
def consultar_horarios():
    rut = request.form.get("rut")
    especialista = Especialista.get_especialista(rut)
    if especialista is None:
        return render_template("horarios.html", error="El RUT ingresado no es válido.", rut=rut, horarios=None) 
    horarios = especialista.get_disponibilidad()
    return render_template("horarios.html", horarios=horarios, rut=rut)

@app.route("/reagendar", methods=["GET", "POST"])
def reagendar():
    # Must be changed when db integration
    if request.method == "POST":
        with open('Data/datosCitasAgendadas.json', 'r', encoding='utf-8') as file:
            dates = json.load(file)
            try:
                id = request.form.get("id")
                date = dates[id]
                static = date["static"]
                stInfo = []
                variable = date["variable"]
                
                for key in static.keys():
                    stInfo.append(f"{key} : {static[key]}")
                
                variableInfo = []
                
                for key in variable:
                    variableInfo.append(variable[key])
                
                return render_template("reagendar_cita.html", static = stInfo, variable = variableInfo, id = id)
            except KeyError:
                return render_template("reagendar_cita.html", error="No existe cita con este id")
    else:
        return render_template("reagendar_cita.html")

#Function that actually changes the json file / database
@app.route("/reagendar/r", methods=["POST"])
def reag():
    for a in request.form:
        print(a)
    
    return render_template("reagendar_cita.html")

@app.route('/editar-horario', methods=['POST'])
def editar_horarios():
    rut = request.form['rut']
    especialista = Especialista.get_especialista(rut)
    horario_generico = []
    for i in range(8, 17):
        horario_generico.append(f"{i}:00")
        horario_generico.append(f"{i}:30") 
    if especialista is None:
        return render_template("horarios.html", error="El RUT ingresado no es válido.", rut=rut, horarios=None)
    return render_template('editar_horario.html', nombre=especialista.nombre, horario_generico=horario_generico, rut=rut)

@app.route('/confirmar-cambio-disponibilidad', methods=['POST'])
def confirmar_cambio_disponibilidad():
    rut = request.form['rut']
    horarios_generales = request.form.getlist('horarios_generales')
    fecha = request.form['fecha']
    horarios_especificos = request.form.getlist('horarios_especificos')
    
    especialista = Especialista.get_especialista(rut)
    cambio_exitoso = especialista.set_disponibilidad(horarios_generales, horarios_especificos, fecha)
    if cambio_exitoso:
        return render_template('confirmar_cambio_disponibilidad.html', nombre=especialista.nombre)
    return render_template('confirmar_cambio_disponibilidad.html', nombre=especialista.nombre, error="No se pudo realizar el cambio de disponibilidad")


@app.route('/lista-especialistas')
def lista_especialistas():
    return render_template('lista_especialistas.html')

if __name__ == '__main__':
    app.run(debug=True, port=1928)