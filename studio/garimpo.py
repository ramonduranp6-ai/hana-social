# -*- coding: utf-8 -*-
"""
Garimpo do rolo de câmera — acha foto/vídeo da Hana escondidos no iCloud.

O PROBLEMA: o acervo do projeto esvaziou (os 12 vídeos brutos foram todos
reprovados pelo auditor) e a fila acaba em 10/08. Mas o rolo de câmera do
Ramón, sincronizado em `~\\iCloudPhotos\\Photos`, tem ~34 mil arquivos sem
organização nenhuma — o `DECISOES.md` registrava essa pasta como BECO SEM
SAÍDA porque ninguém sabia separar "tem a Hana" de "não tem". Este robô
resolve isso com um detector de objetos LOCAL (YOLOv8n, ultralytics) que
reconhece as classes 'dog' e 'person' — fica só o que tem cachorro e NÃO tem
gente, a mesma régua da fronteira com o projeto Canecas.

REGRA DE OURO — NENHUMA FOTO SAI DA MÁQUINA. A inspeção roda 100% local. O
YOLOv8n é baixado UMA VEZ do repositório oficial da Ultralytics no GitHub —
são ~6 MB de PESOS do modelo, não fotos do Ramón. Nenhuma imagem é enviada a
Gemini, ChatGPT, DeepSeek, Grok ou qualquer API. Não existe nenhum
requests.post/put neste arquivo — só leitura local e, no máximo, o download
único do modelo (checar com 'grep -E "requests\\.(post|put)" garimpo.py',
que tem que dar zero, igual ao padrão de robô 100% leitura já usado no
projeto).

LIMITE HONESTO, que precisa estar sempre junto do resultado: o detector
reconhece "isto é um cachorro", NÃO "isto é A HANA" — não existe
reconhecimento individual de cachorro aqui. Se o rolo tiver foto de cachorro
de outra pessoa (amigo, canil, rua), ela passa no filtro do mesmo jeito. Todo
resultado deste robô é "cachorro sem gente no quadro", nunca "é a Hana"
garantido — quem confirma que é ela é o Ramón, olhando o ranking.

PEGADINHA JÁ PAGA (achada construindo este robô, 01/08/2026): rodar python.exe
a partir do Git Bash/MSYS com um usuário de nome acentuado (Ramón França)
corrompe `os.environ`/`os.path.expanduser("~")` — a string vem com caracteres
trocados por `�` e os caminhos deixam de existir. Isso NÃO acontece quando o
robô roda do jeito normal (cmd/Task Scheduler/duplo-clique). Mesmo assim, para
não depender do shell de quem chama, a pasta pessoal é resolvida direto pela
API do Windows (`SHGetFolderPathW`, ver `_pasta_pessoal()`), nunca por
variável de ambiente.

PEGADINHA Nº 2 — A PASTA `iCloudPhotos\\Photos` É SINCRONIZADA SOB DEMANDA
("otimizar armazenamento" do app iCloud para Windows): a maioria dos 34 mil
arquivos são "placeholders" que precisam ser BAIXADOS DA NUVEM na hora de
abrir. Medido em amostra real (01/08/2026, 10 arquivos, rede da casa): abrir
+ decodificar + rodar o detector custou em média **9,3 segundos por arquivo**
(de 3s a 22s) — a maior parte é o tempo de abrir/baixar, não o detector em si
(esse fica por volta de 0,3 a 2,7s). Nessa velocidade, os 34.431 arquivos
INTEIROS levariam perto de **89 HORAS** rodando sem parar — inviável numa
sessão só. Por isso este robô É RETOMÁVEL de verdade (grava o progresso a
cada poucos arquivos) e tem `--minutos` para rodar em pedaços, e usa algumas
threads em paralelo (a espera de download não usa CPU, então rodar 3 arquivos
"ao mesmo tempo" ajuda de verdade, mesmo em CPU só).

O FUNIL, do mais barato pro mais caro (regra do pedido: descartar barato
antes de abrir o arquivo):
  1. Extensão conhecida (foto/vídeo do iPhone) — o resto nem entra na conta.
  2. Tamanho mínimo (15 KB) — descarta ícone/thumbnail/arquivo quebrado.
  3. .PNG é tratado como PRINT DE TELA e descartado SEM ABRIR — foto de
     câmera do iPhone é sempre .HEIC ou .JPG; print é sempre .PNG. (Se um dia
     isso se mostrar errado — por exemplo o Ramón salvar foto editada em PNG
     — é só tirar esta regra; o custo de rever é baixo, o de abrir 723 PNGs à
     toa não é.)
  4. Abre de verdade (PIL + pillow_heif p/ HEIC; ffmpeg extrai 5 frames de
     vídeo) e descarta resolução baixíssima (< 300x300 — sticker/emoji salvo).
  5. Roda o YOLOv8n (CPU, offline): tem 'person' em QUALQUER frame amostrado?
     reprova. Não tem 'dog' em NENHUM frame? reprova. Passou nos dois: OK.

RANKING, não despejo (pedido explícito — centenas de fotos ninguém olha):
  score = 0,35 × (área do cachorro no quadro, capado em 50%)
        + 0,25 × (nitidez — variância do Laplaciano, capada em 300)
        + 0,15 × (resolução em megapixels, capada em 8 MP)
        + 0,15 × (confiança do detector)
        + 0,10 × bônus se for vídeo (o pedido do projeto prioriza vídeo real)
  Os 30 melhores vão para uma subpasta separada, clara, o resto fica junto
  mas sem se misturar com o que ele mesmo sobe.

Uso:
    python studio/garimpo.py --amostra 20      # teste rápido, mede o tempo real
    python studio/garimpo.py --minutos 30      # roda até 30 min e para (retomável)
    python studio/garimpo.py --relatorio       # só regera RELATORIO.md e o top 30
    python studio/garimpo.py --resetar-estado  # apaga o progresso (recomeça do zero)
"""

