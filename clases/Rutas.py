import heapq
from collections import deque
from clases.nodoAestrella import Nodo
from clases.Vehiculo import Vehiculo
from clases.Reporte import Reporte


class Rutas:

    movimientos = [(-1,0),(1,0),(0,-1),(0,1)] # arriba - abajo - izquierda - derecha
    interaccion_adyacencia = {1: 0, 0: 1, 2: 3, 3: 2}

    def __init__(self, L, inicio, final, vehiculo:Vehiculo):
        self.L = L
        self.inicio = inicio
        self.final = final
        self.vehiculo = vehiculo
        self.id = f"Ruta {self.vehiculo.id}"
        self.distancia = 0
    
    def movimientos_posibles(self,nodo):
        candidatos = []
        for m in self.movimientos:
            candidatos.append((nodo.x+m[0],nodo.y+m[1]))
        return candidatos
        
    def heuristica(self, nodo:Nodo, destino:Nodo):         

        
    
        return abs(nodo.x - destino.x) + abs(nodo.y - destino.y)

    def es_valido(self, x,y):
        return 0 <= x < len(self.L) and 0 <= y < len(self.L[0])

    def es_viable(self,x,y):
        return self.L[x][y][0] == 0

    def astar(self, semaforizacion):

        calles=0
        carreras=0
        
        lst_abiertos = []
        lst_cerrados = set()
        #Se crea con clase nodo, el nodo inicio y nodo final
        nodo_inicio = Nodo(self.inicio[0], self.inicio[1]) 
        nodo_destino = Nodo(self.final[0], self.final[1])

        #Agregamos al heapq(lst_abiertos) el nodo nodo_inicio
        heapq.heappush(lst_abiertos, nodo_inicio)
        
        while lst_abiertos:

            #busca monticulo minimo y lo elimina. Luego agrega su posicion a lst_cerrados
            nodo_actual = heapq.heappop(lst_abiertos)
            lst_cerrados.add((nodo_actual.x, nodo_actual.y))
            
            if nodo_actual.x == nodo_destino.x and nodo_actual.y == nodo_destino.y:
                camino = []
                while nodo_actual:
                    camino.append((nodo_actual.x, nodo_actual.y))
                    nodo_actual = nodo_actual.padre

                
                ruta = camino[::-1]

                carreras, calles = self.sumar_carreras_calles(ruta)

                self.distancia = len(ruta) - 1
                cantidad_calles = calles
                cantidad_carreras = carreras
                tiempo = sum(self.L[x][y][1] for x, y in ruta if self.L[x][y][1]) + self.distancia
                reporte = Reporte(self.vehiculo.costo_total * tiempo,self.distancia/self.vehiculo.eficiencia_combustible,cantidad_carreras,cantidad_calles,tiempo)
                self.vehiculo.reportes.append(reporte)

                #print("Reporte acumulado")
                #self.vehiculo.reportar_viaje(self.distancia / self.vehiculo.eficiencia_combustible, cantidad_calles, cantidad_carreras, tiempo)
                    
                return camino[::-1]
            
            candidatos = self.movimientos_posibles(nodo_actual)

            direccion_posible_movimiento = 0; #empieza hacia arriba
            for c in candidatos:
                
                #Si nodo actual puede salir en "direccion_posible_movimiento"
                if self.L[nodo_actual.x][nodo_actual.y][3][direccion_posible_movimiento] in ["dobleVia", "sale"]:
                    
                    adyacencias_nodo_candidato = self.interaccion_adyacencia.get(direccion_posible_movimiento)
                    x, y = c

                    #Si al nodo candidato se puede entrar por "adyacencias_nodo_candidato"
                    if self.L[x][y][3][adyacencias_nodo_candidato] in ["dobleVia", "entra"]:

                        if self.es_valido(x,y) and self.es_viable(x,y) and (x, y) not in lst_cerrados:

                            if semaforizacion:
                                valor_semaforo = 0
                                if self.L[x][y][1] == False:
                                    valor_semaforo = 0
                                else:
                                    valor_semaforo = self.L[x][y][1]

                                # Modificar el cálculo del costo del movimiento para incluir el costo del semáforo
                                costo_movimiento = nodo_actual.g + 1 + valor_semaforo  # 1 es el costo base del movimiento
                                nodo_candidato = Nodo(x, y, nodo_actual, valor_semaforo)  # Pasar el costo del semáforo como parámetro
                                nodo_candidato.g = costo_movimiento
                            else:
                                nodo_candidato = Nodo(x, y, nodo_actual)
                                nodo_candidato.g = nodo_actual.g + 1

                            #Distancia a destino sin ir diagonalmente
                            nodo_candidato.h = self.heuristica(nodo_candidato, nodo_destino)
                            nodo_candidato.f = nodo_candidato.g + nodo_candidato.h
                            heapq.heappush(lst_abiertos, nodo_candidato)
                            lst_cerrados.add((x, y))

                direccion_posible_movimiento += 1 
        
        return None


    def ruta_menor_consumo(self):
        lst_abiertos = []
        lst_cerrados = set()
        nodo_inicio = Nodo(self.inicio[0], self.inicio[1])
        nodo_destino = Nodo(self.final[0], self.final[1])

        heapq.heappush(lst_abiertos, nodo_inicio)

        while lst_abiertos:
            nodo_actual = heapq.heappop(lst_abiertos)
            lst_cerrados.add((nodo_actual.x, nodo_actual.y))

            if nodo_actual.x == nodo_destino.x and nodo_actual.y == nodo_destino.y:
                camino = []
                while nodo_actual:
                    camino.append((nodo_actual.x, nodo_actual.y))
                    nodo_actual = nodo_actual.padre

                ruta = camino[::-1]

                carreras, calles = self.sumar_carreras_calles(ruta)
                self.distancia = len(ruta) -1
                cantidad_calles = calles
                cantidad_carreras = carreras
                tiempo = sum(self.L[x][y][1] for x, y in ruta if self.L[x][y][1]) + self.distancia

                #Reporte
                reporte = Reporte(self.vehiculo.costo_total * (tiempo),self.distancia/self.vehiculo.eficiencia_combustible,cantidad_carreras,cantidad_calles,tiempo)
                self.vehiculo.reportes.append(reporte)
                self.todas_rutas_posibles()
                #self.vehiculo.reportar_viaje(self.distancia / self.vehiculo.eficiencia_combustible, cantidad_calles, cantidad_carreras, tiempo)
                return ruta

            candidatos = self.movimientos_posibles(nodo_actual)

            direccion_posible_movimiento = 0
            for c in candidatos:
                if self.L[nodo_actual.x][nodo_actual.y][3][direccion_posible_movimiento] in ["dobleVia", "sale"]:
                    adyacencias_nodo_candidato = self.interaccion_adyacencia.get(direccion_posible_movimiento)
                    x, y = c

                    if self.L[x][y][3][adyacencias_nodo_candidato] in ["dobleVia", "entra"]:
                        if self.es_valido(x, y) and self.es_viable(x, y) and (x, y) not in lst_cerrados:

                          
                            

                            # Modificar el cálculo del costo del movimiento para incluir el costo del semáforo
                            costo_movimiento = nodo_actual.g + 1   # 1 es el costo base del movimiento
                            nodo_candidato = Nodo(x, y, nodo_actual, 0)  # Pasar el costo del semáforo como parámetro
                            nodo_candidato.g = costo_movimiento
                         

                            nodo_candidato.h = self.heuristica(nodo_candidato, nodo_destino)
                            nodo_candidato.f = nodo_candidato.g + nodo_candidato.h
                            heapq.heappush(lst_abiertos, nodo_candidato)
                            lst_cerrados.add((x, y))

                direccion_posible_movimiento += 1

        return None
    
    def todas_rutas_posibles(self):
        rutas = []
        longitud_maxima = len(self.L) + len(self.L[0])  # Longitud máxima razonable
        self.backtrack(self.inicio, [self.inicio], rutas, longitud_maxima)
        for i, ruta in enumerate(rutas, start=1):
                print(f"Ruta {i} {ruta}: Distancia: {len(ruta)}, Costo de combustible: {len(ruta)/self.vehiculo.eficiencia_combustible}")
        return rutas

    def backtrack(self, nodo, ruta_actual, rutas, longitud_maxima):
        x, y = nodo

        if nodo == self.final:
            rutas.append(ruta_actual[:])
            return

        if len(ruta_actual) >= longitud_maxima:
            return  # Poda: No explorar rutas demasiado largas

        candidatos = self.movimientos_posibles(Nodo(x, y))
        for c in candidatos:
            cx, cy = c
            if self.es_valido(cx, cy) and self.es_viable(cx, cy):
                direccion_actual = self.obtener_direccion(nodo, (cx, cy))
                if direccion_actual is not None:
                    adyacencias_nodo_actual = self.L[x][y][3][direccion_actual]
                    adyacencias_nodo_candidato = self.interaccion_adyacencia.get(direccion_actual)
                    if (adyacencias_nodo_actual in ["dobleVia", "sale"] and
                        self.L[cx][cy][3][adyacencias_nodo_candidato] in ["dobleVia", "entra"]):
                        nueva_ruta = ruta_actual + [(cx, cy)]
                        self.backtrack((cx, cy), nueva_ruta, rutas, longitud_maxima)

    def obtener_direccion(self, nodo_actual, nodo_siguiente):
        x1, y1 = nodo_actual
        x2, y2 = nodo_siguiente
        dx, dy = x2 - x1, y2 - y1
        if dx == -1 and dy == 0:
            return 0  # Arriba
        elif dx == 1 and dy == 0:
            return 1  # Abajo
        elif dx == 0 and dy == -1:
            return 2  # Izquierda
        elif dx == 0 and dy == 1:
            return 3  # Derecha
        return None
    

    def sumar_carreras_calles(self,camino):
        cambios_x = 0
        cambios_y = 0

        for i in range(len(camino) - 1):
            x1, y1 = camino[i]
            x2, y2 = camino[i + 1]
            cambios_x += abs(x2 - x1)
            cambios_y += abs(y2 - y1)

        return cambios_x, cambios_y


