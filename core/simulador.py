"""
MÓDULO 6: Simulador del AFD con Validación Semántica de Alias (2 Pases)
Soporta la lectura previa de alias en FROM/JOIN antes de evaluar las columnas del SELECT.
"""

from core.lexico import tokenizar

def simular(afd, cadena: str) -> tuple:
    pasos = []
    
    # 1. Análisis Léxico
    try:
        tokens = tokenizar(cadena)
    except ValueError as err:
        pasos.append(str(err))
        pasos.append("Resultado: CADENA RECHAZADA (Error Léxico)")
        return False, pasos

    if not tokens:
        pasos.append("Error: La cadena de entrada está vacía.")
        return False, pasos

    # -------------------------------------------------------------------
    # PASE 1: RECOLECCIÓN PREVIA DE ALIAS POR CONSULTA (SEPARADAS POR ';')
    # -------------------------------------------------------------------
    # Estructura: lista de conjuntos, donde cada posición representa una consulta SQL
    alias_por_consulta = []
    alias_actuales = set()
    
    n = len(tokens)
    for i in range(n):
        tok = tokens[i]
        
        # Detectar declaración de alias: 'FROM tabla alias' o 'JOIN tabla alias'
        if tok.valor in ("FROM", "JOIN", "INNER", "LEFT", "RIGHT"):
            # Buscar el token de la tabla y luego su alias si existe
            j = i + 1
            # Omitir palabras tipo 'JOIN' si venía de INNER/LEFT/RIGHT
            if j < n and tokens[j].valor == "JOIN":
                j += 1
            # tokens[j] es la tabla, tokens[j+1] es el alias
            if j + 1 < n and tokens[j].tipo == "IDENTIFICADOR" and tokens[j+1].tipo == "IDENTIFICADOR":
                # Asegurar que el alias no sea una palabra clave ni parte del ON/WHERE
                alias_candidato = tokens[j+1].valor
                if alias_candidato.upper() not in ("WHERE", "JOIN", "ON", "GROUP", "ORDER", "LEFT", "RIGHT", "INNER"):
                    alias_actuales.add(alias_candidato)

        if tok.valor == ";":
            alias_por_consulta.append(alias_actuales)
            alias_actuales = set()

    alias_por_consulta.append(alias_actuales)  # Para la última o única consulta

    # -------------------------------------------------------------------
    # PASE 2: SIMULACIÓN EN EL AFD Y VERIFICACIÓN SEMÁNTICA
    # -------------------------------------------------------------------
    estado_actual = afd.inicial
    pasos.append(f"Estado Inicial: q{estado_actual}")

    idx_consulta = 0
    alias_validos_consulta = alias_por_consulta[idx_consulta] if alias_por_consulta else set()

    for i, tok in enumerate(tokens):

        # Validar consistencia de prefijos 'alias.columna'
        if tok.tipo == "IDENTIFICADOR" and "." in tok.valor:
            prefijo = tok.valor.split(".")[0]
            if alias_validos_consulta and prefijo not in alias_validos_consulta:
                pasos.append(f" Error Semántico en '{tok.valor}' (Posición {tok.posicion + 1}): El alias '{prefijo}' no concuerda con las tablas declaradas {alias_validos_consulta} en la cláusula FROM/JOIN.")
                pasos.append("Resultado: CADENA RECHAZADA")
                return False, pasos

        # Al avanzar de consulta con ';', cambiar al conjunto de alias de la siguiente consulta
        if tok.valor == ";":
            idx_consulta += 1
            if idx_consulta < len(alias_por_consulta):
                alias_validos_consulta = alias_por_consulta[idx_consulta]

        # Transición en el Autómata Finito Determinista
        siguiente = afd.obtener_destino(estado_actual, tok.valor)
        if siguiente is None:
            siguiente = afd.obtener_destino(estado_actual, tok.tipo)

        if siguiente is None:
            pasos.append(f" Error Sintáctico en token '{tok.valor}' (Posición {tok.posicion + 1}): No existe transición desde q{estado_actual}.")
            pasos.append("Resultado: CADENA RECHAZADA")
            return False, pasos

        pasos.append(f"q{estado_actual} --['{tok.valor}']--> q{siguiente}")
        estado_actual = siguiente

    # Comprobación de Aceptación Final
    es_aceptada = estado_actual in afd.finales

    if es_aceptada:
        pasos.append(f" Fin de evaluación en Estado de Aceptación q{estado_actual}.")
        pasos.append("Resultado: SINTAXIS VÁLIDA (CADENA ACEPTADA)")
    else:
        pasos.append(f" Fin de cadena en Estado NO final q{estado_actual}. Sentencia incompleta.")
        pasos.append("Resultado: CADENA RECHAZADA")

    return es_aceptada, pasos