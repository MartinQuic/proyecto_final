class ShuntingYard:
    def __init__(self):
        pass

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
                while (pila and pila[-1] != '(' and
                       self.obtener_precedencia(pila[-1]) >= self.obtener_precedencia(simbolo)):
                    salida.append(pila.pop())
                pila.append(simbolo)

        while pila:
            salida.append(pila.pop())

        return "".join(salida)

    # if __name__ == "__main__":
    # sy = ShuntingYard()
    # expresion = "(a|b)·c*"
    # resultado = sy.infix_a_postfix(expresion)
    # print(f"Infix: {expresion}")
    # print(f"Postfix: {resultado}")
