import unittest
from sql.validador import validar

ACTIVAS={f'SQL_{i:02d}' for i in range(1,11)}
class TestSQLMejorado(unittest.TestCase):
 def test_alias_invalidos(self):
  r=validar('select * from usuarios inner join ciudad on u.id = c.id where usuario=15;', ACTIVAS)
  self.assertFalse(r['valido']);self.assertEqual(r['codigo'],'ALIAS_NO_DECLARADO')
  self.assertEqual((r['linea'],r['columna']),(1,45))
 def test_alias_declarados(self):
  r=validar('select * from usuarios u inner join ciudad c on u.id = c.id where usuario=15;', ACTIVAS)
  self.assertTrue(r['valido'])
 def test_alias_con_as(self):
  self.assertTrue(validar('SELECT u.id FROM usuarios AS u;',ACTIVAS)['valido'])
 def test_varias_consultas(self):
  r=validar('SELECT * FROM usuarios;\nSELECT nombre FROM personas;\nSELECT * FROM x WHERE edad > ;',ACTIVAS)
  self.assertEqual((r['total'],r['correctas'],r['errores']),(3,2,1))
  self.assertEqual(r['sentencias'][2]['linea'],3)
 def test_semicolon_en_cadena(self):
  self.assertTrue(validar("SELECT nombre FROM usuarios WHERE nombre = 'a;b';",ACTIVAS)['valido'])
 def test_regla_inactiva(self):
  r=validar('SELECT * FROM t ORDER BY id;', ACTIVAS-{'SQL_06'})
  self.assertEqual(r['codigo'],'REGLA_INACTIVA')
if __name__=='__main__':unittest.main()
