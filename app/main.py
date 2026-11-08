# -*- coding: utf-8 -*-
"""ARCANUM VITAE - Grimório do Iniciado (v2.2)

Aplicativo de consulta do jogo de tabuleiro híbrido Arcanum Vitae.
Visual: cartografia celeste + Tarot + identidade DEVA. Somente Kivy (sem KivyMD).

Imagens: cartas Rider-Waite-Smith (domínio público, Wikimedia Commons).
Ordem de busca: assets/cartas -> cache do app -> download.
"""
import os
import sys
from collections import deque

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import arvore  # noqa: E402
from cartas import CARTAS, ORDEM_MENORES, id_maior, id_menor  # noqa: E402
from dados_jogo import ARCANOS_MAIORES, ARCANOS_MENORES, RECURSOS, SEPHIROTH  # noqa: E402
from dados_tarot import MANUAL, MAIORES_TAROT, MENORES_TAROT  # noqa: E402
from estilo import (ASSETS, BAD, CEL, DEVA, FONTE_TITULO, GOLD, LOGO, OK, TXT, TXT2,  # noqa: E402
                    VOID, hexc)
from regras_texto import NAIPES_INFO, NOTA_REALEZA, SECOES, ZONAS_TEXTO  # noqa: E402
from widgets import (AnelCeleste, BarraTopo, BotaoDeva, Cartao, CelulaCarta, Divisor,  # noqa: E402
                     Fundo, ImgFlip, MapaArvore, Moldura, legenda, revelar, rotulo, titulo)

VERSAO = '2.2'
UA = "ArcanumVitaeApp/2.2 (jogo de tabuleiro; Kivy)"
MAX_DOWNLOADS = 4

if platform not in ('android', 'ios'):
    Window.size = (360, 640)
Window.clearcolor = VOID


# ---------------------------------------------------------------- imagens
class GerenciadorImagens:
    """Resolve imagens das cartas: assets locais -> cache -> download (Commons)."""

    def __init__(self, pasta_cache):
        self.assets = os.path.join(ASSETS, 'cartas')
        self.cache = pasta_cache
        os.makedirs(self.cache, exist_ok=True)
        self.espera = {}
        self.fila = deque()
        self.ativos = set()

    def caminho(self, cid):
        nome = CARTAS[cid]['arq_local']
        for pasta in (self.assets, self.cache):
            p = os.path.join(pasta, nome)
            if os.path.isfile(p) and os.path.getsize(p) > 2000:
                return p
        return None

    def obter(self, cid, ao_pronto):
        p = self.caminho(cid)
        if p:
            ao_pronto(p)
            return
        self.espera.setdefault(cid, []).append(ao_pronto)
        if cid not in self.ativos and cid not in self.fila:
            self.fila.append(cid)
            self._proximo()

    def _proximo(self):
        while self.fila and len(self.ativos) < MAX_DOWNLOADS:
            cid = self.fila.popleft()
            self.ativos.add(cid)
            self._baixar(cid)

    def _baixar(self, cid):
        info = CARTAS[cid]
        final = os.path.join(self.cache, info['arq_local'])
        tmp = final + '.part'
        if os.path.exists(tmp):
            os.remove(tmp)

        def terminou(ok):
            self.ativos.discard(cid)
            if ok:
                for cb in self.espera.pop(cid, []):
                    cb(final)
            self._proximo()

        def sucesso(req, res):
            try:
                with open(tmp, 'rb') as f:
                    valido = f.read(3) == b'\xff\xd8\xff'
                if valido:
                    os.replace(tmp, final)
                else:
                    os.remove(tmp)
                terminou(valido)
            except OSError:
                terminou(False)

        def falha(req, err):
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
            terminou(False)

        UrlRequest(info['url'], file_path=tmp, on_success=sucesso, on_failure=falha,
                   on_error=falha, req_headers={'User-Agent': UA}, timeout=30)


