class Reporte:
    def __init__(self, costo, carreras, calles, duracion):
        self.costo = costo
        self.carreras = carreras
        self.calles = calles
        self.duracion = duracion


    def getReporte(self):
        print(f"Costo total: {self.costo}")
        print(f"Cantidad de calles: {self.calles}")
        print(f"Cantidad de carreras: {self.carreras}")
        print(f"Tiempo del servicio: {self.duracion}")