import argparse
import ctypes
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from ctypes import wintypes

# Console do Windows quebra com emoji/acento se não forçar UTF-8 — cuidado
# pago várias vezes neste projeto. Nunca io.TextIOWrapper.
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FOTOS = os.path.join(RAIZ, "Fotos da Hana")
SAIDA_BASE = os.path.join(FOTOS, "01 - brutas (suba aqui)", "garimpo")
SAIDA_TOP30 = os.path.join(SAIDA_BASE, "melhores-30")
ESTADO_ARQ = os.path.join(AQUI, ".garimpo_estado.json")
RELATORIO_ARQ = os.path.join(SAIDA_BASE, "RELATORIO.md")
MODELO_ARQ = os.path.join(AQUI, ".garimpo_modelo", "yolov8n.pt")

IMG_EXT = {".jpg", ".jpeg", ".heic", ".webp"}  # .png sai à parte (regra 3 do funil)
VID_EXT = {".mp4", ".mov", ".m4v"}
TAMANHO_MINIMO = 15 * 1024          # 15 KB
RES_MINIMA = 300 * 300              # 300x300 px
CONF_DOG = 0.40                     # confiança mínima pra aceitar 'dog'
CONF_PESSOA = 0.30                  # mais baixa de propósito: prefere rejeitar
                                     # foto duvidosa a deixar pessoa passar
N_FRAMES_VIDEO = 5
GB = 1024 ** 3
DISCO_MINIMO_LIVRE = 10 * GB        # some para arquivos entrarem, robô pausa antes de encher o disco


def _pasta_pessoal():
    """
    Caminho da pasta do usuário (C:\\Users\\<nome>) direto pela API do
    Windows — NUNCA por variável de ambiente/os.path.expanduser. Motivo:
    achado construindo este robô (01/08/2026) — rodando python.exe a partir
    do Git Bash com usuário de nome acentuado, os.environ/expanduser
    devolvem a string CORROMPIDA (caracteres trocados por replacement char),
    e toda conta de caminho que depender disso quebra silenciosamente. A API
    do shell devolve a string certa não importa qual shell chamou o python.
    """
    CSIDL_PROFILE = 40
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PROFILE, 0, 0, buf)
    return buf.value


FONTE = os.path.join(_pasta_pessoal(), "iCloudPhotos", "Photos")


