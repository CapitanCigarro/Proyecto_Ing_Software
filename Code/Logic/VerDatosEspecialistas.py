import json

class VerDatosEspecialistas:
    def __init__(self):
        # Abre y lee el archivo JSON
        with open('../../Data/datosEspecialistas.json', 'r') as file:
            data = json.load(file)
        # Muestra los datos con saltos de línea y formato
        self.imprimir_datos(data)

    def imprimir_datos(self, data):
        for item in data:
            print("Nombre:", item["nombre"])
            print("rut:", item["rut"])
            print("Especialidad:", item["especialidad"])
            print("\n")  # Salto de línea entre cada especialista

main = VerDatosEspecialistas()