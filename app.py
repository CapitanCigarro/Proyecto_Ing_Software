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
        # Obtener los detalles enviados por el formulario
        especialidad = request.form['especialidad']
        fecha = request.form['fecha']
        hora = request.form['hora']
        especialista = request.form['especialista']
        nombre = request.form['nombre']
        
        # Aquí procesas la cita, como guardarla o enviarla por correo, etc.
        # Luego, rediriges a una página de éxito o lo que prefieras.
        return render_template('confirmar_cita.html', especialidad=especialidad, fecha=fecha, hora=hora, especialista=especialista, nombre=nombre)

    # Si es un GET, solo renderiza el formulario
    return render_template('agendar_cita.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=1928)