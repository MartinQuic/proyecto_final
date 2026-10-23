'use strict';

async function cargarPersonalizadas() {
  const host = document.getElementById('personalizadas');
  if (!host) return;
  host.textContent = 'Cargando validadores...';
  try {
    const reglas = await jsonFetch('/api/configuracion/personalizadas');
    host.replaceChildren();
    for (const regla of reglas) {
      const fila = document.createElement('div');
      fila.className = 'regla';
      const texto = document.createElement('span');
      texto.textContent = `${regla.nombre} (${regla.operador}: ${regla.patron})`;
      const activo = document.createElement('input');
      activo.type = 'checkbox';
      activo.checked = Boolean(regla.activo);
      activo.addEventListener('change', async () => {
        activo.disabled = true;
        try {
          await jsonFetch(`/api/configuracion/personalizadas/${encodeURIComponent(regla.id)}`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({activo: activo.checked})
          });
        } catch(error) {
          activo.checked = !activo.checked;
          alert(error.message);
        } finally { activo.disabled = false; }
      });
      const eliminar = document.createElement('button');
      eliminar.type = 'button';
      eliminar.textContent = 'Eliminar';
      eliminar.addEventListener('click', async () => {
        if (!confirm('¿Eliminar este validador?')) return;
        try {
          await jsonFetch(`/api/configuracion/personalizadas/${encodeURIComponent(regla.id)}`, {method: 'DELETE'});
          await cargarPersonalizadas();
        } catch (error) { alert(error.message); }
      });
      fila.append(texto, activo, eliminar);
      host.append(fila);
    }
  } catch (error) {
    host.textContent = `No se pudieron cargar los validadores personalizados: ${error.message}`;
  }
}

const formularioPersonalizado = document.getElementById('form-personalizada');
if (formularioPersonalizado) {
  formularioPersonalizado.addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const boton = form.querySelector('button[type="submit"]');
    if (boton) boton.disabled = true;
    try {
      await jsonFetch('/api/configuracion/personalizadas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          nombre: form.elements.nombre.value,
          operador: form.elements.operador.value,
          patron: form.elements.patron.value
        })
      });
      form.reset();
      await cargarPersonalizadas();
    } catch (error) {
      alert(error.message);
    } finally {
      if (boton) boton.disabled = false;
    }
  });
}