# ---------------------------------------------------------------------------
# Estado (retomável) — grava o mínimo necessário pra não reprocessar arquivo
# já visto. Por privacidade (regra do pedido: nunca registrar em log nome de
# arquivo que não passou no filtro), o que REPROVOU vira só um nome marcado
# "visto" — o MOTIVO da reprovação fica só em contagem agregada, nunca
# amarrado ao nome do arquivo. Só o que APROVOU carrega detalhe (é o que vai
# para o relatório do Ramón de qualquer forma).
# ---------------------------------------------------------------------------

def estado_vazio():
    return {
        "visto": [],           # nomes já processados (aprovados ou não) — só pra não repetir
        "aprovados": {},        # nome -> {score, componentes, tipo, copiado}
        "motivos_reprovacao": {},  # motivo -> contagem (sem nome de arquivo)
        "erros": 0,
        "arquivos_varridos": 0,
        "segundos_gastos": 0.0,
        "ultima_execucao": None,
    }


def carregar_estado():
    if os.path.isfile(ESTADO_ARQ):
        try:
            with open(ESTADO_ARQ, encoding="utf-8") as f:
                dados = json.load(f)
            dados.setdefault("visto", [])
            dados.setdefault("aprovados", {})
            dados.setdefault("motivos_reprovacao", {})
            dados.setdefault("erros", 0)
            dados.setdefault("arquivos_varridos", 0)
            dados.setdefault("segundos_gastos", 0.0)
            return dados
        except Exception as exc:  # noqa: BLE001 — estado corrompido nunca trava o robô
            print(f"[aviso] estado corrompido, recomeçando do zero ({str(exc)[:100]})")
    return estado_vazio()


def salvar_estado_atomico(estado):
    """tmp + os.replace — igual ao padrão salvar_json_atomico já usado no
    projeto (placar_hipoteses.py, margem_semanal.py): nunca deixa o arquivo
    de estado pela metade se o robô cair no meio da gravação."""
    estado["ultima_execucao"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    os.makedirs(os.path.dirname(ESTADO_ARQ), exist_ok=True)
    tmp = ESTADO_ARQ + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ESTADO_ARQ)


# ---------------------------------------------------------------------------
# Funil barato — nenhuma destas checagens abre o conteúdo do arquivo.
# ---------------------------------------------------------------------------

def descarte_barato(nome, caminho):
    """Devolve (passa: bool, motivo: str|None, tipo: 'imagem'|'video'|None)."""
    ext = os.path.splitext(nome)[1].lower()
    if ext == ".png":
        return False, "print de tela (.png)", None
    if ext in IMG_EXT:
        tipo = "imagem"
    elif ext in VID_EXT:
        tipo = "video"
    else:
        return False, "extensão não é foto/vídeo do iPhone", None
    try:
        tamanho = os.path.getsize(caminho)
    except OSError as exc:
        return False, f"erro ao ler tamanho: {exc}", None
    if tamanho < TAMANHO_MINIMO:
        return False, "arquivo pequeno demais (ícone/thumbnail)", None
    return True, None, tipo


def _ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def abrir_imagem(caminho):
    """PIL + pillow_heif (registrado no import do módulo) — devolve RGB."""
    from PIL import Image
    with Image.open(caminho) as im:
        return im.convert("RGB")


def extrair_frames_video(caminho, tmpdir):
    """
    5 frames amostrados a 1 frame por segundo (primeiros ~5s do clipe) — os
    vídeos do iPhone deste projeto ficam na casa de 10-15s (ver skill), então
    isto cobre boa parte do clipe. LIMITE DECLARADO: não cobre o clipe
    inteiro; pessoa fora dos 5 frames amostrados não é pega. Mesma técnica
    (ffmpeg select+mod) já usada no projeto pra extrair frame de auditoria.
    """
    from PIL import Image
    saida_padrao = os.path.join(tmpdir, "f%d.jpg")
    cmd = [_ffmpeg(), "-y", "-i", caminho, "-vf", "select='not(mod(n\\,30))'",
           "-vsync", "vfr", "-frames:v", str(N_FRAMES_VIDEO), saida_padrao]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="ignore", timeout=90)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou: {r.stderr[-200:]}")
    frames = []
    for nome_frame in sorted(os.listdir(tmpdir)):
        caminho_frame = os.path.join(tmpdir, nome_frame)
        frames.append(Image.open(caminho_frame).convert("RGB"))
    if not frames:
        raise RuntimeError("ffmpeg não extraiu nenhum frame")
    return frames


