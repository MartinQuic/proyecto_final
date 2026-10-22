import re

# Subconjunto pedagógico de SELECT. No ejecuta SQL ni utiliza eval.
TOKENS = re.compile(r"'(?:''|[^'])*'|\d+(?:\.\d+)?|>=|<=|!=|<>|[(),;.*=<>]|[A-Za-z_][A-Za-z_0-9]*|\S")
REGLAS = [
 ('SQL_01','SELECT básico'),('SQL_02','Columnas múltiples'),('SQL_03','Comodín *'),
 ('SQL_04','WHERE y comparación'),('SQL_05','AND / OR'),('SQL_06','ORDER BY'),
 ('SQL_07','GROUP BY'),('SQL_08','HAVING'),('SQL_09','INNER JOIN'),('SQL_10','LIMIT')
]
COMPARADORES={'=','>','<','>=','<=','!=','<>'}
class ErrorSQL(ValueError):
 def __init__(self,msg,codigo='SINTAXIS_SQL'):
  super().__init__(msg);self.codigo=codigo

def validar(sql,activas):
 try:
  tokens=TOKENS.findall(sql.strip()); t=[x.upper() if not x.startswith("'") else x for x in tokens]
  i=0; usadas={'SQL_01'}
  def peek(): return t[i] if i<len(t) else None
  def take(value=None):
   nonlocal i
   if i>=len(t) or (value is not None and t[i]!=value):
    raise ErrorSQL('Se esperaba '+(value or 'un token'))
   out=t[i];i+=1;return out
  def identifier():
   first=peek()
   if first is None or not re.fullmatch(r'[A-Z_][A-Z_0-9]*',first) or first in {'SELECT','FROM','WHERE','JOIN','INNER','ON','ORDER','GROUP','BY','HAVING','LIMIT','AND','OR'}:
    raise ErrorSQL('Se esperaba un identificador')
   take()
   if peek()=='.': take('.');identifier()
  def column():
   if peek()=='*': usadas.add('SQL_03');take('*')
   else: identifier()
  def value():
   if peek() is None: raise ErrorSQL('Falta valor')
   if re.fullmatch(r"'(?:''|[^'])*'|\d+(?:\.\d+)?",peek()): take()
   else: identifier()
  def condition():
   identifier(); op=take()
   if op not in COMPARADORES: raise ErrorSQL('Se esperaba operador de comparación')
   value()
   while peek() in ('AND','OR'):
    usadas.add('SQL_05');take();identifier();op=take()
    if op not in COMPARADORES:raise ErrorSQL('Comparador inválido')
    value()
  take('SELECT');column()
  while peek()==',': usadas.add('SQL_02');take(',');column()
  take('FROM');identifier()
  if peek()=='INNER':
   usadas.add('SQL_09');take('INNER');take('JOIN');identifier();take('ON');identifier();take('=');identifier()
  if peek()=='WHERE': usadas.add('SQL_04');take();condition()
  if peek()=='GROUP':
   usadas.add('SQL_07');take();take('BY');identifier()
   while peek()==',': take();identifier()
  if peek()=='HAVING':
   usadas.add('SQL_08')
   if 'SQL_07' not in usadas: raise ErrorSQL('HAVING requiere GROUP BY')
   take();identifier();op=take()
   if op not in COMPARADORES:raise ErrorSQL('Comparador HAVING inválido')
   value()
  if peek()=='ORDER':
   usadas.add('SQL_06');take();take('BY');identifier()
   if peek() in ('ASC','DESC'):take()
  if peek()=='LIMIT':
   usadas.add('SQL_10');take();n=take()
   if not re.fullmatch(r'\d+',n):raise ErrorSQL('LIMIT requiere un entero')
  if peek()==';':take()
  if peek() is not None:raise ErrorSQL('Token inesperado: '+str(peek()))
  desactivadas=sorted(usadas-set(activas))
  if desactivadas:raise ErrorSQL('Reglas inactivas: '+', '.join(desactivadas),'REGLA_INACTIVA')
  return {'valido':True,'codigo':'OK','mensaje':'Consulta válida para el subconjunto SQL definido','reglas_usadas':sorted(usadas)}
 except ErrorSQL as ex:
  return {'valido':False,'codigo':ex.codigo,'mensaje':str(ex),'reglas_usadas':sorted(locals().get('usadas',set()))}
