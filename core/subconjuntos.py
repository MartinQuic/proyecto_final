"""INTEGRANTE 4. Determinización mediante ε-cerradura y subconjuntos."""
from collections import deque
from core.modelos import Automata, EPSILON

def cerradura(afn: Automata, estados: set[int]) -> frozenset[int]:
    vistos=set(estados); pendientes=list(estados)
    while pendientes:
        q=pendientes.pop()
        for dest in afn.destinos(q,EPSILON)-vistos:
            vistos.add(dest); pendientes.append(dest)
    return frozenset(vistos)

def convertir_afd(afn: Automata) -> Automata:
    inicio=cerradura(afn,{afn.inicial})
    indices={inicio:0}; cola=deque([inicio])
    afd=Automata(estados={0},alfabeto=set(afn.alfabeto),inicial=0)
    while cola:
        grupo=cola.popleft(); origen=indices[grupo]
        if grupo & afn.finales: afd.finales.add(origen)
        for simbolo in sorted(afn.alfabeto):
            mover=set().union(*(afn.destinos(e,simbolo) for e in grupo))
            destino=cerradura(afn,mover)
            if destino not in indices:
                indices[destino]=len(indices); cola.append(destino)
                afd.estados.add(indices[destino])
            afd.agregar(origen,simbolo,indices[destino])
    return afd
