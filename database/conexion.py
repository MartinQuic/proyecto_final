import sqlite3
from pathlib import Path
from sql.validador import REGLAS
DB=Path(__file__).with_name('reglas.db')
def conectar():
 con=sqlite3.connect(DB);con.row_factory=sqlite3.Row;return con
def iniciar():
 with conectar() as con:
  con.execute('CREATE TABLE IF NOT EXISTS reglas (id TEXT PRIMARY KEY, nombre TEXT NOT NULL, activo INTEGER NOT NULL DEFAULT 1)')
  con.executemany('INSERT OR IGNORE INTO reglas(id,nombre,activo) VALUES (?,?,1)',REGLAS)
def listar():
 iniciar()
 with conectar() as con:
  return [dict(id=r['id'],nombre=r['nombre'],activo=bool(r['activo'])) for r in con.execute('SELECT * FROM reglas ORDER BY id')]
def cambiar(id,activo):
 iniciar()
 with conectar() as con:
  r=con.execute('UPDATE reglas SET activo=? WHERE id=?',(int(activo),id))
  if r.rowcount==0:raise KeyError(id)
 return {'id':id,'activo':activo}