def nitidez(img_pil):
    """Variância do Laplaciano — métrica clássica de foco: imagem nítida tem
    bordas fortes (variância alta), imagem borrada é 'lisa' (variância baixa).
    cv2 já é dependência do ultralytics, então está sempre disponível aqui."""
    import cv2
    import numpy as np
    cinza = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2GRAY)
    return float(cv2.Laplacian(cinza, cv2.CV_64F).var())


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------

class _ModeloPorThread:
    """threading.local() dá 1 instância de YOLO por worker — evita qualquer
    dúvida sobre thread-safety de rodar predict() no mesmo objeto de 2
    threads ao mesmo tempo (o pytorch não garante isso oficialmente)."""

    def __init__(self):
        self._local = None

    def get(self):
        import threading
        if not hasattr(self, "_storage"):
            self._storage = threading.local()
        if not hasattr(self._storage, "modelo"):
            from ultralytics import YOLO
            os.makedirs(os.path.dirname(MODELO_ARQ), exist_ok=True)
            self._storage.modelo = YOLO(MODELO_ARQ)
        return self._storage.modelo


_FABRICA_MODELO = _ModeloPorThread()


def detectar_num_frame(modelo, img_pil):
    """1 frame -> lista de (classe, confianca, area_ratio)."""
    r = modelo.predict(img_pil, verbose=False)[0]
    w, h = img_pil.size
    area_total = max(w * h, 1)
    achados = []
    for box in r.boxes:
        classe = modelo.names[int(box.cls[0])]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        area_ratio = max((x2 - x1) * (y2 - y1), 0) / area_total
        achados.append((classe, conf, area_ratio))
    return achados


def julgar(frames, tipo):
    """
    Roda o detector nos frames (1 pra foto, N pra vídeo) e decide aprovado
    ou não. Regra: 'person' em QUALQUER frame reprova; 'dog' em NENHUM frame
    reprova. Devolve (aprovado, motivo_se_reprovado, componentes_do_score).
    """
    modelo = _FABRICA_MODELO.get()
    melhor_conf_dog = 0.0
    melhor_area_dog = 0.0
    tem_pessoa = False
    for frame in frames:
        for classe, conf, area_ratio in detectar_num_frame(modelo, frame):
            if classe == "person" and conf >= CONF_PESSOA:
                tem_pessoa = True
            if classe == "dog" and conf >= CONF_DOG:
                if conf > melhor_conf_dog:
                    melhor_conf_dog = conf
                if area_ratio > melhor_area_dog:
                    melhor_area_dog = area_ratio

    if tem_pessoa:
        return False, "tem pessoa no quadro", None
    if melhor_conf_dog <= 0:
        return False, "sem cachorro reconhecível", None

    # nitidez e resolução: usa o frame de MELHOR enquadramento do cachorro
    # como referência (pra vídeo, não faz sentido medir nitidez do frame
    # errado); na prática, usa o primeiro frame como aproximação barata —
    # medir nitidez em todos os frames custaria caro à toa.
    frame_ref = frames[0]
    w, h = frame_ref.size
    componentes = {
        "dog_conf": round(melhor_conf_dog, 3),
        "area_ratio": round(melhor_area_dog, 3),
        "nitidez": round(nitidez(frame_ref), 1),
        "resolucao_mp": round((w * h) / 1_000_000, 2),
        "video": tipo == "video",
    }
    return True, None, componentes


def calcular_score(c):
    norm_area = min(c["area_ratio"] / 0.5, 1.0)
    norm_nitidez = min(c["nitidez"] / 300.0, 1.0)
    norm_res = min(c["resolucao_mp"] / 8.0, 1.0)
    return round(
        0.35 * norm_area
        + 0.25 * norm_nitidez
        + 0.15 * norm_res
        + 0.15 * c["dog_conf"]
        + 0.10 * (1.0 if c["video"] else 0.0),
        4,
    )


