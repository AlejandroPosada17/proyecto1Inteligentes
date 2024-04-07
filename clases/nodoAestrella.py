class Nodo:
    def __init__(self, x, y, padre=None, semaforo=None):
        self.x = x
        self.y = y
        self.padre = padre
        self.g = 0
        self.h = 0
        self.f = 0
        self.semaforo = semaforo
    
    #con esto indicamos como quieremos que se comparen los objetos nodos. En este caso se compararan con el atributo F
    def __lt__(self, otro):
        return self.f < otro.f