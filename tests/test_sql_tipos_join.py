import unittest
from sql.validador import validar

ACTIVAS = {f'SQL_{i:02}' for i in range(1, 11)}

class TestTiposJoin(unittest.TestCase):
    def probar(self, consulta, valido, codigo=None):
        r = validar(consulta, ACTIVAS)
        self.assertEqual(r['valido'], valido, (consulta, r))
        if codigo:
            self.assertEqual(r['codigo'], codigo, (consulta, r))
        return r

    def test_join_permitidos(self):
        for tipo in ('JOIN', 'INNER JOIN', 'LEFT JOIN', 'LEFT OUTER JOIN',
                     'RIGHT JOIN', 'RIGHT OUTER JOIN', 'FULL JOIN', 'FULL OUTER JOIN'):
            with self.subTest(tipo=tipo):
                self.probar(f'SELECT e.nombre, d.nombre FROM empleados e {tipo} departamentos d ON e.dep_id = d.id WHERE e.salario > 2000 ORDER BY e.nombre ASC;', True)

    def test_alias_no_declarado(self):
        self.probar('SELECT * FROM empleados e LEFT JOIN departamentos d ON x.id = d.id;', False, 'ALIAS_NO_DECLARADO')

    def test_columnas_sin_calificar(self):
        self.probar('SELECT * FROM empleados e LEFT JOIN departamentos d ON id = id;', False, 'COLUMNA_SIN_CALIFICAR')
        self.probar('SELECT * FROM empleados e RIGHT JOIN departamentos d ON e.id = id;', False, 'COLUMNA_SIN_CALIFICAR')

    def test_multiples_sentencias(self):
        r = self.probar('SELECT * FROM a x LEFT JOIN b y ON x.id=y.id; SELECT * FROM a x FULL JOIN b y ON id=y.id;', False)
        self.assertEqual(r['total'], 2)
        self.assertEqual(r['correctas'], 1)

    def test_outer_sin_tipo(self):
        self.probar('SELECT * FROM a x OUTER JOIN b y ON x.id=y.id;', False)

if __name__ == '__main__':
    unittest.main()
