"""INTEGRANTE 2. Validación del alfabeto y la cadena de entrada."""
OPERADORES = set('|*()+.ε')

def leer_alfabeto(texto: str) -> set[str]:
    """Admite '0,1', '{0,1}' o '01'; símbolos de un carácter."""
    texto = texto.strip().strip('{}').strip()
    if not texto:
        raise ValueError('El alfabeto no puede estar vacío.')
    if ',' in texto:
        partes = [s.strip() for s in texto.split(',')]
    else:
        partes = [c for c in texto if not c.isspace()]
    if any(len(s) != 1 or s.isspace() for s in partes):
        raise ValueError('Cada símbolo del alfabeto debe tener exactamente un carácter.')
    if any(s in OPERADORES for s in partes):
        raise ValueError('El alfabeto no puede contener operadores reservados: | * ( ) + . ε')
    return set(partes)

def validar_cadena(cadena: str, alfabeto: set[str]) -> None:
    for indice, simbolo in enumerate(cadena):
        if simbolo not in alfabeto:
            raise ValueError(f"Símbolo '{simbolo}' en posición {indice+1} fuera del alfabeto.")
