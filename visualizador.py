"""INTEGRANTE 6. Exportación a DOT y a tablas, sin dependencias obligatorias."""
from core.modelos import Automata

def generar_dot(automata: Automata, titulo: str='Autómata') -> str:
    lineas=['digraph Automata {','  rankdir=LR;',f'  label="{titulo}";', '  labelloc=t;', '  node [shape=circle];', '  inicio [shape=point];',f'  inicio -> q{automata.inicial};']
    for q in sorted(automata.estados):
        forma='doublecircle' if q in automata.finales else 'circle'
        lineas.append(f'  q{q} [shape={forma}];')
    for (a,s),destinos in sorted(automata.transiciones.items()):
        for b in sorted(destinos): lineas.append(f'  q{a} -> q{b} [label="{s}"];')
    lineas.append('}')
    return '\n'.join(lineas)
