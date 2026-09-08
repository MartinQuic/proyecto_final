class ShuntingYard:
    def __init__(self):
        self.operador = set()

    def obtener_precedencia(self, operador):
        if operador == '*':
            return 3
        elif operador == '·':
            return 2
        elif operador == '|':
            return 1
        return 0

    def infix_a_postfix(self, expresion):
        salida = []
        pila = []

        for simbolo in expresion:
            if simbolo.isalnum():
                salida.append(simbolo)
            elif simbolo == '(':
                pila.append(simbolo)
            elif simbolo == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                    if pila and pila[-1] == '(':
                        pila.pop()
            else:
                w           
                