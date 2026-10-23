from core.lexico import leer_alfabeto
from core.regex_parser import convertir_postfija
from core.thompson import construir_afn
from core.subconjuntos import convertir_afd
from core.minimizacion import minimizar
from core.simulador import simular
from core.visualizador import generar_dot

def serializar(a):
 return {'estados':sorted(a.estados),'alfabeto':sorted(a.alfabeto),'inicial':a.inicial,
         'finales':sorted(a.finales),'transiciones':[{'desde':o,'simbolo':s,'hacia':d}
         for (o,s),ds in sorted(a.transiciones.items()) for d in sorted(ds)]}
def procesar(alfabeto,regex,cadena=''):
 sigma=leer_alfabeto(alfabeto)
 postfija=convertir_postfija(regex,sigma)
 afn=construir_afn(postfija,sigma);afd=convertir_afd(afn);minimo=minimizar(afd)
 aceptada,pasos=simular(minimo,cadena)
 return {'aceptada':aceptada,'pasos':pasos,'afn':serializar(afn),'afd':serializar(afd),
         'minimo':serializar(minimo),'dot':generar_dot(minimo,'AFD mínimo')}
