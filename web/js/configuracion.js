'use strict';

async function cargarReglas() {
  const contenedor = document.getElementById('reglas');
  if (!contenedor) return;
  contenedor.textContent = 'Cargando reglas...';
  try {
    const reglas = await jsonFetch('/api/configuracion/reglas');
    contenedor.replaceChildren();
    for (const regla of reglas) {
      const fila = document.createElement('div');
      fila.className = 'regla';
      const texto = document.createElement('span');
      texto.textContent = `${regla.id} — ${regla.nombre}`;
      const activo = document.createElement('input');
      activo.type = 'checkbox';
      activo.checked = Boolean(regla.activo);
      activo.setAttribute('aria-label', `Activar ${regla.nombre}`);
      activo.addEventListener('change', async () => {
        activo.disabled = true;
        try {
          await jsonFetch(`/api/configuracion/reglas/${encodeURIComponent(regla.id)}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ activo: activo.checked })
          });
        } catch (error) {
          activo.checked = !activo.checked;
          alert(error.message);
        } finally {
          activo.disabled = false;
        }
      });
      fila.append(texto, activo);
      contenedor.append(fila);
    }
  } catch (error) {
    contenedor.textContent = `Error cargando reglas: ${error.message}`;
  }
}
