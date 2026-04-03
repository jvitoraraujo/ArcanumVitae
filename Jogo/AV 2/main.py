from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
import os
import unicodedata

# Configuração de Janela
Window.size = (360, 640)

# --- DADOS E REGRAS ---
# [cite_start]Regras Gerais (Resumidas do PDF [cite: 4-156])
REGRAS_TEXTO = """
[b][size=20]ARCANUM VITAE - REGRAS[/size][/b]

[b]OBJETIVO[/b]
Chegar à Coroa (Keter) iluminado. Vence quem tiver mais Sabedoria (PV).

[b]COMO JOGAR[/b]
1. Comece em Malkuth com 2 recursos.
2. Role o dado e mova.
3. Se parar num Caminho (Carta): Resolva o desafio.
4. Se parar numa Esfera (Bola): Use o Mercado.

[b]COMBATE[/b]
Ao sacar uma carta de desafio, escolha:
[color=88FF88]Opção A (Avanço):[/color] Benefício próprio.
[color=FF8888]Opção B (Ataque):[/color] Prejudicar oponente.
"""

ARCANOS_MAIORES = {
    "0": {"nome": "0 O Louco", "desc": "Se falhar aqui, volta para o início do caminho."},
    "1": {"nome": "I O Mago", "desc": "Pode descartar 1 Recurso para Sucesso Automático."},
    "2": {"nome": "II A Papisa", "desc": "Adivinhe se vai vencer ou perder. Se acertar, +1 casa."},
    "3": {"nome": "III A Imperatriz", "desc": "Se vencer, recupera recursos gastos."},
    "4": {"nome": "IV O Imperador", "desc": "Ouros dão +2 Movimento. Copas causam recuo dobrado."},
    "5": {"nome": "V O Papa", "desc": "Pague 1 PV para entrar. Recursos ganhos dobram."},
    "6": {"nome": "VI Os Enamorados", "desc": "Saque 2 cartas: enfrente uma, dê a outra ao oponente."},
    "7": {"nome": "VII O Carro", "desc": "Vitória move você direto para a próxima Esfera."},
    "8": {"nome": "VIII A Justiça", "desc": "Proibido usar itens ou bônus aqui."},
    "9": {"nome": "IX O Eremita", "desc": "Imune a ataques de oponentes."},
    "10": {"nome": "X Roda da Fortuna", "desc": "Par: 1 carta. Ímpar: 2 cartas (prêmio dobro)."},
    "11": {"nome": "XI A Força", "desc": "Paus dá dobro de recurso e ignora recuo."},
    "12": {"nome": "XII O Pendurado", "desc": "Se falhar ganha PV. Se vencer ganha só recurso."},
    "13": {"nome": "XIII A Morte", "desc": "Falha custa 1 Recurso extra."},
    "14": {"nome": "XIV A Temperança", "desc": "Vencer naipes opostos dá +2 PV."},
    "15": {"nome": "XV O Diabo", "desc": "Saque 2 cartas. Pague 1 Ouro para pular a segunda."},
    "16": {"nome": "XVI A Torre", "desc": "Falha expulsa para o início. Espadas é falha auto se não pagar."},
    "17": {"nome": "XVII A Estrela", "desc": "Falha não recua casas, apenas perde a vez."},
    "18": {"nome": "XVIII A Lua", "desc": "Cartas ocultas. Pague para ver."},
    "19": {"nome": "XIX O Sol", "desc": "Sucesso avança +1 casa extra."},
    "20": {"nome": "XX O Julgamento", "desc": "Pode enfrentar carta do descarte."},
    "21": {"nome": "XXI O Mundo", "desc": "Vitória dá 1 Recurso Extra qualquer."}
}

