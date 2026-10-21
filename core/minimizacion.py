"""INTEGRANTE 5. Minimización por refinamiento de particiones."""
from collections import deque
from core.modelos import Automata

def minimizar(afd: Automata) -> Automata:
    # Se consideran solo los estados alcanzables.
    alcanzables={afd.inicial}; cola=deque([afd.inicial])
    while cola:
        q=cola.popleft()
        for s in afd.alfabeto:
            for d in afd.destinos(q,s)-alcanzables:
                alcanzables.add(d); cola.append(d)
    finales=afd.finales & alcanzables
    grupos=[g for g in [finales, alcanzables-finales] if g]
    while True:
        mapa={q:i for i,g in enumerate(grupos) for q in g}
        nuevos=[]
        for grupo in grupos:
            firmas={}
            for q in grupo:
                firma=tuple(mapa.get(next(iter(afd.destinos(q,s)),None),-1) for s in sorted(afd.alfabeto))
                firmas.setdefault(firma,set()).add(q)
            nuevos.extend(firmas.values())
        if len(nuevos)==len(grupos): break
        grupos=nuevos
    mapa={q:i for i,g in enumerate(grupos) for q in g}
    minimo=Automata(estados=set(range(len(grupos))),alfabeto=set(afd.alfabeto),inicial=mapa[afd.inicial],finales={mapa[q] for q in finales})
    for i,grupo in enumerate(grupos):
        q=next(iter(grupo))
        for s in afd.alfabeto:
            for destino in afd.destinos(q,s):
                minimo.agregar(i,s,mapa[destino])
    return minimo
