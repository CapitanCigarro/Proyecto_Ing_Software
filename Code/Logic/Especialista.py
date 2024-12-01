import json
import os 

class Especialista:
    nombre : str
    especialidad : str
    
    def __init__(self, nombre : str, rut, especialidad, fecha=None) -> None:
        self.nombre = nombre
        self.rut = rut
        self.especialidad = especialidad
        self.horas = self.get_disponibilidad(fecha)
            
    @staticmethod        
    def get_especialista(rut):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'datosEspecialistas.json')
        with open(file_path) as file:
            especialistas = json.load(file)
        for especialista in especialistas:
            if especialista['rut'] == rut:
                return Especialista(especialista['nombre'], rut, especialista['especialidad'])
        return None
            
    @staticmethod
    def get_especialistas(especialidad, fecha=None):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'datosEspecialistas.json')
        with open(file_path) as file:
            data = json.load(file)
            
        especialistas = []
        for especialista in data:
            if especialista['especialidad'] == especialidad:
                especialistas.append(Especialista(especialista['nombre'], especialista['rut'], especialista['especialidad'], fecha))
        return especialistas
        
    def get_disponibilidad(self, fecha=None):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'datosHorasDisponibles.json')
        with open(file_path) as file:
            data = json.load(file)
        if not fecha:
            for hora in data:
                if hora['rut'] == str(self.rut):
                    horario = [hora['horas'],hora['fechas_especificas']]
                    return horario
        for hora in data:
            if hora['rut'] == str(self.rut):
                if fecha:
                    if fecha in hora['fechas_especificas']:
                        return hora['fechas_especificas'][fecha]
                return hora['horas']
        return []

    def set_disponibilidad(self, horario_general, horario_especifico, fecha, mantener_horarios=True):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'datosHorasDisponibles.json')
        with open(file_path) as file:
            data = json.load(file)
        
        if not mantener_horarios:
            nuevas_horas = []
            for hora in horario_general:
                nuevas_horas.append(str(hora))
            self.horas = nuevas_horas
        else:
            nuevas_horas = self.horas
            
        try:
            for hora in data:
                if hora['rut'] == str(self.rut):
                    hora['horas'] = nuevas_horas[0]
                    if horario_especifico:
                        hora['fechas_especificas'].update({fecha: horario_especifico})
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except:
            return False
        
    def get_citas(self, fecha_especifica=None):
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'datosCitasAgendadas.json')
        with open(file_path) as file:
            data = json.load(file)
        citas = []
        for cita in data:
            if cita['static']['Rut_doctor'] == self.rut:
                if not fecha_especifica:
                    citas.append(
                        {
                            "id_cita": cita['static']['id'], 
                            "nombre_paciente": cita['static']['Paciente'], 
                            "Comentarios": cita['variable']['Comentarios'], 
                            "fecha": cita['variable']['Fecha'], 
                            "hora": cita['variable']['Hora']
                        }
                    )
                elif cita['Fecha'] == fecha_especifica:
                    citas.append(
                        {
                            "id_cita": cita['static']['id'], 
                            "nombre_paciente": cita['static']['Paciente'], 
                            "Comentarios": cita['variable']['Comentarios'], 
                            "fecha": cita['variable']['Fecha'], 
                            "hora": cita['variable']['Hora']
                        }
                    )        
        return citas
        
