from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb
from Code.Logic.Especialista import Especialista

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(('menu_incial.html'))

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
            
            # Procesar la cita como necesites (ej. guardarla o enviar por correo)
            return render_template('confirmar_cita.html', especialidad=especialista.especialidad, fecha=fecha, hora=hora, especialista=especialista, nombre=especialista.nombre)

        except KeyError as e:
            print(f"Error: El campo {e} no se encuentra en el formulario")
            return "Error: Faltan campos en el formulario", 400
        
    # Si es un GET, solo renderiza el formulario
    return render_template('agendar_cita.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=1928)