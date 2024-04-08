class Vehiculo:
    def __init__(self, id, eficiencia_combustible):
        self.id = id
        self.eficiencia_combustible = eficiencia_combustible
        self.costo_total = 0
        self.cantidad_calles = 0
        self.cantidad_carreras = 0
        self.duracion_servicio = 0
        self.reportes = []


    def reportar_viaje(self, costo, Cantcalles, Cantcarreras, tiempo):
        self.costo_total += costo
        self.cantidad_calles += Cantcalles
        self.cantidad_carreras += Cantcarreras        
        self.duracion_servicio += tiempo

    def generar_reporte(self, rutas):

        if not rutas: 
            print(f"Reporte del vehículo {self.id}:")
            print(f"Costo total: {self.costo_total}")
            print(f"Cantidad de calles: {self.cantidad_calles}")
            print(f"Cantidad de carreras: {self.cantidad_carreras}")
            print(f"Tiempo del servicio: {self.duracion_servicio}")

        else:
            print(f"Reporte del vehículo {self.id}:")
            print(f"Costo total: {self.costo_total}")
            print(f"Cantidad de calles: {self.cantidad_calles}")
            print(f"Cantidad de carreras: {self.cantidad_carreras}")
            print(f"Tiempo del servicio: {self.duracion_servicio}")
            
            print("Comparación de rutas:")
            for ruta in rutas:
                costo_ruta = ruta.distancia_total / self.eficiencia_combustible
                print(f"Ruta {ruta.id}: Costo: {costo_ruta}")

        print("Fin del reporte.")
