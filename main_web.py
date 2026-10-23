from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from api.automatas import procesar
from database.conexion import listar,cambiar,iniciar
from sql.validador import validar
from api.reglas_personalizadas import router as personalizadas_router
from database.personalizadas import evaluar as evaluar_personalizadas, iniciar as iniciar_personalizadas

ROOT = Path(__file__).resolve().parent

app = FastAPI(title='Proyecto Final Autómatas + SQL')

# Registrar endpoints personalizados
# Registrar las rutas personalizadas directamente
for ruta in personalizadas_router.routes:
    app.add_api_route(
        path=ruta.path,
        endpoint=ruta.endpoint,
        methods=ruta.methods,
        name=ruta.name,
    )

# Servir los archivos del frontend
app.mount(
    '/static',
    StaticFiles(directory=str(ROOT / 'web')),
    name='static'
)

# Verificación temporal
print("RUTAS PERSONALIZADAS REGISTRADAS:")
for ruta in app.routes:
    if 'personalizadas' in getattr(ruta, 'path', ''):
        print(ruta.path, getattr(ruta, 'methods', None))
@app.on_event('startup')
def startup():
 iniciar()
 iniciar_personalizadas()
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
def sql(data: EntradaSQL):
    activas = {x['id'] for x in listar() if x['activo']}
    resultado = validar(data.consulta, activas)
    # Evaluar validadores personalizados por sentencia, no sobre todo el lote.
    for sentencia in resultado.get('sentencias', []):
        if not sentencia['valido']:
            continue
        incumplidas = evaluar_personalizadas(sentencia['consulta'])
        if incumplidas:
            sentencia.update(valido=False, codigo='REGLA_PERSONALIZADA',
                             mensaje='No cumple validadores personalizados',
                             incumplidas=incumplidas,
                             linea=sentencia['inicio']['linea'],
                             columna=sentencia['inicio']['columna'],
                             posicion=sentencia['inicio']['posicion'])
    sentencias = resultado.get('sentencias', [])
    if sentencias:
        total = len(sentencias)
        correctas = sum(s['valido'] for s in sentencias)
        resultado.update(valido=correctas == total, total=total,
                         correctas=correctas, errores=total-correctas)
        if total == 1:
            s = sentencias[0]
            resultado.update(codigo=s['codigo'], mensaje=s['mensaje'],
                             reglas_usadas=s.get('reglas_usadas', []))
            if not s['valido']:
                for k in ('linea', 'columna', 'posicion'):
                    resultado[k] = s[k]
        else:
            resultado.update(codigo='OK' if correctas == total else 'ERROR_SQL',
                             mensaje=f'{correctas} de {total} consultas válidas')
    return resultado
