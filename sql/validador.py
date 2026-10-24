"""Validador educativo de consultas SELECT; no ejecuta sentencias SQL."""
from dataclasses import dataclass
from .afd_lexico import tokenizar, FalloLexico

REGLAS = [
    ('SQL_01', 'SELECT básico'), ('SQL_02', 'Columnas múltiples'),
    ('SQL_03', 'Comodín *'), ('SQL_04', 'WHERE y comparación'),
    ('SQL_05', 'AND / OR'), ('SQL_06', 'ORDER BY'),
    ('SQL_07', 'GROUP BY'), ('SQL_08', 'HAVING'),
    ('SQL_09', 'JOIN (INNER / LEFT / RIGHT / FULL)'), ('SQL_10', 'LIMIT'),
]
COMPARADORES = {'=', '>', '<', '>=', '<=', '!=', '<>'}
PALABRAS = {
    'SELECT', 'FROM', 'WHERE', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'JOIN', 'ON', 'AS', 'ORDER',
    'GROUP', 'BY', 'HAVING', 'LIMIT', 'AND', 'OR', 'ASC', 'DESC'
}

@dataclass
class Token:
    value: str
    start: int
    end: int
    kind: str

class ErrorSQL(ValueError):
    def __init__(self, mensaje, token=None, codigo='SINTAXIS_SQL'):
        super().__init__(mensaje)
        self.token = token
        self.codigo = codigo

def _ubicacion(texto, indice):
    return {
        'linea': texto.count('\n', 0, indice) + 1,
        'columna': indice - texto.rfind('\n', 0, indice),
        'posicion': indice,
    }

def _tokens(texto):
    """El AFD léxico produce los tokens que consume Parser."""
    try:
        return [Token(t.value, t.start, t.end, t.kind) for t in tokenizar(texto)]
    except FalloLexico as e:
        t = Token('', e.posicion, e.posicion, 'OTHER')
        raise ErrorSQL(str(e), t, 'LEXICO_SQL') from e

