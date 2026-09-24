class estado:
    def __init__(self, id_estado):
        self.id_estado = id_estado
        self.transiciones = {}
        self.es_final = False

class AFN:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

class algoritmo_thompson:
    def __init__(self): 
        self.contador_estados = 0

    def nuevo_estado(self):
        estado = estado(self.contador_estados)
        self.contador_estados +=1
        return estado

    def crear_afn_basico(self, simbolo):
        inicio = self.nuevo_estado()
        fin = self.nuevo_estado()
        inicio.transiciones[simbolo]=[fin]
        fin.es_final = True

        return AFN(inicio, fin)