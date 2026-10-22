from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from api.automatas import procesar
from database.conexion import listar,cambiar,iniciar
from sql.validador import validar

ROOT=Path(__file__).resolve().parent
app=FastAPI(title='Proyecto Final Autómatas + SQL')
app.mount('/static',StaticFiles(directory=str(ROOT/'web')),name='static')
@app.on_event('startup')
def startup(): iniciar()
@app.get('/')
def inicio():return FileResponse(ROOT/'web'/'index.html')
class EntradaAutomata(BaseModel):
 alfabeto:str
 regex:str
 cadena:str=''
class EntradaSQL(BaseModel):
 consulta:str
class EstadoRegla(BaseModel):
 activo:bool
@app.post('/api/automatas/generar')
def automatas(data:EntradaAutomata):
 try:return procesar(data.alfabeto,data.regex,data.cadena)
 except (ValueError,TypeError) as e:raise HTTPException(status_code=422,detail=str(e))
@app.get('/api/configuracion/reglas')
def reglas():return listar()
@app.patch('/api/configuracion/reglas/{id}')
def actualizar(id:str,data:EstadoRegla):
 try:return cambiar(id,data.activo)
 except KeyError:raise HTTPException(status_code=404,detail='Regla no encontrada')
@app.post('/api/sql/validar')
def sql(data:EntradaSQL):
 activas={x['id'] for x in listar() if x['activo']}
 return validar(data.consulta,activas)
