LETRAS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
NUMEROS = set("0123456789")
SIMBOLOS = set(",;()*=_ .<>=\n\r\t")

ALFABETO = LETRAS.union(NUMEROS).union(SIMBOLOS)

PALABRAS_RESERVADAS = {
    "SELECT", "FROM", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "ASC", "DESC",
    "JOIN", "INNER", "LEFT", "RIGHT", "ON", "AND", "OR"
}

class Token:
    def __init__(self, tipo: str, valor: str, posicion: int):
        self.tipo = tipo      # 'RESERVADA', 'IDENTIFICADOR', 'NUMERO', 'SIMBOLO', 'OPERADOR', 'PUNTO_Y_COMA'
        self.valor = valor    # Ej: 'SELECT', 'e.nombre', '*'
        self.posicion = posicion

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"

def tokenizar(cadena: str) -> list:
    # 1. Validar alfabeto Σ
    for i, char in enumerate(cadena):
        if char not in ALFABETO:
            raise ValueError(f"Error Léxico: Símbolo '{repr(char)[1:-1]}' en posición {i+1} fuera del alfabeto Σ.")

    tokens = []
    i = 0
    n = len(cadena)

    while i < n:
        c = cadena[i]

        if c.isspace():
            i += 1
            continue

        if c == '.':
            raise ValueError(f"Error Léxico/Sintáctico en posición {i+1}: Columna o identificador no puede iniciar con punto ('.').")

        if c == ';':
            tokens.append(Token('PUNTO_Y_COMA', ';', i))
            i += 1
            continue

        if c in ",*()":
            tokens.append(Token('SIMBOLO', c, i))
            i += 1
            continue

        if c in "<>=":
            op = c
            if i + 1 < n and cadena[i+1] in "=":
                op += cadena[i+1]
                i += 1
            tokens.append(Token('OPERADOR', op, i))
            i += 1
            continue

        if c in LETRAS or c == '_':
            inicio = i
            while i < n and (cadena[i] in LETRAS or cadena[i] in NUMEROS or cadena[i] in '._'):
                if cadena[i] == '.' and (i + 1 == n or not (cadena[i+1] in LETRAS or cadena[i+1] == '_')):
                    raise ValueError(f"Error Léxico en posición {i+1}: Formato de identificador inválido cerca de '.'.")
                i += 1
            
            lexema = cadena[inicio:i]
            lexema_upper = lexema.upper()

            if lexema_upper in ("GROUP", "ORDER"):
                resto = cadena[i:].lstrip()
                if resto.upper().startswith("BY"):
                    offset_by = cadena[i:].find("BY") if "BY" in cadena[i:].upper() else 0
                    lexema_compuesto = f"{lexema_upper} BY"
                    tokens.append(Token('RESERVADA', lexema_compuesto, inicio))
                    i = i + offset_by + 2
                    continue

            if lexema_upper in PALABRAS_RESERVADAS:
                tokens.append(Token('RESERVADA', lexema_upper, inicio))
            else:
                tokens.append(Token('IDENTIFICADOR', lexema, inicio))
            continue

        if c in NUMEROS:
            inicio = i
            while i < n and cadena[i] in NUMEROS:
                i += 1
            tokens.append(Token('NUMERO', cadena[inicio:i], inicio))
            continue

        i += 1

    return tokens