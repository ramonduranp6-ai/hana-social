import importlib.util
import os
import sys
import types
import unittest

sys.modules.setdefault("requests", types.SimpleNamespace())
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = importlib.util.spec_from_file_location("ig_api", os.path.join(RAIZ, "publisher", "ig_api.py"))
ig_api = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ig_api)


class IGApiTest(unittest.TestCase):
    def test_salva_container_antes_de_publicar(self):
        chamadas = []
        ig_api.create_image_container = lambda *_: "container-123"
        ig_api.wait_until_ready = lambda *_: chamadas.append("esperou")
        ig_api.publish_container = lambda *_: chamadas.append("publicou") or "post-456"
        resultado = ig_api.publish("user", "token", "image", "url", "legenda", on_container_created=chamadas.append)
        self.assertEqual("post-456", resultado)
        self.assertEqual(["container-123", "esperou", "publicou"], chamadas)
