# -*- coding: utf-8 -*-
"""Widgets do Grimório: cartografia celeste + Tarot + marca DEVA (somente Kivy)."""
import math
import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics import (Color, Ellipse, InstructionGroup, Line, Point, PopMatrix,
                           PushMatrix, Rectangle, RoundedRectangle, Rotate, Scale)
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

import arvore
from estilo import CEL, ELEV, FONTE_MONO, FONTE_TITULO, GOLD, SURF, TXT, TXT2, VOID


def loop(*anims):
    """Encadeia animações em laço infinito."""
    seq = anims[0]
    for a in anims[1:]:
        seq = seq + a
    seq.repeat = True
    return seq


def revelar(widgets, atraso=0.05, dur=0.42, inicio=0.12, limite=14):
    """Entrada escalonada (fade-in) dos widgets de uma página."""
    for i, w in enumerate(widgets):
        w.opacity = 0
        Clock.schedule_once(
            lambda dt, w=w: Animation(opacity=1, d=dur, t='out_quad').start(w),
            inicio + min(i, limite) * atraso)


# ------------------------------------------------------------------ texto
def rotulo(texto, tam=15, cor=TXT, negrito=False, alinhar='left', fonte=None, linha=1.22):
    lb = Label(text=texto, markup=True, color=cor, font_size=sp(tam), bold=negrito,
               halign=alinhar, valign='top', size_hint_y=None, line_height=linha)
    if fonte:
        lb.font_name = fonte
    lb.bind(width=lambda i, w: setattr(i, 'text_size', (w, None)))
    lb.bind(texture_size=lambda i, s: setattr(i, 'height', s[1] + dp(2)))
    return lb


def titulo(texto):
    """H2 DEVA: caixa-alta, dourado, serifa."""
    return rotulo(texto.upper(), 18, GOLD, False, 'left', FONTE_TITULO)


def legenda(texto, cor=CEL, alinhar='left'):
    """Rótulo de seção/metadado: mono, caixa-alta, azul celestial."""
    return rotulo(texto.upper(), 11, cor, False, alinhar, FONTE_MONO)


# ------------------------------------------------------------------ fundo
class Fundo(Widget):
    """Céu noturno: estrelas, anéis de cartografia e meridianos. Pode cintilar."""
    brilho = NumericProperty(0)

    def __init__(self, animado=False, **kw):
        super().__init__(**kw)
        rnd = random.Random(11)
        self._estrelas = [(rnd.random(), rnd.random(), rnd.choice((1, 1, 1, 2, 2, 3))) for _ in range(90)]
        self._piscantes = [(rnd.random(), rnd.random()) for _ in range(16)]
        self._cor_pisca = None
        self.bind(pos=self._desenhar, size=self._desenhar, brilho=self._piscar)
        if animado:
            loop(Animation(brilho=1, d=2.4, t='in_out_sine'),
                 Animation(brilho=0, d=2.4, t='in_out_sine')).start(self)

    def _desenhar(self, *a):
        self.canvas.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        with self.canvas:
            Color(*VOID)
            Rectangle(pos=self.pos, size=self.size)
            Color(CEL[0], CEL[1], CEL[2], 0.05)
            for k in range(1, 7):
                Line(points=[x + w * k / 7, y, x + w * k / 7, y + h], width=0.6)
            Color(CEL[0], CEL[1], CEL[2], 0.07)
            for cx, cy in ((x + w, y + h * 0.9), (x, y + h * 0.1)):
                for k in range(1, 6):
                    Line(circle=(cx, cy, dp(72) * k), width=1)
            for tam in (1, 2, 3):
                pts = []
                for ex, ey, t in self._estrelas:
                    if t == tam:
                        pts += [x + ex * w, y + ey * h]
                Color(CEL[0], CEL[1], CEL[2], 0.28 + 0.1 * tam)
                Point(points=pts, pointsize=dp(0.7) * tam)
            self._cor_pisca = Color(GOLD[0], GOLD[1], GOLD[2], 0.2)
            Point(points=[v for ex, ey in self._piscantes for v in (x + ex * w, y + ey * h)],
                  pointsize=dp(1.7))

    def _piscar(self, *a):
        if self._cor_pisca is not None:
            self._cor_pisca.a = 0.12 + 0.78 * self.brilho