# ---------------------------------------------------------------------------
# Processar 1 arquivo — o que cada thread do pool executa
# ---------------------------------------------------------------------------

def processar_arquivo(nome):
    """Devolve dict: {"nome", "aprovado", "motivo", "componentes", "score", "tipo"}."""
    caminho = os.path.join(FONTE, nome)
    passa, motivo, tipo = descarte_barato(nome, caminho)
    if not passa:
        return {"nome": nome, "aprovado": False, "motivo": motivo}

    tmpdir = None
    try:
        if tipo == "imagem":
            img = abrir_imagem(caminho)
            w, h = img.size
            if w * h < RES_MINIMA:
                return {"nome": nome, "aprovado": False, "motivo": "resolução baixa"}
            frames = [img]
        else:
            tmpdir = tempfile.mkdtemp(prefix="garimpo_")
            frames = extrair_frames_video(caminho, tmpdir)

        aprovado, motivo, componentes = julgar(frames, tipo)
        if not aprovado:
            return {"nome": nome, "aprovado": False, "motivo": motivo}
        score = calcular_score(componentes)
        return {"nome": nome, "aprovado": True, "tipo": tipo,
                "componentes": componentes, "score": score}
    except Exception as exc:  # noqa: BLE001 — 1 arquivo ruim nunca derruba os outros 34 mil
        return {"nome": nome, "aprovado": False, "motivo": f"erro: {str(exc)[:120]}", "erro": True}
    finally:
        if tmpdir and os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)


def _disco_livre_bytes():
    livre = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p(RAIZ), None, None, ctypes.pointer(livre))
    return livre.value


def _copiar_aprovado(nome):
    """Copia (nunca move) da fonte pro garimpo — nunca sobrescreve. Devolve
    True se copiou (ou já existia), False se não deu (aí o robô avisa e
    segue, cópia não pode derrubar o scan)."""
    os.makedirs(SAIDA_BASE, exist_ok=True)
    origem = os.path.join(FONTE, nome)
    destino = os.path.join(SAIDA_BASE, nome)
    if os.path.exists(destino):
        return True
    try:
        shutil.copy2(origem, destino)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"      [aviso] não copiei {nome[:3]}...: {str(exc)[:100]}")
        return False


# ---------------------------------------------------------------------------
# Relatório + top 30
# ---------------------------------------------------------------------------

