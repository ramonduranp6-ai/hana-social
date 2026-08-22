import importlib.util
import os
import sys
import types
import unittest

sys.modules.setdefault("requests", types.SimpleNamespace())
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = importlib.util.spec_from_file_location("recepcionista", os.path.join(RAIZ, "publisher", "recepcionista.py"))
recepcionista = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recepcionista)


class RecepcionistaTest(unittest.TestCase):
    def test_ajuda_eh_resolvida_sem_ia(self):
        self.assertIn("fila", recepcionista.resposta_local("ajuda"))

    def test_pedido_de_acao_nao_e_respondido_localmente(self):
        self.assertIsNone(recepcionista.resposta_local("publique o próximo post"))