ARCANOS_MENORES = {
    "Paus": {
        "Ás": "A: Arrancada (+2 casas)\nB: Empurrão (Oponente recua 1)",
        "2": "A: Foco (+1 casa se tiver Paus)\nB: Duelo (Dados)",
        "3": "A: Expansão (Ganha 1 Paus)\nB: Desarme (Oponente perde 1 Paus)",
        "4": "A: Abrigo (Imune)\nB: Bloqueio (Oponente sem bônus)",
        "5": "A: Treino (Role 4+ p/ andar)\nB: Briga (Perde PV)",
        "6": "A: Vitória (Pula casas)\nB: Inversão (Troca lugar)",
        "7": "A: Bravura (+1 PV)\nB: Barreira (Bloqueia passagem)",
        "8": "A: Pressa (Rola de novo)\nB: Atraso (Líder perde vez)",
        "9": "A: Resiliência (Defesa)\nB: Intimidação (Recua 2)",
        "10": "A: Sobrecarga (Troca Rec por PV)\nB: Peso (Descarta 2)",
        "Valete": "A: Mensageiro\nB: Interferência",
        "Cavaleiro": "A: Galope (+3 casas)\nB: Atropelar",
        "Rainha": "A: Carisma\nB: Comando",
        "Rei": "A: Autoridade\nB: Deslocar"
    },
    "Copas": { # Abreviado para o exemplo, preencha conforme manual anterior se desejar texto completo
        "Ás": "A: Purificação\nB: Chantagem",
        "2": "A: Parceria\nB: Vínculo",
        "3": "A: Celebração\nB: Exclusão",
        "4": "A: Meditação\nB: Apatia",
        "5": "A: Sacrifício\nB: Culpa",
        "6": "A: Nostalgia\nB: Regresso",
        "7": "A: Sonho\nB: Ilusão",
        "8": "A: Abandono\nB: Desapego",
        "9": "A: Desejo\nB: Gula",
        "10": "A: Família\nB: Isolamento",
        "Valete": "A: Intuição\nB: Fofoca",
        "Cavaleiro": "A: Oferta\nB: Sedução",
        "Rainha": "A: Compaixão\nB: Vampirismo",
        "Rei": "A: Equilíbrio\nB: Veto"
    },
    "Espadas": {
        "Ás": "A: Ideia\nB: Plágio",
        "2": "A: Cegueira\nB: Escuridão",
        "3": "A: Dor\nB: Traição",
        "4": "A: Descanso\nB: Sono",
        "5": "A: Aceitação\nB: Vitória Vazia",
        "6": "A: Navegação\nB: Desvio",
        "7": "A: Astúcia\nB: Furtividade",
        "8": "A: Prisão\nB: Cela",
        "9": "A: Ansiedade\nB: Pesadelo",
        "10": "A: Renascimento\nB: Ruína",
        "Valete": "A: Espião\nB: Calúnia",
        "Cavaleiro": "A: Investida\nB: Ataque Rápido",
        "Rainha": "A: Crítica\nB: Silêncio",
        "Rei": "A: A Lei\nB: O Juiz"
    },
    "Ouros": {
        "Ás": "A: Lucro\nB: Taxa",
        "2": "A: Câmbio\nB: Inflação",
        "3": "A: Obra\nB: Pedágio",
        "4": "A: Apego\nB: Falência",
        "5": "A: Caridade\nB: Confisco",
        "6": "A: Doação\nB: Burocracia",
        "7": "A: Investimento\nB: Servidão",
        "8": "A: Trabalho\nB: Imposto",
        "9": "A: Herdeiro\nB: Auditoria",
        "10": "A: Legado\nB: Herança",
        "Valete": "A: Estágio\nB: Estagnação",
        "Cavaleiro": "A: Segurança\nB: Custo de Vida",
        "Rainha": "A: Conforto\nB: Monopólio",
        "Rei": "A: Poder\nB: Compra Hostil"
    }
}

