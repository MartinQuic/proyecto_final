class Estado:
    def __init__(self, id_estado):
        self.id_estado = id_estado
        self.transiciones = {}
        self.es_final = False

class AFN:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

class Algoritmo_Thompson:
    def __init__(self): 
        self.contador_estados = 0

    def nuevo_estado(self):
        estado = Estado(self.contador_estados)
        self.contador_estados +=1
        return estado

    def crear_afn_basico(self, simbolo):
        inicio = self.nuevo_estado()
        fin = self.nuevo_estado()
        inicio.transiciones[simbolo]=[fin]
        fin.es_final = True
        return AFN(inicio, fin)

    def concatenar(self, afn1, afn2):
        afn1.estado_final.es_final = False
        
        # Conectamos la salida de afn1 con la entrada de afn2 mediante ε
        if 'ε' not in afn1.estado_final.transiciones:
            afn1.estado_final.transiciones['ε'] = []
        afn1.estado_final.transiciones['ε'].append(afn2.estado_inicial)
        
        return AFN(afn1.estado_inicial, afn2.estado_final)

    def unir(self, afn1, afn2):
        inicio = self.nuevo_estado()
        fin = self.nuevo_estado()
        
        afn1.estado_final.es_final = False
        afn2.estado_final.es_final = False
        
        # Ramas paralelas con transiciones ε
        inicio.transiciones['ε'] = [afn1.estado_inicial, afn2.estado_inicial]
        
        if 'ε' not in afn1.estado_final.transiciones:
            afn1.estado_final.transiciones['ε'] = []
        afn1.estado_final.transiciones['ε'].append(fin)
        
        if 'ε' not in afn2.estado_final.transiciones:
            afn2.estado_final.transiciones['ε'] = []
        afn2.estado_final.transiciones['ε'].append(fin)
        
        fin.es_final = True
        return AFN(inicio, fin)

    def kleene(self, afn):
        inicio = self.nuevo_estado()
        fin = self.nuevo_estado()
        
        afn.estado_final.es_final = False
        
        # Salto de inicio a fin (cadena vacía) y entrada al AFN
        inicio.transiciones['ε'] = [afn.estado_inicial, fin]
        
        # Bucle de retorno ε y salida hacia el estado final
        if 'ε' not in afn.estado_final.transiciones:
            afn.estado_final.transiciones['ε'] = []
        afn.estado_final.transiciones['ε'].append(afn.estado_inicial)
        afn.estado_final.transiciones['ε'].append(fin)
        
        fin.es_final = True
        return AFN(inicio, fin)

    def postfix_a_afn(self, expresion_postfix):
        pila_afn = []

        for simbolo in expresion_postfix:
            if simbolo == '·':
                afn2 = pila_afn.pop()
                afn1 = pila_afn.pop()
                pila_afn.append(self.concatenar(afn1, afn2))
            elif simbolo == '|':
                afn2 = pila_afn.pop()
                afn1 = pila_afn.pop()
                pila_afn.append(self.unir(afn1, afn2))
            elif simbolo == '*':
                afn = pila_afn.pop()
                pila_afn.append(self.kleene(afn))
            else:
                # Es un operando (letra, token o número)
                pila_afn.append(self.crear_afn_basico(simbolo))

        return pila_afn.pop()


# if __name__ == "__main__":
#     thompson = Algoritmo_Thompson() # Instancia con mayúscula
#     expresion_postfix = "ab|c*·" 
#     afn_resultante = thompson.postfix_a_afn(expresion_postfix)
    
#     print(f"AFN Creado con éxito.")
#     print(f"Estado Inicial: S{afn_resultante.estado_inicial.id_estado}")
#     print(f"Estado Final: S{afn_resultante.estado_final.id_estado}")
#     print(f"Total de estados generados: {thompson.contador_estados}")