# ---------------------------------------------------------------- telas
class Pagina(Screen):
    """Tela de conteúdo: céu estrelado + barra superior + área rolável."""

    def __init__(self, ao_voltar, **kw):
        super().__init__(**kw)
        raiz = FloatLayout()
        raiz.add_widget(Fundo())
        col = BoxLayout(orientation='vertical')
        self.barra = BarraTopo(ao_voltar)
        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(3), scroll_type=['bars', 'content'],
                                 bar_color=(GOLD[0], GOLD[1], GOLD[2], 0.5),
                                 bar_inactive_color=(GOLD[0], GOLD[1], GOLD[2], 0.15))
        self.caixa = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12),
                               padding=[dp(16), dp(14), dp(16), dp(28)])
        self.caixa.bind(minimum_height=lambda i, h: setattr(i, 'height', h))
        self.scroll.add_widget(self.caixa)
        col.add_widget(self.barra)
        col.add_widget(self.scroll)
        raiz.add_widget(col)
        self.add_widget(raiz)

    def montar(self, titulo_barra, widgets):
        self.barra.definir(titulo_barra)
        self.caixa.clear_widgets()
        for w in widgets:
            self.caixa.add_widget(w)
        self.scroll.scroll_y = 1
        revelar(widgets)


class TelaHome(Screen):
    """Capa animada: céu que cintila, anel zodiacal que gira, Árvore da Vida pulsando."""

    def __init__(self, ao_ascender, **kw):
        super().__init__(**kw)
        f = FloatLayout()
        f.add_widget(Fundo(animado=True))
        f.add_widget(AnelCeleste(size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.44}))
        f.add_widget(MapaArvore(rotulos=False, margem=0.12, size_hint=(0.9, 0.54),
                                pos_hint={'center_x': 0.5, 'center_y': 0.44}, opacity=0.6))
        self.logo = Image(source=LOGO, fit_mode='contain', size_hint=(0.9, 0.24),
                          pos_hint={'center_x': 0.5, 'center_y': 0.865})
        self.sub = legenda("A ascensão da Árvore da Vida", CEL, 'center')
        self.sub.pos_hint = {'center_x': 0.5, 'y': 0.728}
        self.botao = BotaoDeva("Ascender", size_hint=(0.66, None), pos_hint={'center_x': 0.5, 'y': 0.095})
        self.botao.bind(on_release=lambda *_: ao_ascender())
        selo = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(120), dp(54)),
                         pos_hint={'center_x': 0.5, 'y': 0.006}, spacing=dp(2))
        selo.add_widget(Image(source=os.path.join(DEVA, 'deva-sigilo-180.png'), fit_mode='contain'))
        selo.add_widget(legenda("DEVA ARCHIVE", CEL, 'center'))
        self.selo = selo
        for w in (self.logo, self.sub, self.botao, selo):
            f.add_widget(w)
        self.add_widget(f)

    def on_enter(self, *a):
        for i, w in enumerate((self.logo, self.sub, self.botao, self.selo)):
            w.opacity = 0
            Clock.schedule_once(lambda dt, w=w: Animation(opacity=1, d=0.9, t='out_quad').start(w),
                                0.15 + i * 0.22)
        self.botao.pulsar()


