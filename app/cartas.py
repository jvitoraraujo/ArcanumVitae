"""Catálogo das 78 cartas e suas imagens oficiais Rider-Waite-Smith (RWS).

As ilustrações originais de Pamela Colman Smith (1909) estão em domínio público
e são hospedadas no Wikimedia Commons. Este módulo NÃO depende do Kivy, então
pode ser usado tanto pelo app quanto pelo script baixar_cartas.py.

Numeração: o manual segue o Rider-Waite (VIII = A Força, XI = A Justiça), então
o número do jogo e o número RWS coincidem. As imagens são localizadas pela
chave (nome) da carta.
"""
import hashlib
import os
import unicodedata

from dados_jogo import ARCANOS_MAIORES

COMMONS_BASE = "https://upload.wikimedia.org/wikipedia/commons/"

ORDEM_MENORES = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'Valete', 'Cavaleiro', 'Rainha', 'Rei']
RANK_EN = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
           'Nine', 'Ten', 'Page', 'Knight', 'Queen', 'King']

# chave -> (nome PT, nome EN, prefixo do arquivo no Commons)
NAIPES = {
    'paus':    ('Paus',    'Wands',     'Wands'),
    'copas':   ('Copas',   'Cups',      'Cups'),
    'espadas': ('Espadas', 'Swords',    'Swords'),
    'ouros':   ('Ouros',   'Pentacles', 'Pents'),
}

NOMES_EN_MAIORES = {
    'louco': 'The Fool', 'mago': 'The Magician', 'papisa': 'The High Priestess',
    'imperatriz': 'The Empress', 'imperador': 'The Emperor', 'papa': 'The Hierophant',
    'enamorados': 'The Lovers', 'carro': 'The Chariot', 'justica': 'Justice',
    'eremita': 'The Hermit', 'roda': 'Wheel of Fortune', 'forca': 'Strength',
    'pendurado': 'The Hanged Man', 'morte': 'Death', 'temperanca': 'Temperance',
    'diabo': 'The Devil', 'torre': 'The Tower', 'estrela': 'The Star',
    'lua': 'The Moon', 'sol': 'The Sun', 'julgamento': 'Judgement', 'mundo': 'The World',
}

NUMERAIS = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
            'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX',
            'XX', 'XXI']


def pasta_assets():
    """Pasta de assets: ../assets (layout do repositório) ou ./assets (app empacotado)."""
    base = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(base, 'assets'), os.path.join(base, '..', 'assets')):
        if os.path.isdir(cand):
            return os.path.abspath(cand)
    return os.path.join(base, 'assets')


def slug(texto):
    """'Ás' -> 'as', 'Cavaleiro' -> 'cavaleiro' (sem acento, minúsculo)."""
    n = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in n if not unicodedata.combining(c)).lower()


def url_commons(arquivo):
    """URL direta do arquivo no Commons (pasta = 1º e 2 primeiros hex do MD5 do nome)."""
    h = hashlib.md5(arquivo.encode('utf-8')).hexdigest()
    return f"{COMMONS_BASE}{h[0]}/{h[:2]}/{arquivo}"


def id_maior(chave):
    return f"maior_{chave}"


def id_menor(naipe, carta):
    return f"{naipe}_{slug(carta)}"


def _montar():
    cartas = {}
    for m in ARCANOS_MAIORES:
        cid = id_maior(m['chave'])
        cartas[cid] = dict(
            id=cid, tipo='maior', chave=m['chave'],
            nome_pt=m['nome'], nome_en=NOMES_EN_MAIORES[m['chave']],
            numero_jogo=m['num'], numeral_jogo=m['numeral'],
            numero_rws=m['rws_num'], numeral_rws=NUMERAIS[m['rws_num']],
            arq_commons=m['rws_arquivo'],
            arq_local=f"maior_{m['rws_num']}.jpg",
        )
    for chave, (pt, en, pref) in NAIPES.items():
        for i, rank in enumerate(ORDEM_MENORES):
            cid = id_menor(chave, rank)
            arq = f"{pref}{i + 1:02d}.jpg"
            if rank in ('Valete', 'Cavaleiro', 'Rainha', 'Rei'):
                nome_pt = f"{rank} de {pt}"
            elif rank == 'Ás':
                nome_pt = f"Ás de {pt}"
            else:
                nome_pt = f"{rank} de {pt}"
            cartas[cid] = dict(
                id=cid, tipo='menor', naipe=chave, carta=rank,
                nome_pt=nome_pt, nome_en=f"{RANK_EN[i]} of {en}",
                arq_commons=arq, arq_local=f"{chave}_{slug(rank)}.jpg",
            )
    for c in cartas.values():
        c['url'] = url_commons(c['arq_commons'])
    return cartas


CARTAS = _montar()
