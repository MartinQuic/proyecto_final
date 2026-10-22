import sqlite3
from pathlib import Path
DB=Path(__file__).with_name('reglas.db')
OPERADORES={'contiene','no_contiene','empieza_con','termina_con'}
def conectar():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def iniciar():
 with conectar() as c:
  c.execute('''CREATE TABLE IF NOT EXISTS reglas_personalizadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL,
    operador TEXT NOT NULL, patron TEXT NOT NULL, activo INTEGER NOT NULL DEFAULT 1)''')
def listar():
 iniciar()
 with conectar() as c:
  return [dict(r) | {'activo':bool(r['activo'])} for r in c.execute('SELECT * FROM reglas_personalizadas ORDER BY id')]
def crear(nombre,operador,patron):
 nombre=nombre.strip();patron=patron.strip()
 if not nombre or len(nombre)>100 or not patron or len(patron)>200 or operador not in OPERADORES:
  raise ValueError('Nombre, operador o patrón inválido')
 iniciar()
 with conectar() as c:
  cur=c.execute('INSERT INTO reglas_personalizadas(nombre,operador,patron) VALUES (?,?,?)',(nombre,operador,patron))
  return {'id':cur.lastrowid,'nombre':nombre,'operador':operador,'patron':patron,'activo':True}
def cambiar(regla_id,activo):
 iniciar()
 with conectar() as c:
  cur=c.execute('UPDATE reglas_personalizadas SET activo=? WHERE id=?',(int(activo),regla_id))
  if cur.rowcount==0:raise KeyError(regla_id)
 return {'id':regla_id,'activo':activo}
def eliminar(regla_id):
 iniciar()
 with conectar() as c:
  cur=c.execute('DELETE FROM reglas_personalizadas WHERE id=?',(regla_id,))
  if cur.rowcount==0:raise KeyError(regla_id)
 return {'eliminada':regla_id}
def evaluar(consulta):
 texto=consulta.casefold().strip();incumplidas=[]
 for r in listar():
  if not r['activo']:continue
  p=r['patron'].casefold()
  ok={'contiene':lambda:p in texto,'no_contiene':lambda:p not in texto,
      'empieza_con':lambda:texto.startswith(p),'termina_con':lambda:texto.endswith(p)}[r['operador']]()
  if not ok:incumplidas.append({'id':r['id'],'nombre':r['nombre'],'operador':r['operador'],'patron':r['patron']})
 return incumplidas