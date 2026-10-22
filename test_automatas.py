"""INTEGRANTE 6. Ejecutar con: python -m unittest discover -s tests -v"""
import unittest
from core.lexico import leer_alfabeto
from core.regex_parser import convertir_postfija
from core.thompson import construir_afn
from core.subconjuntos import convertir_afd
from core.minimizacion import minimizar
from core.simulador import simular
from core.visualizador import generar_dot

def compilar(expresion, alfabeto={'0','1'}):
    return minimizar(convertir_afd(construir_afn(convertir_postfija(expresion,alfabeto),alfabeto)))

class PruebasAutomatas(unittest.TestCase):
    def test_alfabeto(self):
        self.assertEqual(leer_alfabeto('{0,1}'),{'0','1'})
    def test_regex_y_cadena(self):
        afd=compilar('(0|1)*01')
        for cadena in ['01','001','1101']:
            self.assertTrue(simular(afd,cadena)[0],cadena)
        for cadena in ['','0','10','111']:
            self.assertFalse(simular(afd,cadena)[0],cadena)
    def test_estrella_vacio(self):
        afd=compilar('0*')
        self.assertTrue(simular(afd,'')[0]);self.assertTrue(simular(afd,'000')[0]);self.assertFalse(simular(afd,'1')[0])
    def test_union(self):
        afd=compilar('0|1')
        self.assertTrue(simular(afd,'0')[0]);self.assertTrue(simular(afd,'1')[0]);self.assertFalse(simular(afd,'01')[0])
    def test_epsilon(self):
        afd=compilar('ε|0')
        self.assertTrue(simular(afd,'')[0]);self.assertTrue(simular(afd,'0')[0])
    def test_errores(self):
        for regex in ['(0|','*0','0||1','(0','0)']:
            with self.subTest(regex=regex),self.assertRaises(ValueError): compilar(regex)
    def test_alfabeto_cadena(self):
        with self.assertRaises(ValueError): simular(compilar('0'),'A')
    def test_minimizar_equivalente(self):
        regex='(0|1)*01'; a={'0','1'}
        afn=construir_afn(convertir_postfija(regex,a),a)
        original=convertir_afd(afn); reducido=minimizar(original)
        self.assertLessEqual(len(reducido.estados),len(original.estados))
        for n in range(6):
            for numero in range(2**n):
                cadena=format(numero,f'0{n}b') if n else ''
                self.assertEqual(simular(original,cadena)[0],simular(reducido,cadena)[0])
        self.assertIn('digraph',generar_dot(reducido))

if __name__=='__main__': unittest.main()
