'use strict';

const secciones = [...document.querySelectorAll('main section')];

function navegar(id) {
  secciones.forEach(s => { s.hidden = s.id !== id; });
  document.querySelectorAll('nav button[data-tab]').forEach(b => {
    b.classList.toggle('activo', b.dataset.tab === id);
  });
  if (id === 'config') {
    if (typeof cargarReglas === 'function') {
      Promise.resolve(cargarReglas()).catch(console.error);
    }
    if (typeof cargarPersonalizadas === 'function') {
      Promise.resolve(cargarPersonalizadas()).catch(error => {
        const host = document.getElementById('personalizadas');
        if (host) host.textContent = `No se pudieron cargar los validadores personalizados: ${error.message}`;
        console.error(error);
      });
    }
  }
}

document.querySelectorAll('nav button[data-tab]').forEach(button => {
  button.addEventListener('click', () => navegar(button.dataset.tab));
});

async function jsonFetch(url, options = {}) {
  const response = await fetch(url, options);
  const contentType = response.headers.get('content-type') || '';
  const result = contentType.includes('application/json')
    ? await response.json()
    : { detail: await response.text() };
  if (!response.ok) {
    const detalle = result.detail;
    throw new Error(typeof detalle === 'string' ? detalle : JSON.stringify(detalle || `HTTP ${response.status}`));
  }
  return result;
}

const enviar = (url, data) => jsonFetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});

navegar('inicio');
