import importlib.util
import os
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO = os.path.join(RAIZ, "publisher", "prontidao.py")
SPEC = importlib.util.spec_from_file_location("prontidao", CAMINHO)
prontidao = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prontidao)


class ProntidaoTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        with open(os.path.join(self.temp.name, "video.mp4"), "wb") as arquivo:
            arquivo.write(b"teste")
        self.post = {
            "type": "reel", "status": "pending", "media_file": "video.mp4",
            "caption": "Legenda", "pilar": "A PATROA MANDA",
            "auditoria": {"veredito": "SEM OBJECAO"},
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_peca_completa_passa_sem_data(self):
        erros, avisos = prontidao.validar(self.post, self.temp.name)
        self.assertEqual([], erros)
        self.assertTrue(avisos)

    def test_sem_auditoria_nao_vai_para_telegram(self):
        self.post.pop("auditoria")
        erros, _ = prontidao.validar(self.post, self.temp.name)
        self.assertIn("auditoria.veredito precisa ser SEM OBJECAO", erros)

    def test_midia_ausente_bloqueia(self):
        self.post["media_file"] = "nao-existe.mp4"
        erros, _ = prontidao.validar(self.post, self.temp.name)
        self.assertTrue(any("mídia não encontrada" in erro for erro in erros))