class AnelCeleste(Widget):
    """Anel zodiacal de cartografia celeste que gira lentamente."""
    angulo = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            PushMatrix()
            self._rot = Rotate(angle=0, origin=(0, 0))
        self._g = InstructionGroup()
        self.canvas.add(self._g)
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self._desenhar, size=self._desenhar, angulo=self._girar)
        loop(Animation(angulo=-360, d=240), Animation(angulo=0, d=0)).start(self)

    def _girar(self, *a):
        self._rot.angle = self.angulo

    def _desenhar(self, *a):
        cx, cy = self.center
        r = min(self.width, self.height) / 2 * 0.95
        self._rot.origin = (cx, cy)
        g = self._g
        g.clear()
        g.add(Color(GOLD[0], GOLD[1], GOLD[2], 0.30))
        g.add(Line(circle=(cx, cy, r), width=1.1))
        g.add(Color(CEL[0], CEL[1], CEL[2], 0.28))
        g.add(Line(circle=(cx, cy, r * 0.86), width=0.8, dash_length=dp(2), dash_offset=dp(4)))
        g.add(Line(circle=(cx, cy, r * 0.70), width=0.7))
        for i in range(72):
            ang = math.radians(i * 5)
            longo = i % 6 == 0
            r1, r2 = r * (0.93 if longo else 0.96), r
            g.add(Color(GOLD[0], GOLD[1], GOLD[2], 0.45 if longo else 0.18))
            g.add(Line(points=[cx + r1 * math.cos(ang), cy + r1 * math.sin(ang),
                               cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)], width=1))
        g.add(Color(CEL[0], CEL[1], CEL[2], 0.5))
        for i in range(12):  # nós zodiacais
            ang = math.radians(i * 30 + 15)
            nx, ny = cx + r * 0.86 * math.cos(ang), cy + r * 0.86 * math.sin(ang)
            g.add(Ellipse(pos=(nx - dp(2), ny - dp(2)), size=(dp(4), dp(4))))


class Divisor(Widget):
    """Divisor canônico DEVA: linhas finas, pontos e estrela de 4 pontas ao centro."""

    def __init__(self, **kw):
        kw.setdefault('size_hint_y', None)
        kw.setdefault('height', dp(20))
        super().__init__(**kw)
        self.bind(pos=self._desenhar, size=self._desenhar)

    def _desenhar(self, *a):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = dp(6)
        meio = self.width * 0.5
        with self.canvas:
            Color(GOLD[0], GOLD[1], GOLD[2], 0.35)
            Line(points=[self.x, cy, cx - dp(40), cy], width=1)
            Line(points=[cx + dp(40), cy, self.right, cy], width=1)
            Color(CEL[0], CEL[1], CEL[2], 0.7)
            for dx in (-dp(30), -dp(20), dp(20), dp(30)):
                Ellipse(pos=(cx + dx - dp(1), cy - dp(1)), size=(dp(2), dp(2)))
            Color(*GOLD)
            Line(points=[cx, cy + r, cx + r * 0.28, cy + r * 0.28, cx + r, cy, cx + r * 0.28, cy - r * 0.28,
                         cx, cy - r, cx - r * 0.28, cy - r * 0.28, cx - r, cy, cx - r * 0.28, cy + r * 0.28],
                 width=1.1, close=True)


