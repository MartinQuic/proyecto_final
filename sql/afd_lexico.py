"""AFD de tokens SQL: reconocimiento real, carácter por carácter.

Estados de identificadores: q0 -> q_id (letra/_), q_id -> q_id (letra/dígito/_).
Estados numéricos: q0 -> q_int (dígito), q_int -> q_dot (.),
                 q_dot -> q_decimal (dígito), q_decimal -> q_decimal (dígito).
q_id, q_int y q_decimal son estados de aceptación.
Un token se acepta al no existir transición para el siguiente carácter.
El analizador sintáctico (Parser) valida la estructura SQL posteriormente.
"""
from dataclasses import dataclass

# δ: estado x clase de carácter -> nuevo estado
TRANSICIONES = {
    'q0': {'LETRA': 'q_id', 'DIGITO': 'q_int', 'GUION_BAJO': 'q_id'},
    'q_id': {'LETRA': 'q_id', 'DIGITO': 'q_id', 'GUION_BAJO': 'q_id'},
    'q_int': {'DIGITO': 'q_int', 'PUNTO': 'q_dot'},
    'q_dot': {'DIGITO': 'q_decimal'},
    'q_decimal': {'DIGITO': 'q_decimal'},
}
ACEPTACION = {'q_id': 'ID', 'q_int': 'NUM', 'q_decimal': 'NUM'}
PUNTUACION = frozenset('(),;.*=<>+/-')
OPERADORES_DOBLES = frozenset(('>=', '<=', '!=', '<>'))


@dataclass(frozen=True)
class TokenLexico:
    value: str
    start: int
    end: int
    kind: str


class FalloLexico(ValueError):
    def __init__(self, mensaje, posicion):
        super().__init__(mensaje)
        self.posicion = posicion


def clase(c):
    # Mismo alfabeto de identificadores que el regex anterior: ASCII.
    if 'a' <= c <= 'z' or 'A' <= c <= 'Z':
        return 'LETRA'
    if '0' <= c <= '9':
        return 'DIGITO'
    if c == '_':
        return 'GUION_BAJO'
    if c == '.':
        return 'PUNTO'
    return 'OTRO'


def reconocer_palabra_numero(texto, inicio):
    """Ejecuta el AFD y devuelve el token y su posición de fin."""
    estado = 'q0'
    i = inicio
    ultimo_final = None
    while i < len(texto):
        siguiente = TRANSICIONES[estado].get(clase(texto[i]))
        if siguiente is None:
            break
        estado = siguiente
        i += 1
        if estado in ACEPTACION:
            ultimo_final = (i, ACEPTACION[estado])
    if ultimo_final is None:
        return None
    fin, tipo = ultimo_final
    return TokenLexico(texto[inicio:fin], inicio, fin, tipo)


def tokenizar(texto):
    """Tokenizador por AFD sin re.finditer. Omite espacios y comentarios SQL."""
    tokens = []
    i = 0
    n = len(texto)
    while i < n:
        c = texto[i]
        if c.isspace():
            i += 1
            continue
        if texto.startswith('--', i):
            fin = texto.find('\n', i + 2)
            i = n if fin == -1 else fin
            continue
        if texto.startswith('/*', i):
            fin = texto.find('*/', i + 2)
            if fin == -1:
                raise FalloLexico('Comentario de bloque sin cerrar', i)
            i = fin + 2
            continue
        if c == "'":
            inicio = i
            i += 1
            while i < n:
                if texto[i] == "'":
                    if i + 1 < n and texto[i + 1] == "'":
                        i += 2  # comilla escapada SQL: ''
                        continue
                    i += 1
                    tokens.append(TokenLexico(texto[inicio:i], inicio, i, 'STRING'))
                    break
                i += 1
            else:
                raise FalloLexico('Cadena de texto sin cerrar', inicio)
            continue
        t = reconocer_palabra_numero(texto, i)
        if t is not None:
            tokens.append(t)
            i = t.end
            continue
        dos = texto[i:i + 2]
        if dos in OPERADORES_DOBLES:
            tokens.append(TokenLexico(dos, i, i + 2, 'OP'))
            i += 2
            continue
        if c in PUNTUACION:
            tokens.append(TokenLexico(c, i, i + 1, 'PUNC'))
            i += 1
            continue
        raise FalloLexico('Carácter no reconocido: ' + c, i)
    return tokens
