"""Confere as dependências locais do Estúdio sem chamar IA nem alterar arquivos."""
import importlib.util
import sys

PACOTES = {"Pillow": "PIL", "imageio-ffmpeg": "imageio_ffmpeg", "ultralytics": "ultralytics", "pillow-heif": "pillow_heif"}

faltam = [nome for nome, modulo in PACOTES.items() if importlib.util.find_spec(modulo) is None]
if faltam:
    print("[AMBIENTE][FALHA] faltam: " + ", ".join(faltam))
    print("Instale com: python -m pip install -r requirements-studio.txt")
    sys.exit(1)
print("[AMBIENTE][OK] Estúdio pronto.")