def gerar_relatorio(estado, tempo_desta_sessao=None):
    os.makedirs(SAIDA_TOP30, exist_ok=True)
    aprovados = estado["aprovados"]
    ranking = sorted(aprovados.items(), key=lambda kv: kv[1]["score"], reverse=True)
    top30 = ranking[:30]

    # top 30 sempre reflete o ranking ATUAL — limpa e recopia (arquivos são
    # pequenos frente ao total, o custo de refazer é baixo).
    for antigo in os.listdir(SAIDA_TOP30):
        try:
            os.remove(os.path.join(SAIDA_TOP30, antigo))
        except OSError:
            pass
    for i, (nome, info) in enumerate(top30, 1):
        origem = os.path.join(SAIDA_BASE, nome)
        if os.path.isfile(origem):
            destino = os.path.join(SAIDA_TOP30, f"{i:02d}_{nome}")
            try:
                shutil.copy2(origem, destino)
            except OSError:
                pass

    total_pasta = len(os.listdir(FONTE)) if os.path.isdir(FONTE) else 0
    n_video = sum(1 for _, i in aprovados.items() if i["componentes"]["video"])
    n_foto = len(aprovados) - n_video

    linhas = []
    linhas.append("# Garimpo do rolo de câmera — relatório\n")
    linhas.append(f"Gerado em {time.strftime('%Y-%m-%d %H:%M:%S')}.\n")
    linhas.append("## Números\n")
    linhas.append(f"- Arquivos na pasta de origem (iCloudPhotos\\Photos): {total_pasta}\n")
    linhas.append(f"- Já varridos até agora: {len(estado['visto'])}\n")
    linhas.append(f"- Faltam varrer: {max(total_pasta - len(estado['visto']), 0)}\n")
    linhas.append(f"- Aprovados (cachorro, sem pessoa): {len(aprovados)} "
                   f"({n_foto} foto(s), {n_video} vídeo(s))\n")
    linhas.append(f"- Erros ao abrir: {estado['erros']}\n")
    linhas.append(f"- Tempo total gasto (todas as sessões): "
                   f"{estado['segundos_gastos']/3600:.1f}h\n")
    if tempo_desta_sessao:
        linhas.append(f"- Tempo gasto NESTA sessão: {tempo_desta_sessao/60:.1f} min\n")
    linhas.append("\n## Por que foi reprovado (contagem, sem nome de arquivo)\n")
    for motivo, n in sorted(estado["motivos_reprovacao"].items(), key=lambda kv: -kv[1]):
        linhas.append(f"- {motivo}: {n}\n")
    linhas.append("\n## Critério do ranking\n")
    linhas.append("`score = 0,35×área do cachorro no quadro + 0,25×nitidez + "
                   "0,15×resolução + 0,15×confiança do detector + 0,10×bônus de vídeo`\n")
    linhas.append("\n## Top 30 (copiados em `melhores-30/`)\n")
    linhas.append("| # | arquivo | tipo | score | área% | nitidez | MP | confiança |\n")
    linhas.append("|---|---|---|---|---|---|---|---|\n")
    for i, (nome, info) in enumerate(top30, 1):
        c = info["componentes"]
        linhas.append(f"| {i} | {nome} | {info['tipo']} | {info['score']:.3f} | "
                       f"{c['area_ratio']*100:.0f}% | {c['nitidez']:.0f} | "
                       f"{c['resolucao_mp']:.1f} | {c['dog_conf']:.2f} |\n")
    linhas.append("\n## Limites honestos\n")
    linhas.append("- O detector reconhece 'é um cachorro', não 'é A Hana' — não há "
                   "reconhecimento individual. Cachorro de outra pessoa passa igual.\n")
    linhas.append("- Vídeo é julgado por 5 frames amostrados (± primeiros 5s do clipe), "
                   "não pelo clipe inteiro — pessoa fora da amostra não é pega.\n")
    linhas.append("- Todo .png foi descartado sem abrir (tratado como print de tela).\n")

    with open(RELATORIO_ARQ, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    return len(aprovados), n_foto, n_video, total_pasta


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--amostra", type=int, default=None,
                     help="processa só N arquivos novos (teste rápido/medição)")
    ap.add_argument("--minutos", type=float, default=None,
                     help="orçamento de tempo; para e salva quando estourar")
    ap.add_argument("--workers", type=int, default=3,
                     help="threads em paralelo (a espera de download não usa CPU)")
    ap.add_argument("--relatorio", action="store_true",
                     help="só regera RELATORIO.md e a pasta melhores-30, sem varrer nada novo")
    ap.add_argument("--resetar-estado", action="store_true",
                     help="apaga o progresso salvo e recomeça do zero")
    a = ap.parse_args()

    if not os.path.isdir(FONTE):
        print(f"[ERRO] pasta de origem não existe: {FONTE}")
        return 1

    if a.resetar_estado:
        if os.path.isfile(ESTADO_ARQ):
            os.remove(ESTADO_ARQ)
        print("[ok] estado apagado.")
        return 0

    estado = carregar_estado()

    if a.relatorio:
        n, nf, nv, total = gerar_relatorio(estado)
        print(f"[ok] relatório regerado: {n} aprovados ({nf} foto, {nv} vídeo) "
              f"de {total} arquivos na pasta. Ver {RELATORIO_ARQ}")
        return 0

    todos = sorted(os.listdir(FONTE))
    ja_visto = set(estado["visto"])
    pendentes = [n for n in todos if n not in ja_visto]
    print(f"[info] {len(todos)} arquivo(s) na pasta, {len(pendentes)} ainda não varrido(s).")

    if not pendentes:
        print("[ok] nada pendente — pasta inteira já foi varrida.")
        gerar_relatorio(estado)
        return 0

    if a.amostra:
        pendentes = pendentes[: a.amostra]
        print(f"[info] --amostra: processando só {len(pendentes)} arquivo(s) nesta rodada.")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    # Baixa/carrega o modelo UMA VEZ na thread principal antes de abrir o
    # pool — sem isto, achado no teste real (01/08/2026): as N threads
    # tentam baixar o mesmo arquivo yolov8n.pt ao mesmo tempo (cada uma cria
    # seu próprio YOLO() na primeira chamada), disparando 3 downloads
    # concorrentes pro mesmo caminho. Funcionou por sorte (o download é
    # atômico), mas é desperdício e um risco bobo de corromper o arquivo.
    _FABRICA_MODELO.get()

    inicio_sessao = time.time()
    inicio = inicio_sessao  # marca do último checkpoint — vai sendo reposto a cada save
    prazo = inicio_sessao + a.minutos * 60 if a.minutos else None
    lote_desde_ultimo_save = 0
    processados_nesta_sessao = 0
    parou_por_tempo = False
    parou_por_disco = False

    print(f"[info] rodando com {a.workers} thread(s). "
          f"{'sem limite de tempo' if not prazo else f'para em {a.minutos} min'}.")

    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        futuros = {}
        fila = iter(pendentes)

        def _preencher():
            while len(futuros) < a.workers * 2:
                nome = next(fila, None)
                if nome is None:
                    return False
                futuros[pool.submit(processar_arquivo, nome)] = nome
            return True

        _preencher()
        while futuros:
            if _disco_livre_bytes() < DISCO_MINIMO_LIVRE:
                print("[PAROU] disco com menos de 10 GB livres — melhor parar do que "
                      "arriscar encher a máquina baixando arquivo do iCloud.")
                parou_por_disco = True
                break
            if prazo and time.time() > prazo:
                parou_por_tempo = True
                break

            done = next(as_completed(list(futuros.keys())))
            nome = futuros.pop(done)
            resultado = done.result()

            estado["visto"].append(nome)
            estado["arquivos_varridos"] += 1
            processados_nesta_sessao += 1
            if resultado.get("erro"):
                estado["erros"] += 1
            if resultado["aprovado"]:
                estado["aprovados"][nome] = {
                    "score": resultado["score"],
                    "componentes": resultado["componentes"],
                    "tipo": resultado["tipo"],
                }
                _copiar_aprovado(nome)
                print(f"      [APROVADO] score={resultado['score']:.3f} "
                      f"({resultado['tipo']})")
            else:
                motivo = resultado.get("motivo", "?")
                estado["motivos_reprovacao"][motivo] = (
                    estado["motivos_reprovacao"].get(motivo, 0) + 1)

            lote_desde_ultimo_save += 1
            if lote_desde_ultimo_save >= 10:
                estado["segundos_gastos"] += time.time() - inicio
                inicio = time.time()
                salvar_estado_atomico(estado)
                lote_desde_ultimo_save = 0
                decorrido = processados_nesta_sessao
                print(f"[progresso] {decorrido}/{len(pendentes)} nesta sessão "
                      f"({len(estado['visto'])} no total) — estado salvo.")

            _preencher()

        # não deixa futuros pendentes órfãos se saiu por tempo/disco
        for f in list(futuros.keys()):
            f.cancel()

    estado["segundos_gastos"] += time.time() - inicio
    salvar_estado_atomico(estado)

    tempo_sessao = time.time() - inicio_sessao
    n, nf, nv, total = gerar_relatorio(estado, tempo_desta_sessao=tempo_sessao)

    print()
    if parou_por_tempo:
        print(f"[ok] orçamento de {a.minutos} min esgotado — rode de novo pra continuar.")
    elif parou_por_disco:
        print("[ok] parado por segurança de disco — libere espaço e rode de novo.")
    else:
        print(f"[ok] {processados_nesta_sessao} arquivo(s) processado(s) nesta sessão.")
    print(f"[resumo] {n} aprovado(s) no total ({nf} foto, {nv} vídeo) de {total} na pasta. "
          f"Relatório em {RELATORIO_ARQ}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
