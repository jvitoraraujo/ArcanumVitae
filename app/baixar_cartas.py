# -*- coding: utf-8 -*-
"""Baixa as 78 cartas oficiais Rider-Waite-Smith (domínio público) para assets/cartas.

Fonte: Wikimedia Commons (ilustrações de Pamela Colman Smith, 1909).
Uso:   python baixar_cartas.py
Sem dependências externas (usa urllib). Pula arquivos já baixados.
Os nomes seguem o padrão do app: maior_<nº RWS>.jpg e <naipe>_<carta>.jpg
"""
import os
import time
import urllib.error
import urllib.request

from cartas import CARTAS, pasta_assets

PASTA = os.path.join(pasta_assets(), "cartas")
UA = "ArcanumVitaeApp/2.1 (jogo de tabuleiro; download unico das cartas RWS)"


def baixar(url, destino, tentativas=3):
    for t in range(1, tentativas + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                dados = r.read()
            if dados[:3] != b"\xff\xd8\xff":
                raise ValueError("resposta não é JPEG")
            with open(destino, "wb") as f:
                f.write(dados)
            return True
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            print(f"   tentativa {t}/{tentativas} falhou: {e}")
            time.sleep(2 * t)
    return False


def main():
    os.makedirs(PASTA, exist_ok=True)
    print("--- Baixando Tarot Rider-Waite-Smith (78 cartas) ---")
    falhas = []
    for cid, c in CARTAS.items():
        destino = os.path.join(PASTA, c["arq_local"])
        if os.path.isfile(destino) and os.path.getsize(destino) > 2000:
            print(f"ok (já existe)  {c['arq_local']}")
            continue
        print(f"baixando        {c['arq_local']}  <-  {c['arq_commons']}")
        if baixar(c["url"], destino):
            time.sleep(0.3)  # gentileza com o servidor
        else:
            falhas.append(c["arq_local"])
    print()
    if falhas:
        print("FALHARAM:", ", ".join(falhas))
        print("Rode novamente; o app também baixa as faltantes sozinho quando online.")
    else:
        print("Concluído! Todas as 78 cartas estão em assets/cartas.")


if __name__ == "__main__":
    main()