# ------------------------------------------------------------------ botões e cartões
class BotaoDeva(ButtonBehavior, Label):
    """Botão com borda dourada, caixa-alta e brilho ao toque."""
    brilho = NumericProperty(0)

    def __init__(self, texto, acao=None, primario=True, **kw):
        kw.setdefault('size_hint_y', None)
        kw.setdefault('height', dp(54))
        super().__init__(text=texto.upper(), font_size=sp(14), halign='center', valign='middle',
                         color=GOLD if primario else TXT, font_name=FONTE_TITULO, **kw)
        cor = GOLD if primario else CEL
        with self.canvas.before:
            Color(*ELEV)
            self._fundo = RoundedRectangle(radius=[dp(10)])
            self._c_glow = Color(GOLD[0], GOLD[1], GOLD[2], 0)
            self._glow = RoundedRectangle(radius=[dp(10)])
            Color(cor[0], cor[1], cor[2], 0.6)
            self._borda = Line(rounded_rectangle=(0, 0, 0, 0, dp(10)), width=1.1)
        self.bind(pos=self._atualiza, size=self._atualiza, brilho=self._brilhar)
        self.bind(size=lambda i, s: setattr(i, 'text_size', s))
        if acao:
            self.bind(on_release=lambda *_: acao())

    def _atualiza(self, *a):
        self._fundo.pos = self._glow.pos = self.pos
        self._fundo.size = self._glow.size = self.size
        self._borda.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(10))

    def _brilhar(self, *a):
        self._c_glow.a = 0.28 * self.brilho

    def on_press(self):
        Animation(brilho=1, d=0.1).start(self)

    def on_release(self):
        Animation(brilho=0, d=0.4, t='out_quad').start(self)

    def pulsar(self):
        loop(Animation(brilho=0.8, d=1.3, t='in_out_sine'),
             Animation(brilho=0, d=1.3, t='in_out_sine')).start(self)


class Cartao(BoxLayout):
    """Superfície DEVA com borda sutil e altura que acompanha o conteúdo."""

    def __init__(self, cor=SURF, realce=None, **kw):
        kw.setdefault('orientation', 'vertical')
        kw.setdefault('padding', dp(14))
        kw.setdefault('spacing', dp(6))
        super().__init__(size_hint_y=None, **kw)
        self.bind(minimum_height=lambda i, h: setattr(i, 'height', h))
        borda = realce or CEL
        with self.canvas.before:
            Color(*cor)
            self._ret = RoundedRectangle(radius=[dp(10)])
            Color(borda[0], borda[1], borda[2], 0.28)
            self._lin = Line(rounded_rectangle=(0, 0, 0, 0, dp(10)), width=1)
            Color(GOLD[0], GOLD[1], GOLD[2], 0.55)
            self._topo = Line(points=[0, 0, 0, 0], width=1.4)
        self.bind(pos=self._atualiza, size=self._atualiza)

    def _atualiza(self, *a):
        self._ret.pos, self._ret.size = self.pos, self.size
        self._lin.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(10))
        self._topo.points = [self.x + dp(14), self.top, self.x + dp(54), self.top]


class BotaoVoltar(ButtonBehavior, Widget):
    def __init__(self, **kw):
        kw.setdefault('size_hint', (None, None))
        kw.setdefault('size', (dp(48), dp(48)))
        super().__init__(**kw)
        self.bind(pos=self._desenhar, size=self._desenhar)

    def _desenhar(self, *a):
        self.canvas.clear()
        cx, cy = self.center
        with self.canvas:
            Color(*GOLD)
            Line(points=[cx + dp(4), cy + dp(10), cx - dp(5), cy, cx + dp(4), cy - dp(10)], width=1.8)

    def on_press(self):
        Animation(opacity=0.4, d=0.08).start(self)

    def on_release(self):
        Animation(opacity=1, d=0.25).start(self)


