from core.modelos import AutomataSintactico

def convertir_afd(afn: AutomataSintactico) -> AutomataSintactico:
    # El autómata sintáctico ya nace en su forma determinista (AFD)
    return afn