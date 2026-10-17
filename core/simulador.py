"""INTEGRANTE 5. Simulador de AFD con recorrido paso a paso."""
from core.modelos import Automata
from core.lexico import validar_cadena

def simular(afd: Automata, cadena: str) -> tuple[bool, list[str]]:
    validar_cadena(cadena,afd.alfabeto)
    actual=afd.inicial; pasos=[f'Inicio: q{actual}']
    for simbolo in cadena:
        destinos=afd.destinos(actual,simbolo)
        if len(destinos)!=1:
            pasos.append(f'Sin transición con {simbolo}: rechazo')
            return False,pasos
        siguiente=next(iter(destinos))
        pasos.append(f'q{actual} --{simbolo}--> q{siguiente}')
        actual=siguiente
    aceptada=actual in afd.finales
    pasos.append('ACEPTADA' if aceptada else 'RECHAZADA')
    return aceptada,pasos
