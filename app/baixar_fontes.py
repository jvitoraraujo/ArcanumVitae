# -*- coding: utf-8 -*-
"""Opcional: baixa as fontes da marca DEVA (Cinzel e JetBrains Mono, licença OFL) para assets/fonts.

Sem elas o app usa a fonte padrão do Kivy (Roboto) e funciona normalmente.
Uso:  python baixar_fontes.py
"""
import os
import urllib.error
import urllib.request

from cartas import pasta_assets

PASTA = os.path.join(pasta_assets(), "fonts")
UA = "ArcanumVitaeApp/2.2 (download unico de fontes OFL)"
FONTES = {
    "Cinzel[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    "JetBrainsMono[wght].ttf": "https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}
ASSINATURAS = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"ttcf")


def main():
    os.makedirs(PASTA, exist_ok=True)
    for nome, url in FONTES.items():
        destino = os.path.join(PASTA, nome)
        if os.path.isfile(destino) and os.path.getsize(destino) > 10000:
            print("ok (já existe)  ", nome)
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                dados = r.read()
            if dados[:4] not in ASSINATURAS:
                raise ValueError("arquivo não parece uma fonte TrueType")
            with open(destino, "wb") as f:
                f.write(dados)
            print("baixada         ", nome)
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            print(f"FALHOU          {nome}: {e}\n   Baixe manualmente em fonts.google.com e salve em {PASTA}")


if __name__ == "__main__":
    main()
