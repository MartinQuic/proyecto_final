const secciones=[...document.querySelectorAll('main section')];
function navegar(id){secciones.forEach(s=>s.hidden=s.id!==id);document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('activo',b.dataset.tab===id));if(id==='config')cargarReglas();}
document.querySelectorAll('nav button').forEach(b=>b.addEventListener('click',()=>navegar(b.dataset.tab)));
navegar('inicio');
async function jsonFetch(url,opts={}){const r=await fetch(url,opts);const x=await r.json();if(!r.ok)throw new Error(x.detail||r.statusText);return x}
const enviar=(url,data)=>jsonFetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