class BarraTopo(BoxLayout):
    def __init__(self, ao_voltar, **kw):
        super().__init__(orientation='horizontal', size_hint_y=None, height=dp(56),
                         padding=[dp(4), 0, dp(4), 0], **kw)
        self.voltar = BotaoVoltar()
        self.voltar.bind(on_release=lambda *_: ao_voltar())
        self.titulo = Label(text='', color=GOLD, font_size=sp(15), font_name=FONTE_TITULO,
                            halign='center', valign='middle', shorten=True, shorten_from='right')
        self.titulo.bind(size=lambda i, s: setattr(i, 'text_size', s))
        self.add_widget(self.voltar)
        self.add_widget(self.titulo)
        self.add_widget(Widget(size_hint_x=None, width=dp(48)))
        with self.canvas.before:
            Color(*SURF)
            self._bg = Rectangle()
            Color(GOLD[0], GOLD[1], GOLD[2], 0.3)
            self._linha = Line(points=[0, 0, 0, 0], width=1)
        self.bind(pos=self._atualiza, size=self._atualiza)

    def _atualiza(self, *a):
        self._bg.pos, self._bg.size = self.pos, self.size
        self._linha.points = [self.x, self.y, self.right, self.y]

    def definir(self, texto):
        self.titulo.text = texto.upper()


