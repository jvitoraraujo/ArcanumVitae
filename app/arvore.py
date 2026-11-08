# -*- coding: utf-8 -*-
"""Geometria da Árvore da Vida (sem dependência do Kivy).

Coordenadas normalizadas (0..1) seguindo o tabuleiro: x da esquerda p/ direita,
y de baixo p/ cima. CAMINHOS lista os 22 caminhos (pares de Esferas).
"""
import math

NOS = {
    'Keter':    (0.50, 0.95),
    'Chokmah':  (0.80, 0.82),
    'Binah':    (0.20, 0.82),
    'Chesed':   (0.80, 0.62),
    'Gevurah':  (0.20, 0.62),
    'Tiferet':  (0.50, 0.50),
    'Netzach':  (0.80, 0.32),
    'Hod':      (0.20, 0.32),
    'Yesod':    (0.50, 0.19),
    'Malkuth':  (0.50, 0.05),
}

ZONA = {'Malkuth': 1, 'Yesod': 1, 'Hod': 2, 'Netzach': 2, 'Tiferet': 2,
        'Gevurah': 3, 'Chesed': 3, 'Binah': 4, 'Chokmah': 4, 'Keter': 4}

CAMINHOS = [
    ('Keter', 'Chokmah'), ('Keter', 'Binah'), ('Keter', 'Tiferet'),
    ('Chokmah', 'Binah'), ('Chokmah', 'Tiferet'), ('Chokmah', 'Chesed'),
    ('Binah', 'Tiferet'), ('Binah', 'Gevurah'),
    ('Chesed', 'Gevurah'), ('Chesed', 'Tiferet'), ('Chesed', 'Netzach'),
    ('Gevurah', 'Tiferet'), ('Gevurah', 'Hod'),
    ('Tiferet', 'Netzach'), ('Tiferet', 'Yesod'), ('Tiferet', 'Hod'),
    ('Netzach', 'Hod'), ('Netzach', 'Yesod'), ('Netzach', 'Malkuth'),
    ('Hod', 'Yesod'), ('Hod', 'Malkuth'), ('Yesod', 'Malkuth'),
]


def ponto(nome, x, y, w, h, margem=0.0):
    """Posição em pixels do nó dentro de um retângulo (x, y, w, h)."""
    nx, ny = NOS[nome]
    mx, my = w * margem, h * margem
    return x + mx + nx * (w - 2 * mx), y + my + ny * (h - 2 * my)


def mais_proximo(px, py, x, y, w, h, limite, margem=0.0):
    """Nome do nó mais próximo de (px, py) dentro do limite em pixels, ou None."""
    melhor, dmin = None, limite
    for nome in NOS:
        nx, ny = ponto(nome, x, y, w, h, margem)
        d = math.hypot(px - nx, py - ny)
        if d <= dmin:
            melhor, dmin = nome, d
    return melhor


def vizinhos(nome):
    """Esferas ligadas a `nome` por um caminho."""
    out = []
    for a, b in CAMINHOS:
        if a == nome:
            out.append(b)
        elif b == nome:
            out.append(a)
    return out