# KV Language
KV = """
#:import Window kivy.core.window.Window

<BaseScreen@Screen>:
    canvas.before:
        Color:
            rgba: 0.1, 0.08, 0.08, 1  # Fundo quase preto para ressaltar as cartas
        Rectangle:
            pos: self.pos
            size: self.size

<CustomButton@MDFillRoundFlatButton>:
    md_bg_color: 0.45, 0.35, 0.25, 1 
    text_color: 0.95, 0.9, 0.8, 1
    font_size: "18sp"

<HomeScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20
        alignment: {'center_x': 0.5, 'center_y': 0.5}
        
        Image:
            source: 'logo.png'
            size_hint: (1, 0.5)
            allow_stretch: True
            
        MDLabel:
            text: "ARCANUM VITAE"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.8, 0.7, 0.5, 1
            font_style: "H4"
            bold: True
            
        MDRaisedButton:
            text: "ASCENDER"
            font_size: "24sp"
            size_hint: (0.8, None)
            height: "60dp"
            md_bg_color: 0.6, 0.5, 0.3, 1
            text_color: 0.1, 0.1, 0.1, 1
            on_release: app.root.current = 'menu'

<MenuScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(25)
        alignment: {'center_x': 0.5, 'center_y': 0.5}

        MDLabel:
            text: "Grimório do Iniciado"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.8, 0.7, 0.5, 1
            font_style: "H5"

        CustomButton:
            text: "REGRAS"
            size_hint_x: 0.9
            on_release: app.root.current = 'rules'

        CustomButton:
            text: "ARCANOS"
            size_hint_x: 0.9
            on_release: app.root.current = 'arcana_select'

        CustomButton:
            text: "TAROT"
            size_hint_x: 0.9
            on_release: app.root.current = 'tarot'
            
        MDRaisedButton:
            text: "Voltar"
            md_bg_color: 0.2, 0.2, 0.2, 1
            on_release: app.root.current = 'home'

<RulesScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Regras Sagradas"
            left_action_items: [["arrow-left", lambda x: app.change_screen('menu')]]
            md_bg_color: 0.25, 0.22, 0.18, 1
        
        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                adaptive_height: True
                MDLabel:
                    text: root.rules_text
                    markup: True
                    theme_text_color: "Custom"
                    text_color: 0.9, 0.85, 0.75, 1
                    size_hint_y: None
                    height: self.texture_size[1]

<ArcanaSelectScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 40
        alignment: {'center_x': 0.5, 'center_y': 0.5}

        MDLabel:
            text: "Escolha o Caminho"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.8, 0.7, 0.5, 1
            font_style: "H5"

        CustomButton:
            text: "ARCANOS MAIORES"
            size_hint_x: 1
            on_release: app.show_grid("Maior")

        MDGridLayout:
            cols: 2
            spacing: 20
            size_hint: (1, None)
            height: "200dp"

            CustomButton:
                text: "PAUS"
                on_release: app.show_grid("Paus")
            CustomButton:
                text: "COPAS"
                on_release: app.show_grid("Copas")
            CustomButton:
                text: "ESPADAS"
                on_release: app.show_grid("Espadas")
            CustomButton:
                text: "OUROS"
                on_release: app.show_grid("Ouros")
        
        MDRaisedButton:
            text: "Voltar"
            md_bg_color: 0.2, 0.2, 0.2, 1
            on_release: app.root.current = 'menu'

<CardGridScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: root.suit_title
            left_action_items: [["arrow-left", lambda x: app.change_screen('arcana_select')]]
            md_bg_color: 0.25, 0.22, 0.18, 1
        
        MDScrollView:
            MDGridLayout:
                id: grid
                cols: 3
                padding: dp(10)
                spacing: dp(15)
                adaptive_height: True
                row_default_height: dp(180) # Altura maior para caber a carta
                row_force_default: True

<CardDetailScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        
        MDTopAppBar:
            title: root.card_name
            left_action_items: [["arrow-left", lambda x: app.back_to_grid()]]
            md_bg_color: 0.25, 0.22, 0.18, 1

        MDBoxLayout:
            size_hint_y: 0.55
            padding: dp(20)
            Image:
                source: root.image_source
                allow_stretch: True
            
        MDScrollView:
            MDBoxLayout:
                padding: dp(20)
                adaptive_height: True
                MDLabel:
                    text: root.card_rules
                    markup: True
                    theme_text_color: "Custom"
                    text_color: 0.9, 0.85, 0.75, 1
                    font_style: "Body1"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]

<TarotScreen>:
    BaseScreen:
    MDBoxLayout:
        orientation: 'vertical'
        alignment: {'center_x': 0.5, 'center_y': 0.5}
        padding: 40
        MDLabel:
            text: "Em breve: guia de leitura."
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.8, 0.7, 0.5, 1
        MDRaisedButton:
            text: "Voltar"
            on_release: app.root.current = 'menu'
"""

