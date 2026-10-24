// Renderizador SVG de AFN, AFD y AFD mínimo. Sin dependencias externas.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  function elemento(tipo, atributos = {}, texto) {
    const nodo = document.createElementNS(NS, tipo);
    for (const [nombre, valor] of Object.entries(atributos)) nodo.setAttribute(nombre, String(valor));
    if (texto !== undefined) nodo.textContent = String(texto);
    return nodo;
  }

  function pintarAutomata(automata, idContenedor) {
    const host = document.getElementById(idContenedor);
    if (!host) throw new Error(`No existe el contenedor #${idContenedor}`);
    host.replaceChildren();
    if (!automata || !Array.isArray(automata.estados) || automata.estados.length === 0) {
      host.textContent = 'No hay estados para dibujar.';
      return;
    }

    const estados = automata.estados.map(String);
    const finales = new Set((automata.finales || []).map(String));
    const transiciones = automata.transiciones || [];
    const n = estados.length;
    const ancho = Math.max(540, Math.min(1100, n * 125 + 180));
    const alto = Math.max(400, Math.min(900, n * 90 + 150));
    const centroX = ancho / 2, centroY = alto / 2;
    const radio = Math.min(ancho, alto) * 0.33;
    const radioNodo = 25;
    const svg = elemento('svg', {viewBox: `0 0 ${ancho} ${alto}`, xmlns: NS, role: 'img', 'aria-label': 'Autómata con estados y transiciones'});
    svg.style.display = 'block';
    svg.style.width = '100%';
    svg.style.height = 'auto';
    svg.style.minHeight = '340px';

    const defs = elemento('defs');
    const marcador = elemento('marker', {id: 'punta-flecha-grafo', markerWidth: 10, markerHeight: 10, refX: 9, refY: 3, orient: 'auto'});
    marcador.append(elemento('path', {d: 'M0 0 L0 6 L9 3 z', fill: '#69cbd3'}));
    defs.append(marcador); svg.append(defs);

    const posiciones = new Map();
    estados.forEach((estado, indice) => {
      const angulo = -Math.PI / 2 + indice * 2 * Math.PI / n;
      posiciones.set(estado, {x: centroX + radio * Math.cos(angulo), y: centroY + radio * Math.sin(angulo)});
    });
    const conexiones = new Map();
    transiciones.forEach(t => {
      const origen = String(t.desde), destino = String(t.hacia);
      const clave = JSON.stringify([origen, destino]);
      if (!conexiones.has(clave)) conexiones.set(clave, []);
      conexiones.get(clave).push(t.simbolo === '' ? 'ε' : String(t.simbolo ?? 'ε'));
    });

    for (const [clave, simbolos] of conexiones) {
      const [origen, destino] = JSON.parse(clave);
      const p = posiciones.get(origen), q = posiciones.get(destino);
      if (!p || !q) continue;
      let recorrido, xEtiqueta, yEtiqueta;
      if (origen === destino) {
        recorrido = `M ${p.x - 13} ${p.y - 22} C ${p.x - 85} ${p.y - 115}, ${p.x + 85} ${p.y - 115}, ${p.x + 13} ${p.y - 22}`;
        xEtiqueta = p.x; yEtiqueta = p.y - 90;
      } else {
        const dx = q.x - p.x, dy = q.y - p.y, distancia = Math.hypot(dx, dy) || 1;
        const ux = dx / distancia, uy = dy / distancia;
        const sx = p.x + ux * radioNodo, sy = p.y + uy * radioNodo;
        const ex = q.x - ux * (radioNodo + 5), ey = q.y - uy * (radioNodo + 5);
        const inversa = conexiones.has(JSON.stringify([destino, origen]));
        const curvatura = inversa ? (origen < destino ? 28 : -28) : 0;
        const mx = (sx + ex) / 2 - uy * curvatura;
        const my = (sy + ey) / 2 + ux * curvatura;
        recorrido = `M ${sx} ${sy} Q ${mx} ${my} ${ex} ${ey}`;
        xEtiqueta = (sx + 2 * mx + ex) / 4;
        yEtiqueta = (sy + 2 * my + ey) / 4 - 10;
      }
      svg.append(elemento('path', {d: recorrido, fill: 'none', stroke: '#69cbd3', 'stroke-width': 2, 'marker-end': 'url(#punta-flecha-grafo)'}));
      svg.append(elemento('text', {x: xEtiqueta, y: yEtiqueta, 'text-anchor': 'middle', fill: '#f5cf84', 'font-size': 15}, [...new Set(simbolos)].join(', ')));
    }

    for (const estado of estados) {
      const p = posiciones.get(estado);
      svg.append(elemento('circle', {cx: p.x, cy: p.y, r: radioNodo, fill: estado === String(automata.inicial) ? '#296a70' : '#192d44', stroke: '#d3e8f0', 'stroke-width': 2}));
      if (finales.has(estado)) svg.append(elemento('circle', {cx: p.x, cy: p.y, r: radioNodo - 5, fill: 'none', stroke: '#d3e8f0', 'stroke-width': 2}));
      svg.append(elemento('text', {x: p.x, y: p.y + 5, 'text-anchor': 'middle', fill: '#ffffff', 'font-size': 15}, `q${estado}`));
    }
    const inicial = posiciones.get(String(automata.inicial));
    if (inicial) svg.append(elemento('path', {d: `M ${inicial.x - 83} ${inicial.y} H ${inicial.x - 33}`, fill: 'none', stroke: '#f5cf84', 'stroke-width': 2, 'marker-end': 'url(#punta-flecha-grafo)'}));
    host.append(svg);
  }
  window.pintarAutomata = pintarAutomata;
})();
