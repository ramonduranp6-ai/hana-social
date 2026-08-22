import importlib.util
import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO = os.path.join(RAIZ, "publisher", "cobertura_fila.py")
SPEC = importlib.util.spec_from_file_location("cobertura_fila", CAMINHO)
cobertura = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cobertura)


class CoberturaFilaTest(unittest.TestCase):
    def test_conta_apenas_aprovados_futuros(self):
        with tempfile.TemporaryDirectory() as pasta:
            anterior = cobertura.FILA
            cobertura.FILA = pasta
            try:
                for nome, status, data in [
                    ("a", "approved", "2026-08-23T14:00:00Z"),
                    ("b", "pending", "2026-08-24T14:00:00Z"),
                ]:
                    destino = os.path.join(pasta, nome)
                    os.mkdir(destino)
                    with open(os.path.join(destino, "post.json"), "w", encoding="utf-8") as arquivo:
                        json.dump({"status": status, "scheduled_for": data}, arquivo)
                dados = cobertura.resumo(datetime(2026, 8, 22, tzinfo=timezone.utc))
                self.assertEqual(1, len(dados["posts"]))
                self.assertIn("1 dia(s)", cobertura.mensagem(dados))
            finally:
                cobertura.FILA = anterior
