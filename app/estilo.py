# -*- coding: utf-8 -*-
"""Tokens visuais: paleta DEVA (Cosmic Darkness & Starlight) e fontes opcionais."""
import os

from cartas import pasta_assets


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


VOID = hexc('050811')     # canvas
SURF = hexc('0B111E')     # superfície
ELEV = hexc('0F172A')     # elevado
GOLD = hexc('DFB15B')     # ouro estelar
GOLD_H = hexc('E2B857')
CEL = hexc('8DA9C4')      # azul celestial
TXT = hexc('E2E8F0')      # pergaminho
TXT2 = hexc('94A3B8')
BORDA = hexc('1E293B')
OK = hexc('7FC4A0')
WARN = hexc('E9A64A')
BAD = hexc('E8837C')

ASSETS = pasta_assets()
DEVA = os.path.join(ASSETS, 'deva')
LOGO = os.path.join(ASSETS, 'logo.png')
FONTS = os.path.join(ASSETS, 'fonts')


def _fonte(candidatos, padrao='Roboto'):
    for nome in candidatos:
        p = os.path.join(FONTS, nome)
        if os.path.isfile(p):
            return p
    return padrao


# Opcionais: rode baixar_fontes.py para obter Cinzel e JetBrains Mono (licença OFL).
FONTE_TITULO = _fonte(['Cinzel-Regular.ttf', 'Cinzel[wght].ttf', 'Cinzel.ttf'])
FONTE_MONO = _fonte(['JetBrainsMono-Regular.ttf', 'JetBrainsMono[wght].ttf', 'JetBrainsMono.ttf'], 'RobotoMono-Regular')


def espacar(texto):
    """Espaça letras (efeito de tracking largo) sem depender de glifos especiais."""
    return ' '.join(texto)
