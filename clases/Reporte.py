class Reporte:
    def __init__(self, costoServicio, costoCombustible, carreras, calles, duracion):
        self.costoServicio = costoServicio
        self.costoCombustible = costoCombustible
        self.carreras = carreras
        self.calles = calles
        self.duracion = duracion


    def getReporte(self):
        print(f"Costo del servicio: {self.costoServicio}")
        print(f"Costo de combustible: {self.costoCombustible}")
        print(f"Cantidad de calles: {self.calles}")
        print(f"Cantidad de carreras: {self.carreras}")
        print(f"Tiempo del servicio: {self.duracion}")
