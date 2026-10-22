import unittest
from sql.validador import validar
ACTIVAS={f'SQL_{i:02}' for i in range(1,11)}
class PruebasSQL(unittest.TestCase):
 def test_select(self):self.assertTrue(validar('SELECT nombre FROM empleados;',ACTIVAS)['valido'])
 def test_where(self):self.assertTrue(validar('SELECT nombre FROM empleados WHERE edad >= 18;',ACTIVAS)['valido'])
 def test_regla_inactiva(self):
  r=validar('SELECT nombre FROM empleados ORDER BY nombre;',ACTIVAS-{'SQL_06'})
  self.assertFalse(r['valido']);self.assertEqual(r['codigo'],'REGLA_INACTIVA')
 def test_error(self):self.assertFalse(validar('DELETE FROM empleados;',ACTIVAS)['valido'])
if __name__=='__main__':unittest.main()