# ------------------------------------------------------------------ mapa da Árvore
class MapaArvore(Widget):
    """Constelação da Árvore da Vida (10 Esferas, 22 Caminhos). Pulsa e pode ser tocada."""
    pulso = NumericProperty(0)

    def __init__(self, interativo=False, rotulos=True, ao_tocar=None, margem=0.1, **kw):
        super().__init__(**kw)
        self.interativo, self.rotulos, self.ao_tocar, self.margem = interativo, rotulos, ao_tocar, margem
        self._halos = []
        self.bind(pos=self._desenhar, size=self._desenhar, pulso=self._pulsar)
        loop(Animation(pulso=1, d=1.9, t='in_out_sine'),
             Animation(pulso=0, d=1.9, t='in_out_sine')).start(self)

    def _p(self, nome):
        return arvore.ponto(nome, self.x, self.y, self.width, self.height, self.margem)

    def _desenhar(self, *a):
        self.canvas.clear()
        self._halos = []
        r = dp(13) if self.interativo else dp(10)
        with self.canvas:
            for a_, b_ in arvore.CAMINHOS:
                (x1, y1), (x2, y2) = self._p(a_), self._p(b_)
                Color(CEL[0], CEL[1], CEL[2], 0.32)
                Line(points=[x1, y1, x2, y2], width=1)
                Color(GOLD[0], GOLD[1], GOLD[2], 0.4)  # "casas" ao longo do caminho
                Point(points=[v for t in (0.3, 0.5, 0.7) for v in (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)],
                      pointsize=dp(1.3))
            for i, nome in enumerate(arvore.NOS):
                x, y = self._p(nome)
                abismo = arvore.ZONA[nome] == 4
                cor = CEL if abismo else GOLD
                halo = Color(cor[0], cor[1], cor[2], 0.12)
                elip = Ellipse(pos=(x - r * 1.9, y - r * 1.9), size=(r * 3.8, r * 3.8))
                self._halos.append((i, halo, elip, x, y, r))
                Color(*VOID)
                Ellipse(pos=(x - r, y - r), size=(2 * r, 2 * r))
                Color(*cor)
                Line(circle=(x, y, r), width=1.4)
                Color(cor[0], cor[1], cor[2], 0.8)
                Ellipse(pos=(x - r * 0.28, y - r * 0.28), size=(r * 0.56, r * 0.56))
                if self.rotulos:
                    lb = CoreLabel(text=nome.upper(), font_size=sp(9), font_name=FONTE_MONO)
                    lb.refresh()
                    tex = lb.texture
                    Color(*TXT2)
                    Rectangle(texture=tex, size=tex.size, pos=(x - tex.width / 2, y - r - tex.height - dp(3)))
        self._pulsar()

    def _pulsar(self, *a):
        for i, halo, elip, x, y, r in self._halos:
            f = self.pulso if i % 2 == 0 else 1 - self.pulso
            halo.a = 0.06 + 0.2 * f
            k = 1.7 + 0.5 * f
            elip.pos = (x - r * k, y - r * k)
            elip.size = (2 * r * k, 2 * r * k)

    def on_touch_down(self, touch):
        if self.interativo and self.collide_point(*touch.pos):
            touch.grab(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            dx, dy = touch.pos[0] - touch.opos[0], touch.pos[1] - touch.opos[1]
            if math.hypot(dx, dy) < dp(12):
                nome = arvore.mais_proximo(touch.pos[0], touch.pos[1], self.x, self.y, self.width,
                                           self.height, dp(34), self.margem)
                if nome and self.ao_tocar:
                    self.ao_tocar(nome)
            return True
        return super().on_touch_up(touch)


# ------------------------------------------------------------------ cartas de Tarot
class ImgFlip(Image):
    """Imagem que pode "virar" (escala horizontal) como uma carta de Tarot."""
    sx = NumericProperty(1)

    def __init__(self, **kw):
        kw.setdefault('fit_mode', 'contain')
        super().__init__(**kw)
        with self.canvas.before:
            PushMatrix()
            self._esc = Scale(1, 1, 1)
        with self.canvas.after:
            PopMatrix()
        self.bind(sx=self._escalar, pos=self._escalar, size=self._escalar)

    def _escalar(self, *a):
        self._esc.origin = self.center
        self._esc.x = max(self.sx, 0.001)

    def virar(self, dur=0.55, atraso=0.0):
        self.sx = 0
        Clock.schedule_once(lambda dt: Animation(sx=1, d=dur, t='out_back').start(self), atraso)


class Moldura(Widget):
    """Moldura dourada com brilho pulsante, ao redor de uma carta."""
    brilho = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._cores = []
        self.bind(pos=self._desenhar, size=self._desenhar, brilho=self._brilhar)
        loop(Animation(brilho=1, d=1.8, t='in_out_sine'),
             Animation(brilho=0, d=1.8, t='in_out_sine')).start(self)

    def _desenhar(self, *a):
        self.canvas.clear()
        self._cores = []
        x, y, w, h = self.x, self.y, self.width, self.height
        with self.canvas:
            for k, base in ((3, 0.10), (2, 0.16), (1, 0.28)):
                c = Color(GOLD[0], GOLD[1], GOLD[2], base)
                self._cores.append((c, base))
                Line(rounded_rectangle=(x - dp(3) * k, y - dp(3) * k, w + dp(6) * k, h + dp(6) * k, dp(12) + dp(2) * k),
                     width=1.2)
            Color(GOLD[0], GOLD[1], GOLD[2], 0.9)
            Line(rounded_rectangle=(x, y, w, h, dp(10)), width=1.6)

    def _brilhar(self, *a):
        for c, base in self._cores:
            c.a = base * (0.5 + 1.0 * self.brilho)


class CelulaCarta(ButtonBehavior, BoxLayout):
    """Miniatura de carta na grade (moldura dourada + nome)."""

    def __init__(self, imagem, nome, **kw):
        kw.setdefault('orientation', 'vertical')
        kw.setdefault('padding', dp(5))
        kw.setdefault('spacing', dp(3))
        super().__init__(**kw)
        self.add_widget(imagem)
        lb = Label(text=nome, markup=True, font_size=sp(10), color=TXT, halign='center', valign='middle',
                   size_hint_y=None, height=dp(30), font_name=FONTE_TITULO)
        lb.bind(size=lambda i, s: setattr(i, 'text_size', s))
        self.add_widget(lb)
        with self.canvas.before:
            Color(*SURF)
            self._fundo = RoundedRectangle(radius=[dp(8)])
            self._cor = Color(GOLD[0], GOLD[1], GOLD[2], 0.4)
            self._borda = Line(rounded_rectangle=(0, 0, 0, 0, dp(8)), width=1.1)
        self.bind(pos=self._atualiza, size=self._atualiza)

    def _atualiza(self, *a):
        self._fundo.pos, self._fundo.size = self.pos, self.size
        self._borda.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(8))

    def on_press(self):
        self._cor.a = 1
        Animation(opacity=0.75, d=0.08).start(self)

    def on_release(self):
        self._cor.a = 0.4
        Animation(opacity=1, d=0.25).start(self)
