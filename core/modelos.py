"""INTEGRANTE 3. Modelo compartido de autómatas."""
from dataclasses import dataclass, field

EPSILON = 'ε'

@dataclass
class Automata:
    estados: set[int] = field(default_factory=set)
    alfabeto: set[str] = field(default_factory=set)
    transiciones: dict[tuple[int, str], set[int]] = field(default_factory=dict)
    inicial: int = 0
    finales: set[int] = field(default_factory=set)

    def agregar(self, origen: int, simbolo: str, destino: int) -> None:
        self.estados.update((origen, destino))
        self.transiciones.setdefault((origen, simbolo), set()).add(destino)
        if simbolo != EPSILON:
            self.alfabeto.add(simbolo)

    def destinos(self, origen: int, simbolo: str) -> set[int]:
        return self.transiciones.get((origen, simbolo), set())

    def tabla(self) -> str:
        encabezado = 'Estado | ' + ' | '.join(sorted(self.alfabeto))
        if any(s == EPSILON for _, s in self.transiciones):
            encabezado += ' | ε'
        lineas = [encabezado, '-' * len(encabezado)]
        for estado in sorted(self.estados):
            etiqueta = ('→' if estado == self.inicial else '') + ('*' if estado in self.finales else '') + f'q{estado}'
            simbolos = sorted(self.alfabeto) + ([EPSILON] if ' | ε' in encabezado else [])
            celdas = [','.join('q'+str(d) for d in sorted(self.destinos(estado,s))) or '—' for s in simbolos]
            lineas.append(etiqueta + ' | ' + ' | '.join(celdas))
        return '\n'.join(lineas)
