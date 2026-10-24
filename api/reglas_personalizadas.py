from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from database import personalizadas as p
router=APIRouter(prefix='/api/configuracion/personalizadas',tags=['Reglas personalizadas'])
class Nueva(BaseModel):
 nombre:str=Field(min_length=1,max_length=100)
 operador:str
 patron:str=Field(min_length=1,max_length=200)
class Estado(BaseModel):
 activo:bool
@router.get('')
def listar():return p.listar()
@router.post('',status_code=201)
def crear(data:Nueva):
 try:return p.crear(data.nombre,data.operador,data.patron)
 except ValueError as e:raise HTTPException(status_code=422,detail=str(e))
@router.patch('/{id}')
def cambiar(id:int,data:Estado):
 try:return p.cambiar(id,data.activo)
 except KeyError:raise HTTPException(status_code=404,detail='Regla no encontrada')
@router.delete('/{id}')
def eliminar(id:int):
 try:return p.eliminar(id)
 except KeyError:raise HTTPException(status_code=404,detail='Regla no encontrada')
