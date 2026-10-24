import unittest
from sql.afd_lexico import tokenizar, reconocer_palabra_numero, TRANSICIONES, ACEPTACION, FalloLexico
from sql.validador import validar

ACTIVAS = {f'SQL_{i:02}' for i in range(1, 11)}

class TestAFDSQLIntegrado(unittest.TestCase):
    def test_afd_real_transiciones(self):
        self.assertEqual(TRANSICIONES['q_id']['DIGITO'], 'q_id')
        self.assertEqual(ACEPTACION['q_decimal'], 'NUM')
        self.assertEqual(reconocer_palabra_numero('nombre15', 0).kind, 'ID')

    def test_tokens_con_posiciones(self):
        t = tokenizar('SELECT col1 FROM t WHERE precio >= 12.50;')
        self.assertEqual([x.value for x in t[:3]], ['SELECT','col1','FROM'])
        self.assertEqual([x.kind for x in t if x.value in ('col1','12.50')], ['ID','NUM'])
        self.assertIn('>=', [x.value for x in t])

    def test_sql_join_y_filtros(self):
        sql = 'SELECT e.nombre, d.nombre FROM empleados e LEFT JOIN departamentos d ON e.dep_id = d.id WHERE e.salario > 2000 ORDER BY e.nombre ASC;'
        self.assertTrue(validar(sql, ACTIVAS)['valido'])

    def test_sql_errores_join(self):
        sql = 'SELECT * FROM usuarios U INNER JOIN ciudad C ON id = id;'
        r = validar(sql, ACTIVAS)
        self.assertFalse(r['valido'])
        self.assertEqual(r['codigo'], 'COLUMNA_SIN_CALIFICAR')

    def test_multiples_con_cadena_punto_y_coma(self):
        r = validar("SELECT * FROM t WHERE nombre = 'a;b'; SELECT id FROM t;", ACTIVAS)
        self.assertEqual(r['total'], 2)
        self.assertTrue(r['valido'])

    def test_comentarios(self):
        r = validar('/* encabezado */ SELECT id FROM t -- comentario\n;', ACTIVAS)
        self.assertTrue(r['valido'])

    def test_error_lexico_posicion(self):
        r = validar('SELECT id FROM t WHERE nombre = @;', ACTIVAS)
        self.assertFalse(r['valido'])
        self.assertEqual(r['codigo'], 'LEXICO_SQL')
        self.assertEqual(r['columna'], 33)

    def test_cadena_sin_cerrar(self):
        r = validar("SELECT * FROM t WHERE n = 'sin cerrar", ACTIVAS)
        self.assertFalse(r['valido'])
        self.assertEqual(r['codigo'], 'LEXICO_SQL')

if __name__ == '__main__': unittest.main()
