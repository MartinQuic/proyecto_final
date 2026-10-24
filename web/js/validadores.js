// Conservar el helper `enviar` que ya define web/js/app.js.
let automataActual = null;

const $ = id => document.getElementById(id);

function mostrarTransiciones(etapa) {
  const host = $('tabla-auto');
  if (!host) return;
  host.replaceChildren();
  const transiciones = etapa?.transiciones || [];
  const tabla = document.createElement('table');
  const cabecera = document.createElement('tr');
  for (const titulo of ['Desde', 'Símbolo', 'Hacia']) {
    const th = document.createElement('th');
    th.textContent = titulo;
    cabecera.append(th);
  }
  tabla.append(cabecera);
  for (const t of transiciones) {
    const fila = document.createElement('tr');
    for (const valor of [t.desde, t.simbolo === '' ? 'ε' : t.simbolo, t.hacia]) {
      const td = document.createElement('td');
      td.textContent = String(valor ?? '');
      fila.append(td);
    }
    tabla.append(fila);
  }
  host.append(tabla);
}

function actualizarEtapa() {
  if (!automataActual) return;
  const nombre = $('etapa-auto')?.value || 'minimo';
  const etapa = automataActual[nombre];
  if (!etapa) {
    $('estado-grafo').textContent = `La respuesta de Python no contiene ${nombre}.`;
    return;
  }
  try {
    if (typeof window.pintarAutomata !== 'function') {
      throw new Error('No se cargó /static/js/grafo.js');
    }
    window.pintarAutomata(etapa, 'grafo-auto');
    $('estado-grafo').textContent = `${nombre.toUpperCase()}: ${etapa.estados?.length ?? 0} estados y ${etapa.transiciones?.length ?? 0} transiciones.`;
    mostrarTransiciones(etapa);
  } catch (error) {
    $('estado-grafo').textContent = `Error del dibujo: ${error.message}`;
    console.error('Error SVG:', error);
  }
}

function presentarSQL(d) {
  const out = $('resultado-sql');
  const items = d.sentencias || [];
  if (!items.length) {
    out.textContent = d.mensaje || JSON.stringify(d, null, 2);
    return;
  }
  out.textContent = [
    `Resultado: ${d.correctas}/${d.total} consultas válidas`,
    ...items.map(s => {
      const lugar = s.valido
        ? `Inicio: línea ${s.inicio.linea}, columna ${s.inicio.columna}`
        : `Error: línea ${s.linea}, columna ${s.columna} (posición ${s.posicion})`;
      return `\nConsulta ${s.numero}: ${s.valido ? 'ACEPTADA' : 'RECHAZADA'}\n${lugar}\n${s.codigo}: ${s.mensaje}`;
    })
  ].join('\n');
}

$('validar-sql')?.addEventListener('click', async () => {
  const salida = $('resultado-sql');
  salida.textContent = 'Validando consultas...';
  try {
    const respuesta = await enviar('/api/sql/validar', {consulta: $('consulta').value});
    presentarSQL(respuesta);
  } catch (error) {
    salida.textContent = `Error: ${error.message}`;
  }
});

$('generar')?.addEventListener('click', async () => {
  const salida = $('resultado-auto');
  salida.textContent = 'Generando...';
  $('estado-grafo').textContent = 'Construyendo diagrama...';
  try {
    const resultado = await enviar('/api/automatas/generar', {
      alfabeto: $('alfabeto').value,
      regex: $('regex').value,
      cadena: $('cadena').value
    });
    console.log('Respuesta autómata:', resultado);
    automataActual = resultado;
    window.ultimoAutomata = resultado;
    salida.textContent = (resultado.aceptada ? 'ACEPTADA' : 'RECHAZADA') + '\n' +
      (Array.isArray(resultado.pasos) ? resultado.pasos.join('\n') : '');
    $('dot').textContent = typeof resultado.dot === 'string' ? resultado.dot : JSON.stringify(resultado.dot ?? '', null, 2);
    actualizarEtapa();
  } catch (error) {
    salida.textContent = `Error: ${error.message}`;
    $('estado-grafo').textContent = 'No se pudo generar el autómata.';
    console.error(error);
  }
});

$('etapa-auto')?.addEventListener('change', actualizarEtapa);


// Limpiar solamente los campos y resultados de la sesión actual; no afecta SQLite.
$('limpiar-sql')?.addEventListener('click', () => {
  $('consulta').value = '';
  $('resultado-sql').textContent = '';
  $('consulta').focus();
});

$('limpiar-auto')?.addEventListener('click', () => {
  for (const id of ['alfabeto', 'regex', 'cadena']) $(id).value = '';
  for (const id of ['resultado-auto', 'dot']) $(id).textContent = '';
  $('tabla-auto')?.replaceChildren();
  $('grafo-auto')?.replaceChildren();
  $('estado-grafo').textContent = 'Ingresa una expresión y presiona «Generar y simular».';
  $('etapa-auto').value = 'minimo';
  automataActual = null;
  window.ultimoAutomata = null;
  $('alfabeto').focus();
});