class Parser:
    def __init__(self, tokens, final):
        self.t = tokens
        self.i = 0
        self.final = final
        self.usadas = {'SQL_01'}
        self.tablas = set()
        self.aliases = set()
        self.referencias = []

    def actual(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def palabra(self):
        x = self.actual()
        return x.value.upper() if x else None

    def tomar(self, valor=None):
        x = self.actual()
        if x is None or (valor is not None and x.value.upper() != valor):
            raise ErrorSQL('Se esperaba ' + (valor or 'un token'),
                           x or Token('', self.final, self.final, 'EOF'))
        self.i += 1
        return x

    def aceptar(self, valor):
        if self.palabra() == valor:
            self.tomar()
            return True
        return False

    def identificador(self):
        x = self.actual()
        if x is None or x.kind != 'ID' or x.value.upper() in PALABRAS:
            raise ErrorSQL('Se esperaba un identificador',
                           x or Token('', self.final, self.final, 'EOF'))
        return self.tomar()

    def columna(self, admitir_comodin=True):
        x = self.actual()
        if admitir_comodin and self.aceptar('*'):
            self.usadas.add('SQL_03')
            return
        if x is None:
            raise ErrorSQL('Se esperaba columna', Token('', self.final, self.final, 'EOF'))
        self.identificador()
        if self.aceptar('('):
            if self.aceptar('*'):
                self.usadas.add('SQL_03')
            else:
                self.columna(False)
            self.tomar(')')
        elif self.aceptar('.'):
            self.referencias.append(x)
            if self.aceptar('*'):
                self.usadas.add('SQL_03')
            else:
                self.identificador()

    def origen(self):
        nombre = self.identificador()
        if self.aceptar('.'):
            nombre = self.identificador()
        tabla = nombre.value.casefold()
        if tabla in self.tablas or tabla in self.aliases:
            raise ErrorSQL('Tabla o alias duplicado: ' + nombre.value, nombre, 'ALIAS_DUPLICADO')
        self.tablas.add(tabla)
        self.aceptar('AS')
        x = self.actual()
        if x and x.kind == 'ID' and x.value.upper() not in PALABRAS:
            alias = self.identificador()
            a = alias.value.casefold()
            if a in self.aliases or (a in self.tablas and a != tabla):
                raise ErrorSQL('Alias duplicado: ' + alias.value, alias, 'ALIAS_DUPLICADO')
            self.aliases.add(a)
            self.tablas.discard(tabla)
            self.tablas.add(a)
        return nombre

    def valor(self):
        x = self.actual()
        if x is None:
            raise ErrorSQL('Falta un valor', Token('', self.final, self.final, 'EOF'))
        if x.kind in ('STRING', 'NUM'):
            self.tomar()
        else:
            self.columna(False)

    def condicion(self):
        self.comparacion()
        while self.palabra() in ('AND', 'OR'):
            self.usadas.add('SQL_05')
            self.tomar()
            self.comparacion()

    def comparacion(self, en_join=False):
        izquierda = self.actual()
        if en_join and izquierda is not None and izquierda.kind == 'ID':
            siguiente = self.t[self.i + 1] if self.i + 1 < len(self.t) else None
            if siguiente is None or siguiente.value != '.':
                raise ErrorSQL(
                    f"Columna '{izquierda.value}' sin tabla o alias en JOIN. Usa U.id = C.id",
                    izquierda, 'COLUMNA_SIN_CALIFICAR'
                )
        self.columna(False)
        op = self.actual()
        if not op or op.value not in COMPARADORES:
            raise ErrorSQL('Se esperaba operador de comparación',
                           op or Token('', self.final, self.final, 'EOF'))
        self.tomar()
        derecha = self.actual()
        if en_join:
            if derecha is None or derecha.kind != 'ID':
                raise ErrorSQL('JOIN requiere columna calificada en ambos lados',
                               derecha or Token('', self.final, self.final, 'EOF'),
                               'COLUMNA_SIN_CALIFICAR')
            siguiente = self.t[self.i + 1] if self.i + 1 < len(self.t) else None
            if siguiente is None or siguiente.value != '.':
                raise ErrorSQL(
                    f"Columna '{derecha.value}' sin tabla o alias en JOIN. Usa U.id = C.id",
                    derecha, 'COLUMNA_SIN_CALIFICAR'
                )
        self.valor()

    def analizar(self):
        self.tomar('SELECT')
        self.columna()
        while self.aceptar(','):
            self.usadas.add('SQL_02')
            self.columna()
        self.tomar('FROM')
        self.origen()
        while self.palabra() in ('INNER', 'LEFT', 'RIGHT', 'FULL', 'JOIN'):
            self.usadas.add('SQL_09')
            # JOIN equivale a INNER JOIN. OUTER es opcional en LEFT/RIGHT/FULL.
            tipo = self.palabra()
            if tipo != 'JOIN':
                self.tomar()
                if tipo in ('LEFT', 'RIGHT', 'FULL'):
                    self.aceptar('OUTER')
            self.tomar('JOIN')
            self.origen()
            self.tomar('ON')
            self.comparacion(en_join=True)
        if self.aceptar('WHERE'):
            self.usadas.add('SQL_04')
            self.condicion()
        if self.aceptar('GROUP'):
            self.usadas.add('SQL_07')
            self.tomar('BY')
            self.columna(False)
            while self.aceptar(','):
                self.columna(False)
        if self.aceptar('HAVING'):
            self.usadas.add('SQL_08')
            if 'SQL_07' not in self.usadas:
                raise ErrorSQL('HAVING requiere GROUP BY', self.t[self.i - 1])
            self.condicion()
        if self.aceptar('ORDER'):
            self.usadas.add('SQL_06')
            self.tomar('BY')
            self.columna(False)
            if self.palabra() in ('ASC', 'DESC'):
                self.tomar()
            while self.aceptar(','):
                self.columna(False)
                if self.palabra() in ('ASC', 'DESC'):
                    self.tomar()
        if self.aceptar('LIMIT'):
            self.usadas.add('SQL_10')
            n = self.actual()
            if not n or n.kind != 'NUM' or not n.value.isdigit():
                raise ErrorSQL('LIMIT requiere un entero',
                               n or Token('', self.final, self.final, 'EOF'))
            self.tomar()
        if self.actual():
            raise ErrorSQL('Token inesperado: ' + self.actual().value, self.actual())
        for ref in self.referencias:
            if ref.value.casefold() not in self.tablas:
                raise ErrorSQL('Alias o tabla no declarada: ' + ref.value,
                               ref, 'ALIAS_NO_DECLARADO')
        return sorted(self.usadas)

def _sentencias(tokens):
    grupos = []
    actual = []
    for t in tokens:
        if t.value == ';':
            if actual:
                grupos.append(actual)
                actual = []
        else:
            actual.append(t)
    if actual:
        grupos.append(actual)
    return grupos

def validar(sql, activas):
    """Valida múltiples SELECT separadas por ';' con posiciones absolutas base cero."""
    try:
        tokens = _tokens(sql)
    except ErrorSQL as e:
        return {'valido': False, 'codigo': e.codigo, 'mensaje': str(e),
                **_ubicacion(sql, e.token.start), 'sentencias': [], 'total': 0}
    grupos = _sentencias(tokens)
    if not grupos:
        return {'valido': False, 'codigo': 'SQL_VACIO', 'mensaje': 'No se ingresaron consultas',
                'linea': 1, 'columna': 1, 'posicion': 0, 'sentencias': [], 'total': 0}
    resultados = []
    for numero, grupo in enumerate(grupos, 1):
        p = Parser(grupo, grupo[-1].end)
        inicio = _ubicacion(sql, grupo[0].start)
        r = {'numero': numero, 'inicio': inicio,
             'consulta': sql[grupo[0].start:grupo[-1].end]}
        try:
            usadas = p.analizar()
            inactivas = sorted(set(usadas) - set(activas))
            if inactivas:
                raise ErrorSQL('Reglas inactivas: ' + ', '.join(inactivas),
                               grupo[0], 'REGLA_INACTIVA')
            r.update(valido=True, codigo='OK', mensaje='Consulta válida', reglas_usadas=usadas)
        except ErrorSQL as e:
            donde = _ubicacion(sql, e.token.start if e.token else grupo[0].start)
            r.update(valido=False, codigo=e.codigo, mensaje=str(e),
                     reglas_usadas=sorted(p.usadas), **donde)
        resultados.append(r)
    errores = [r for r in resultados if not r['valido']]
    respuesta = {
        'valido': not errores, 'codigo': 'OK' if not errores else 'ERROR_SQL',
        'mensaje': f'{len(resultados)-len(errores)} de {len(resultados)} consultas válidas',
        'total': len(resultados), 'correctas': len(resultados)-len(errores),
        'errores': len(errores), 'sentencias': resultados,
    }
    if len(resultados) == 1:
        unico = resultados[0]
        respuesta.update(codigo=unico['codigo'], mensaje=unico['mensaje'],
                         reglas_usadas=unico.get('reglas_usadas', []))
        if not unico['valido']:
            for campo in ('linea', 'columna', 'posicion'):
                respuesta[campo] = unico[campo]
    return respuesta
