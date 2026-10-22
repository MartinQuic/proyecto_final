async function cargarPersonalizadas(){
 const host=document.getElementById('personalizadas');if(!host)return;
 host.replaceChildren();
 const reglas=await jsonFetch('/api/configuracion/personalizadas');
 for(const r of reglas){const fila=document.createElement('div');fila.className='regla';
 const nombre=document.createElement('span');nombre.textContent=`${r.nombre} (${r.operador}: ${r.patron})`;
 const activo=document.createElement('input');activo.type='checkbox';activo.checked=r.activo;
 activo.onchange=async()=>{try{await jsonFetch('/api/configuracion/personalizadas/'+r.id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({activo:activo.checked})})}catch(e){activo.checked=!activo.checked;alert(e.message)}};
 const borrar=document.createElement('button');borrar.textContent='Eliminar';borrar.onclick=async()=>{if(!confirm('¿Eliminar regla?'))return;await jsonFetch('/api/configuracion/personalizadas/'+r.id,{method:'DELETE'});await cargarPersonalizadas()};
 fila.append(nombre,activo,borrar);host.append(fila);
 }
}
document.getElementById('form-personalizada').addEventListener('submit',async(e)=>{
 e.preventDefault(); const form=e.target;
 try{await jsonFetch('/api/configuracion/personalizadas',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nombre:form.elements.nombre.value,operador:form.elements.operador.value,patron:form.elements.patron.value})});form.reset();await cargarPersonalizadas()}catch(x){alert(x.message)}
});
