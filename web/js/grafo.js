// Gráfico SVG sin dependencias externas. Adecuado para autómatas pequeños/medianos.
function pintarAutomata(a, contenedor) {
 const el=document.getElementById(contenedor);el.replaceChildren();
 if(!a || !a.estados || !a.estados.length)return;
 const ns='http://www.w3.org/2000/svg';
 const svg=document.createElementNS(ns,'svg');
 const estados=a.estados.map(String); const n=estados.length;
 const size=Math.max(480,Math.min(1050, 160+n*100));const cx=size/2,cy=size/2;
 const radio=Math.min(size*.36, Math.max(80, n*22));const nr=24;
 svg.setAttribute('viewBox',`0 0 ${size} ${size}`);svg.setAttribute('role','img');
 svg.setAttribute('aria-label','Diagrama del autómata con estados y transiciones');
 const mk=(tag,attrs={},text)=>{const e=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;return e};
 const defs=mk('defs');const marker=mk('marker',{id:'flecha-auto',markerWidth:10,markerHeight:10,refX:9,refY:3,orient:'auto',markerUnits:'strokeWidth'});marker.append(mk('path',{d:'M0,0 L0,6 L9,3 z',fill:'#69cbd3'}));defs.append(marker);svg.append(defs);
 const pos={};estados.forEach((q,i)=>{const ang=-Math.PI/2+i*2*Math.PI/n;pos[q]={x:cx+radio*Math.cos(ang),y:cy+radio*Math.sin(ang)}});
 const edges=new Map();for(const t of a.transiciones||[]){const key=String(t.desde)+'|'+String(t.hacia);if(!edges.has(key))edges.set(key,[]);edges.get(key).push(String(t.simbolo)===''?'ε':String(t.simbolo));}
 for(const [key,labels] of edges){const [from,to]=key.split('|');const p=pos[from],q=pos[to];if(!p||!q)continue;let d,lx,ly;
 if(from===to){d=`M${p.x-13} ${p.y-20} C${p.x-70} ${p.y-100},${p.x+70} ${p.y-100},${p.x+13} ${p.y-20}`;lx=p.x;ly=p.y-80;}
 else {const dx=q.x-p.x,dy=q.y-p.y,dist=Math.hypot(dx,dy)||1,ux=dx/dist,uy=dy/dist;
 const sx=p.x+ux*nr,sy=p.y+uy*nr,ex=q.x-ux*(nr+4),ey=q.y-uy*(nr+4);
 const bend=edges.has(to+'|'+from)?18:0, mx=(sx+ex)/2-uy*bend,my=(sy+ey)/2+ux*bend;
 d=`M${sx} ${sy} Q${mx} ${my} ${ex} ${ey}`;lx=(sx+2*mx+ex)/4;ly=(sy+2*my+ey)/4-9;}
 svg.append(mk('path',{d,fill:'none',stroke:'#69cbd3','stroke-width':2,'marker-end':'url(#flecha-auto)'}));
 svg.append(mk('text',{x:lx,y:ly,'text-anchor':'middle',fill:'#f5cf84','font-size':14,'font-weight':'bold'},labels.join(', ')));
 }
 for(const q of estados){const p=pos[q];const accepting=a.finales.map(String).includes(q);
 svg.append(mk('circle',{cx:p.x,cy:p.y,r:nr,fill:q===String(a.inicial)?'#296a70':'#192d44',stroke:'#d3e8f0','stroke-width':2}));
 if(accepting)svg.append(mk('circle',{cx:p.x,cy:p.y,r:nr-5,fill:'none',stroke:'#d3e8f0','stroke-width':2}));
 svg.append(mk('text',{x:p.x,y:p.y+5,'text-anchor':'middle',fill:'#fff','font-size':14},'q'+q));}
 const ini=pos[String(a.inicial)];if(ini){const left=ini.x-nr;svg.append(mk('path',{d:`M${left-55} ${ini.y} H${left-6}`,stroke:'#f5cf84','stroke-width':2,'marker-end':'url(#flecha-auto)'}));}
 el.append(svg);
}