class HomeScreen(Screen): pass
class MenuScreen(Screen): pass
class RulesScreen(Screen):
    rules_text = StringProperty(REGRAS_TEXTO)
class ArcanaSelectScreen(Screen): pass
class CardGridScreen(Screen):
    suit_title = StringProperty("")
class CardDetailScreen(Screen):
    card_name = StringProperty("")
    card_rules = StringProperty("")
    image_source = StringProperty("")
class TarotScreen(Screen): pass

class ArcanumApp(MDApp):
    current_suit = "" 

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RulesScreen(name='rules'))
        sm.add_widget(ArcanaSelectScreen(name='arcana_select'))
        sm.add_widget(CardGridScreen(name='card_grid'))
        sm.add_widget(CardDetailScreen(name='card_detail'))
        sm.add_widget(TarotScreen(name='tarot'))
        return sm

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def back_to_grid(self):
        self.root.current = 'card_grid'

    def normalize_filename(self, category, key):
        # Transforma "Paus", "Ás" -> "assets/paus_as.jpg"
        # Remove acentos e joga para minusculo
        cat_slug = category.lower()
        key_slug = key.lower()
        
        # Mapa simples de substituição de caracteres
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ã': 'a', 'õ': 'o', 'ê': 'e', 'ç': 'c'
        }
        for char, new_char in replacements.items():
            key_slug = key_slug.replace(char, new_char)
            
        return f"assets/{cat_slug}_{key_slug}.jpg"

    def show_grid(self, category):
        self.current_suit = category
        screen = self.root.get_screen('card_grid')
        screen.suit_title = f"Arcanos: {category}"
        grid = screen.ids.grid
        grid.clear_widgets()

        items = []
        if category == "Maior":
            items = [(k, v['nome'], v['desc']) for k, v in ARCANOS_MAIORES.items()]
            items.sort(key=lambda x: int(x[0]))
        else:
            data = ARCANOS_MENORES.get(category, {})
            # Ordem correta
            order = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Cavaleiro', 'Rainha', 'Rei']
            items = [(k, f"{k} de {category}", data[k]) for k in order if k in data]

        for key, name, rule in items:
            # Gera nome do arquivo normalizado (sem acento)
            img_path = self.normalize_filename(category, key)
            
            # Se não existir, usa logo.png
            final_img = img_path if os.path.exists(img_path) else "logo.png"

            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="160dp", # Tamanho da carta na grade
                radius=[12,],
                ripple_behavior=True
            )
            # Nome curto na grade
            display_name = name.replace(f" de {category}", "")
            if category == "Maior":
                display_name = name.split(" ", 1)[1] if " " in name else name

            card.add_widget(FitImage(
                source=final_img,
                radius=[12, 12, 0, 0],
                size_hint_y=0.75
            ))

            card.add_widget(MDLabel(
                text=display_name,
                bold=True, 
                theme_text_color="Custom",
                text_color=(1,1,1,1),
                halign="center",
                md_bg_color=(0, 0, 0, 0.6),
                size_hint_y=0.25
            ))
            
            card.bind(on_release=lambda x, n=name, r=rule, i=final_img: self.open_detail(n, r, i))
            grid.add_widget(card)

        self.root.current = 'card_grid'

    def open_detail(self, name, rule, image):
        screen = self.root.get_screen('card_detail')
        screen.card_name = name
        screen.card_rules = f"[size=18][b]Efeito no Jogo:[/b][/size]\n\n{rule}"
        screen.image_source = image
        self.root.current = 'card_detail'

if __name__ == '__main__':
    ArcanumApp().run()