# ---------------------------------------------------------------- app
class ArcanumApp(App):

    def build(self):
        self.title = "Arcanum Vitae"
        self.icon = LOGO
        self.imagens = GerenciadorImagens(os.path.join(self.user_data_dir, 'cartas'))
        self._direcao = 'left'
        self._voltar_atual = None
        self._par = 0
        self.sm = ScreenManager(transition=SlideTransition(duration=0.3))
        self.sm.add_widget(TelaHome(self.menu, name='home'))
        self.paginas = [Pagina(self.voltar, name='a'), Pagina(self.voltar, name='b')]
        for p in self.paginas:
            self.sm.add_widget(p)
        Window.bind(on_keyboard=self._tecla)
        return self.sm

    def _tecla(self, janela, tecla, *a):
        if tecla == 27 and self.sm.current != 'home':  # botão voltar do Android / Esc
            self.voltar()
            return True
        return False

    def voltar(self):
        if self._voltar_atual:
            self._direcao = 'right'
            self._voltar_atual()

    def home(self):
        self._direcao = 'right'
        self._voltar_atual = None
        self.sm.transition.direction = 'right'
        self.sm.current = 'home'
        self._direcao = 'left'

    def mostrar(self, titulo_barra, voltar_fn, widgets):
        flat = []
        for w in widgets:
            flat.extend(w if isinstance(w, list) else [w])
        self._voltar_atual = voltar_fn
        self._par = 1 - self._par
        pag = self.paginas[self._par]
        pag.montar(titulo_barra, flat)
        self.sm.transition.direction = self._direcao
        self.sm.current = pag.name
        self._direcao = 'left'

    @staticmethod
    def cab(texto):
        return [titulo(texto), Divisor()]

    @staticmethod
    def selo_deva():
        bloco = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70), spacing=dp(2))
        bloco.add_widget(Image(source=os.path.join(DEVA, 'deva-sigilo-180.png'), fit_mode='contain'))
        bloco.add_widget(legenda("DEVA ARCHIVE", CEL, 'center'))
        return bloco

    # -------- menu
    def menu(self):
        w = [
            self.cab("Grimório do Iniciado"),
            BotaoDeva("Regras", self.regras),
            BotaoDeva("Tabuleiro", self.tabuleiro),
            BotaoDeva("Sephiroth", self.sephiroth),
            BotaoDeva("Arcanos", self.selecao_arcanos),
            BotaoDeva("Recursos & Ações", self.recursos),
            BotaoDeva("Tarot", self.tarot),
            BotaoDeva("Créditos", self.creditos, primario=False),
            Divisor(),
            self.selo_deva(),
        ]
        self.mostrar("Arcanum Vitae", self.home, w)

    # -------- regras
    def regras(self):
        w = self.cab("Regras Sagradas")
        w.append(rotulo("Escolha uma seção. Os efeitos de cada carta estão em Arcanos; os custos das esferas em Sephiroth.",
                        13, TXT2))
        for i, (tit, _) in enumerate(SECOES):
            w.append(BotaoDeva(tit, lambda i=i: self.regra_secao(i)))
        self.mostrar("Regras", self.menu, w)

    def regra_secao(self, i):
        tit, paragrafos = SECOES[i]
        c = Cartao()
        for p in paragrafos:
            c.add_widget(rotulo(p, 15))
        w = self.cab(tit) + [c]
        nav = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        if i > 0:
            nav.add_widget(BotaoDeva("Anterior", lambda: self._ir_secao(i - 1, 'right'), primario=False))
        if i < len(SECOES) - 1:
            nav.add_widget(BotaoDeva("Próxima", lambda: self._ir_secao(i + 1, 'left')))
        w.append(nav)
        self.mostrar("Regras", self.regras, w)

    def _ir_secao(self, i, direcao):
        self._direcao = direcao
        self.regra_secao(i)

    # -------- tabuleiro (mapa celeste interativo)
    def tabuleiro(self):
        w = self.cab("A Árvore da Vida")
        w.append(MapaArvore(interativo=True, ao_tocar=self.sephira_detalhe, size_hint_y=None, height=dp(440)))
        w.append(legenda("Toque em uma esfera para ver custo e recompensa", TXT2, 'center'))
        w.append(Divisor())
        caminho = os.path.join(ASSETS, 'tabuleiro.jpg')
        if os.path.exists(caminho):
            img = Image(source=caminho, fit_mode='contain', size_hint_y=None)
            img.bind(width=lambda i, wd: setattr(i, 'height', wd * 1.34))
            w.append(img)
        w.append(rotulo("[b]Esferas (Sephiroth):[/b] círculos. Zonas seguras, sem carta. Só se entra com número exato.", 14))
        w.append(rotulo("[b]Caminhos (Arcanos Maiores):[/b] casas que ligam as esferas. Zonas de perigo.", 14))
        c = Cartao()
        c.add_widget(legenda("Zonas das Esferas"))
        for z, esf in ZONAS_TEXTO:
            c.add_widget(rotulo(f"[b]{z}:[/b] {esf}", 14))
        c.add_widget(rotulo("Os Caminhos têm Níveis 1 a 4 nas mesmas faixas (cada Caminho pertence ao Nível da mais "
                            "alta das duas Esferas que liga). Ataques atingem o mesmo Nível/Zona ou o adjacente. "
                            "Reis e Rainhas: alcance global.", 13, TXT2))
        w.append(c)
        self.mostrar("Tabuleiro", self.menu, w)

    def sephira_detalhe(self, nome):
        s = next(x for x in SEPHIROTH if x['nome'] == nome)
        cor = CEL if s['zona'] == 4 else GOLD
        c = Cartao(realce=cor)
        c.add_widget(rotulo(f"{s['nome'].upper()}  ·  {s['sub']}", 20, cor, False, 'left', FONTE_TITULO))
        c.add_widget(legenda(f"Esfera {s['ordem']} de 10 · Zona {s['zona']}"))
        c.add_widget(rotulo(f"[b]Requisito / custo:[/b] {s['requisito']}", 15))
        c.add_widget(rotulo(f"[b]Recompensa:[/b] {s['recompensa']}", 15))
        liga = ", ".join(arvore.vizinhos(nome))
        c.add_widget(rotulo(f"[b]Caminhos ligam a:[/b] {liga}.", 13, TXT2))
        w = self.cab(nome) + [c, rotulo("Em qualquer esfera vale o Mercado Universal: 3 Recursos quaisquer por 1 à escolha.", 13, TXT2)]
        self.mostrar(nome, self.tabuleiro, w)

    # -------- sephiroth
    def sephiroth(self):
        w = self.cab("As Esferas (Sephiroth)")
        w.append(rotulo("Zonas seguras. Ao parar em uma esfera não se saca carta. Pague o custo para consagrar e "
                        "ganhar a recompensa. Do início (Malkuth) ao fim (Keter).", 13, TXT2))
        for s in SEPHIROTH:
            cor = CEL if s['zona'] == 4 else GOLD
            c = Cartao(realce=cor)
            c.add_widget(rotulo(f"{s['nome'].upper()}  ·  {s['sub']}", 17, cor, False, 'left', FONTE_TITULO))
            c.add_widget(legenda(f"Esfera {s['ordem']} de 10 · Zona {s['zona']}"))
            c.add_widget(rotulo(f"[b]Requisito / custo:[/b] {s['requisito']}", 14))
            c.add_widget(rotulo(f"[b]Recompensa:[/b] {s['recompensa']}", 14))
            w.append(c)
        c = Cartao()
        c.add_widget(legenda("Mercado Universal"))
        c.add_widget(rotulo("Em qualquer esfera: troque 3 Recursos quaisquer por 1 Recurso à escolha.", 14))
        w.append(c)
        self.mostrar("Sephiroth", self.menu, w)

    # -------- recursos
    def recursos(self):
        w = self.cab("Recursos & Ações")
        w.append(rotulo("Gaste Tokens na Fase Tática ou como Reação (defesa). Máximo de 5 de cada tipo por jogador.", 14, TXT2))
        for chave, r in zip(['paus', 'copas', 'espadas', 'ouros'], RECURSOS):
            cor = hexc(NAIPES_INFO[chave]['cor'])
            c = Cartao(realce=cor)
            linha = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(72), spacing=dp(10))
            tok = os.path.join(ASSETS, 'tokens', f'token_{chave}.png')
            if os.path.exists(tok):
                linha.add_widget(Image(source=tok, fit_mode='contain', size_hint_x=None, width=dp(72)))
            linha.add_widget(rotulo(r['nome'].upper(), 18, cor, False, 'left', FONTE_TITULO))
            c.add_widget(linha)
            c.add_widget(legenda("Custo: 1 Token", GOLD))
            for nome, txt in r['um']:
                c.add_widget(rotulo(f"[b]{nome}:[/b] {txt}", 14))
            c.add_widget(legenda("Custo: 2 Tokens", GOLD))
            for nome, txt in r['dois']:
                c.add_widget(rotulo(f"[b]{nome}:[/b] {txt}", 14))
            w.append(c)
        self.mostrar("Recursos & Ações", self.menu, w)

    # -------- arcanos (jogo)
    def selecao_arcanos(self):
        w = self.cab("Escolha o Caminho")
        w.append(BotaoDeva("Arcanos Maiores · 22 caminhos", lambda: self.grade('maior', 'jogo')))
        for chave in ('paus', 'copas', 'espadas', 'ouros'):
            w.append(BotaoDeva(f"{chave} · desafios", lambda c=chave: self.grade(c, 'jogo'), primario=False))
        self.mostrar("Arcanos", self.menu, w)

    # -------- grade de cartas
    def grade(self, categoria, modo):
        voltar = self.selecao_arcanos if modo == 'jogo' else self.selecao_tarot
        if categoria == 'maior':
            if modo == 'jogo':
                lista = sorted(ARCANOS_MAIORES, key=lambda m: m['num'])
                itens = [(id_maior(m['chave']), f"{m['numeral']}\n{m['nome']}") for m in lista]
                intro = "Cada Arcano Maior rege um caminho. Toque para ver a Regra Ambiental."
            else:
                lista = sorted(ARCANOS_MAIORES, key=lambda m: m['rws_num'])
                itens = [(id_maior(m['chave']), f"{CARTAS[id_maior(m['chave'])]['numeral_rws']}\n{m['nome']}")
                         for m in lista]
                intro = "Toque em uma carta para ver o significado."
            barra = "Arcanos Maiores"
        else:
            info = NAIPES_INFO[categoria]
            itens = [(id_menor(categoria, r), r) for r in ORDEM_MENORES]
            barra = CARTAS[id_menor(categoria, 'Ás')]['nome_pt'].replace('Ás de ', '')
            intro = (f"[b]Tema:[/b] {info['tema']}\n[b]Recompensa:[/b] {info['recompensa']}" if modo == 'jogo'
                     else f"[b]Tema:[/b] {info['tema']}")
        grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, row_default_height=dp(196),
                          row_force_default=True)
        grid.bind(minimum_height=lambda i, h: setattr(i, 'height', h))
        celulas = []
        for cid, nome in itens:
            img = ImgFlip(source=LOGO)
            self.imagens.obter(cid, lambda p, i=img: setattr(i, 'source', p))
            cel = CelulaCarta(img, nome, size_hint_y=None, height=dp(196))
            cel.bind(on_release=lambda x, c=cid: self.detalhe(c, modo, categoria))
            grid.add_widget(cel)
            celulas.append(cel)
        w = self.cab(barra) + [rotulo(intro, 14, TXT2), grid]
        self.mostrar(barra, voltar, w)
        revelar(celulas, atraso=0.035, inicio=0.25, limite=24)

    # -------- detalhe de carta
    def moldura_carta(self, cid):
        cont = FloatLayout(size_hint_y=None, height=dp(440))
        caixa = dict(size_hint=(0.6, 0.86), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        cont.add_widget(Moldura(**caixa))
        img = ImgFlip(source=LOGO, **caixa)
        cont.add_widget(img)
        estado = {'ok': False}

        def pronto(p):
            estado['ok'] = True
            img.source = p
            img.virar(0.6, 0.3)  # a carta é revelada ao virar

        self.imagens.obter(cid, pronto)
        return cont

    def detalhe(self, cid, modo, categoria):
        info = CARTAS[cid]
        voltar = lambda: self.grade(categoria, modo)  # noqa: E731
        if info['tipo'] == 'maior':
            numeral = info['numeral_jogo'] if modo == 'jogo' else info['numeral_rws']
            nome_topo = f"{numeral} · {info['nome_pt']}"
        else:
            nome_topo = info['nome_pt']
        w = [titulo(nome_topo), legenda(info['nome_en']), Divisor(), self.moldura_carta(cid)]
        w.extend(self._texto_jogo(info) if modo == 'jogo' else self._texto_tarot(info))
        self.mostrar(info['nome_pt'], voltar, w)

    def _texto_jogo(self, info):
        out = []
        if info['tipo'] == 'maior':
            m = next(x for x in ARCANOS_MAIORES if x['chave'] == info['chave'])
            c = Cartao(realce=GOLD)
            c.add_widget(legenda("Regra Ambiental", GOLD))
            c.add_widget(rotulo(f"[b]{m['regra_titulo']}[/b]", 17, GOLD, False, 'left', FONTE_TITULO))
            c.add_widget(rotulo(m['regra'], 15))
            out.append(c)
            out.append(rotulo("Enquanto o peão estiver neste caminho a regra vale. Caminhos Padrão (Níveis 1 a 3): "
                              "1 carta de desafio. Caminhos Críticos (Nível 4, Abismo): 2 cartas.", 12, TXT2))
        else:
            dados = next(x for x in ARCANOS_MENORES[info['naipe']] if x['carta'] == info['carta'])
            ni = NAIPES_INFO[info['naipe']]
            ca = Cartao(realce=OK)
            ca.add_widget(legenda("Opção A · Avanço Pessoal", OK))
            ca.add_widget(rotulo(f"[b]{dados['a'][0]}[/b]", 17, OK, False, 'left', FONTE_TITULO))
            ca.add_widget(rotulo(dados['a'][1], 15))
            out.append(ca)
            cb = Cartao(realce=BAD)
            cb.add_widget(legenda(f"Opção B · {ni['opb']}", BAD))
            cb.add_widget(rotulo(f"[b]{dados['b'][0]}[/b]", 17, BAD, False, 'left', FONTE_TITULO))
            cb.add_widget(rotulo(dados['b'][1], 15))
            out.append(cb)
            corte = info['carta'] in ('Valete', 'Cavaleiro', 'Rainha', 'Rei')
            if corte:
                out.append(rotulo(NOTA_REALEZA, 12, TXT2))
            out.append(rotulo(f"[b]Teste:[/b] role 1d6, 4 ou mais vence. [b]Vitória:[/b] {'2 Tokens' if corte else '1 Token'} "
                              f"de {ni['recompensa']} e 1 PV. [b]Falha:[/b] sem prêmio, recua 1d4 (nunca além da Esfera "
                              "de origem) e perde a vez. Declare A ou B em voz alta antes de rolar.", 12, TXT2))
        return out

    def _texto_tarot(self, info):
        if info['tipo'] == 'maior':
            kw, up, rev = MAIORES_TAROT[info['chave']]
        else:
            kw, up, rev = MENORES_TAROT[info['naipe']][ORDEM_MENORES.index(info['carta'])]
        c = Cartao(realce=GOLD)
        c.add_widget(rotulo(kw, 16, GOLD, False, 'left', FONTE_TITULO))
        c.add_widget(legenda("Em pé", OK))
        c.add_widget(rotulo(up, 15))
        c.add_widget(legenda("Invertida", BAD))
        c.add_widget(rotulo(rev, 15))
        return [c]

    # -------- tarot
    def tarot(self):
        w = self.cab("Leitura de Tarot")
        w.append(rotulo("Baralho Rider-Waite-Smith. Aprenda o básico e consulte o significado das 78 cartas.", 14, TXT2))
        w.append(BotaoDeva("Manual básico de leitura", self.tarot_manual))
        w.append(BotaoDeva("Significado das cartas", self.selecao_tarot))
        self.mostrar("Tarot", self.menu, w)

    def tarot_manual(self):
        w = self.cab("Manual Básico de Leitura")
        for i, (tit, _) in enumerate(MANUAL):
            w.append(BotaoDeva(tit, lambda i=i: self.tarot_secao(i)))
        self.mostrar("Manual de Tarot", self.tarot, w)

    def tarot_secao(self, i):
        tit, paragrafos = MANUAL[i]
        c = Cartao()
        for p in paragrafos:
            c.add_widget(rotulo(p, 15))
        w = self.cab(tit) + [c]
        nav = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        if i > 0:
            nav.add_widget(BotaoDeva("Anterior", lambda: self._ir_tarot(i - 1, 'right'), primario=False))
        if i < len(MANUAL) - 1:
            nav.add_widget(BotaoDeva("Próxima", lambda: self._ir_tarot(i + 1, 'left')))
        w.append(nav)
        self.mostrar("Manual de Tarot", self.tarot_manual, w)

    def _ir_tarot(self, i, direcao):
        self._direcao = direcao
        self.tarot_secao(i)

    def selecao_tarot(self):
        w = self.cab("Significado das Cartas")
        w.append(BotaoDeva("Arcanos Maiores · 22", lambda: self.grade('maior', 'tarot')))
        for chave in ('paus', 'copas', 'espadas', 'ouros'):
            w.append(BotaoDeva(f"{chave} · 14", lambda c=chave: self.grade(c, 'tarot'), primario=False))
        self.mostrar("Tarot", self.tarot, w)

    # -------- créditos
    def creditos(self):
        logo = Image(source=os.path.join(DEVA, 'deva-lockup-vertical.png'), fit_mode='contain',
                     size_hint_y=None, height=dp(230))
        w = [logo,
             rotulo(f"ARCANUM VITAE · v{VERSAO}", 17, GOLD, False, 'center', FONTE_TITULO),
             legenda("DEVA ARCHIVE // Grimório do Iniciado", CEL, 'center'),
             Divisor(),
             rotulo("Projetado e desenvolvido por Vitor Araújo sob o ecossistema DEVA.", 15, TXT, False, 'center'),
             rotulo("Ilustrações das cartas: Pamela Colman Smith, baralho Rider-Waite-Smith (1909), domínio público, "
                    "via Wikimedia Commons.", 13, TXT2, False, 'center'),
             legenda("github.com/jvitoraraujo", CEL, 'center')]
        self.mostrar("Créditos", self.menu, w)


if __name__ == '__main__':
    ArcanumApp().run()
