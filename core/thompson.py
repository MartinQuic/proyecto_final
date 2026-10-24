"""INTEGRANTE 3. Construcción del AFN-ε mediante Thompson."""
from core.modelos import Automata, EPSILON

def construir_afn(postfija: list[str], alfabeto: set[str]) -> Automata:
    afn = Automata(alfabeto=set(alfabeto))
    pila: list[tuple[int,int]] = []
    contador = 0
    def nuevo():
        nonlocal contador
        n = contador; contador += 1; afn.estados.add(n); return n
    for token in postfija:
        if token in alfabeto or token == EPSILON:
            a,b=nuevo(),nuevo(); afn.agregar(a,token,b); pila.append((a,b))
        elif token == '*':
            if not pila: raise ValueError('Regex inválida: * sin operando.')
            a,b=pila.pop(); ini,fin=nuevo(),nuevo()
            for x,y in [(ini,a),(ini,fin),(b,a),(b,fin)]: afn.agregar(x,EPSILON,y)
            pila.append((ini,fin))
        elif token in {'.','|'}:
            if len(pila)<2: raise ValueError('Regex inválida: faltan operandos.')
            c,d=pila.pop(); a,b=pila.pop()
            if token=='.':
                afn.agregar(b,EPSILON,c); pila.append((a,d))
            else:
                ini,fin=nuevo(),nuevo()
                for x,y in [(ini,a),(ini,c),(b,fin),(d,fin)]: afn.agregar(x,EPSILON,y)
                pila.append((ini,fin))
        else: raise ValueError('Token inesperado: '+token)
    if len(pila)!=1: raise ValueError('Expresión regular incorrecta.')
    afn.inicial, fin = pila.pop(); afn.finales={fin}
    return afn
