import unittest
from main_web import app

class RutasPersonalizadas(unittest.TestCase):
    def test_registro_rutas(self):
        paths = {
    r.path
    for r in app.routes
    if hasattr(r, "path")
}
        self.assertIn('/api/configuracion/personalizadas', paths)
        self.assertIn('/api/configuracion/personalizadas/{id}', paths)
