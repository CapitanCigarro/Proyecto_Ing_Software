import datetime

class Horario:
    fecha : datetime.datetime
    hora : datetime.time
    disponibilidad : str
    
    def __init__(self, fecha : datetime.datetime, hora : datetime.time, disponibilidad : str) -> None:
        self.fecha = fecha
        self.hora = hora
        self.disponibilidad = disponibilidad
    