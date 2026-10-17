from core.lexico import OPERADORES
PRECEDENCIA = {'|': 1, '+': 1, '.': 2}

def convertir_postfija(regex: str, alfabeto: set[str]) -> list[str]:
    regex = ''.join(regex.split())
    if not regex:
        raise ValueError('Ingrese una expresión regular.')
    invalidos = set(regex) - alfabeto - OPERADORES
    if invalidos:
        raise ValueError(f'Símbolos fuera del alfabeto o desconocidos: {sorted(invalidos)}')
    tokens: list[str] = []
    def fin_atomo(x): return x in alfabeto or x in {'ε', ')', '*'}
    def inicio_atomo(x): return x in alfabeto or x in {'ε', '('}
    for i, actual in enumerate(regex):
        if i and fin_atomo(regex[i-1]) and inicio_atomo(actual):
            tokens.append('.')
        tokens.append('|' if actual == '+' else actual)
    salida: list[str] = []
    pila: list[str] = []
    espera_atomo = True
    for token in tokens:
        if token in alfabeto or token == 'ε':
            if not espera_atomo: raise ValueError('Falta un operador.')
            salida.append(token); espera_atomo = False
        elif token == '(':
            if not espera_atomo: raise ValueError('Falta concatenación antes de (.')
            pila.append(token)
        elif token == ')':
            if espera_atomo: raise ValueError('Paréntesis vacío u operador sin operando.')
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            if not pila: raise ValueError('Paréntesis de cierre sin apertura.')
            pila.pop(); espera_atomo = False
        elif token == '*':
            if espera_atomo: raise ValueError("El operador * necesita un operando.")
            salida.append(token)
        elif token in PRECEDENCIA:
            if espera_atomo: raise ValueError('Operador binario sin operando izquierdo.')
            while pila and pila[-1] != '(' and PRECEDENCIA.get(pila[-1],0) >= PRECEDENCIA[token]:
                salida.append(pila.pop())
            pila.append(token); espera_atomo = True
        else:
            raise ValueError('Token no admitido: ' + token)
    if espera_atomo: raise ValueError('La expresión termina incompleta.')
    while pila:
        item = pila.pop()
        if item == '(': raise ValueError('Paréntesis sin cerrar.')
        salida.append(item)
    return salida
