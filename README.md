<div align="center">

<img src="assets/deva/deva-lockup-vertical.png" width="280" alt="DEVA">

✦ . * . ⟡ . * . ✦

<h1>ARCANUM VITAE</h1>

<em>O que está em cima é como o que está embaixo.</em>

<em>A Ascensão da Árvore da Vida: jogo de tabuleiro híbrido, com o Grimório do Iniciado como aplicativo de consulta.</em>

<code>⟡ CORE: KIVY · ⟡ ARCANOS: 78 · ⟡ ESFERAS: 10</code>

<img src="https://img.shields.io/badge/DEVA-ECOSYSTEM-0B111E?style=flat-square&labelColor=0B111E&color=DFB15B" alt="DEVA Ecosystem">
<img src="https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-0B111E?style=flat-square&labelColor=0F172A&color=E9A64A" alt="Status">
<img src="https://img.shields.io/badge/LICENSE-A%20DEFINIR-0B111E?style=flat-square&labelColor=0F172A&color=CBD5E1" alt="Licença">

✦ . * . ⟡ . * . ✦

</div>

## ✧ Visão Geral

Dez Esferas de Luz e vinte e dois Caminhos de Provação formam a Árvore da Vida. Os Iniciados a sobem entre zonas seguras e zonas de perigo, até a Coroa.

**Arcanum Vitae** é um jogo de tabuleiro competitivo para 2 a 4 jogadores, com partidas de 45 a 90 minutos. Cada jogador percorre as **10 Esferas (Sephiroth)** pelos **22 Caminhos (Arcanos Maiores)**, enfrentando **56 Arcanos Menores** como desafios. Vence quem chegar a **Keter** com a maior Sabedoria (PV), depois de dominar os quatro elementos: Paus, Copas, Espadas e Ouros.

O **Grimório do Iniciado** é o aplicativo de consulta: regras, custos das Esferas, efeitos de cada carta e uma seção de leitura de Tarot.

## ✧ Constelação

| Nó | Tipo | Estado |
|---|---|---|
| [`app/`](app) · Grimório do Iniciado | Aplicativo (Kivy) | `EM DESENVOLVIMENTO` |
| [`docs/GUIA_DO_JOGO.md`](docs/GUIA_DO_JOGO.md) · Guia do Jogo | Tomo para jogadores | `ATIVO` |
| [`docs/MANUAL_ARCANUM_VITAE.docx`](docs/MANUAL_ARCANUM_VITAE.docx) · Manual de Regras (também em [PDF](docs/MANUAL_ARCANUM_VITAE.pdf)) | Tomo de regras | `ATIVO` |
| [`assets/`](assets) · Tabuleiro, tokens, cartas e marca DEVA | Arquivo de imagens | `ATIVO` |

```
arcanum-vitae/
├── README.md
├── app/        Grimório do Iniciado: código, requirements.txt, buildozer.spec
├── assets/     logo, tabuleiro, tokens, cartas/ (Rider-Waite) e deva/ (marca)
└── docs/       GUIA_DO_JOGO.md · MANUAL_ARCANUM_VITAE.docx · MANUAL_ARCANUM_VITAE.pdf
```

## ✧ O Grimório do Iniciado

Consulta durante a partida, em português:

- **Regras:** 13 seções, do resumo de turno à contagem final.
- **Tabuleiro:** mapa celeste interativo da Árvore (toque em uma Esfera para ver custo e recompensa), Zonas e Níveis.
- **Sephiroth:** custo e recompensa das 10 Esferas.
- **Arcanos:** 22 Maiores (Regra Ambiental) e 56 Menores (opções A e B).
- **Recursos & Ações:** o que cada Token faz por 1 ou 2 unidades.
- **Tarot:** manual básico de leitura e significado das 78 cartas, em pé e invertida.
- **Créditos:** marca DEVA e atribuições.

**Visual:** cartografia celeste (céu estrelado, anel zodiacal, constelação da Árvore) com elementos de Tarot (molduras douradas e cartas que viram ao abrir) e a identidade DEVA. Há animações na capa (cintilar de estrelas, anel girando, Esferas pulsando), transições deslizantes entre telas e entrada escalonada dos conteúdos.

As cartas usam o baralho **Rider-Waite-Smith** original (Pamela Colman Smith, 1909, domínio público), obtido do Wikimedia Commons.

## ✧ Especificações Técnicas

| Componente | Tecnologia / Protocolo | Finalidade |
|---|---|---|
| **Core Engine** | Python 3.9 a 3.13 / Kivy 2.3 | Aplicação multiplataforma (desktop e mobile) |
| **Interface** | Kivy puro (`widgets.py`) | Componentes próprios: céu, mapa da Árvore, botões, moldura de carta, animações |
| **Dados do jogo** | Python (`dados_jogo.py`, `dados_tarot.py`) | Regras, Arcanos e significados, extraídos do manual |
| **Imagens das cartas** | Wikimedia Commons / `UrlRequest` | Download na primeira exibição, com cache local |
| **Empacotamento** | Buildozer / kivy-ios | Android (APK) e iOS |

## ✧ Execução do Projeto

```bash
# Clone do repositório
git clone https://github.com/jvitoraraujo/arcanum-vitae.git
cd arcanum-vitae/app

# Ambiente virtual (use Python 3.12; veja os requisitos abaixo)
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
# source .venv/bin/activate      # Linux / macOS

# Dependências
pip install -r requirements.txt

# Opcional: guarda as 78 cartas em assets/cartas para uso offline
python baixar_cartas.py

# Opcional: fontes da marca DEVA (Cinzel e JetBrains Mono)
python baixar_fontes.py

# Execução do Grimório
python main.py
```

Sem rodar `baixar_cartas.py`, o app baixa cada carta na primeira vez que ela é exibida e guarda em cache. Isso exige internet na primeira vez. Sem `baixar_fontes.py`, o app usa a fonte padrão do Kivy.

### Requisitos de versão

| Item | Mínimo | Máximo | Observação |
|---|---|---|---|
| **Python** | 3.9 | 3.13 | Testado em **3.12**. 3.13 deve funcionar (o Kivy 2.3.1 publica pacotes para ela), mas não foi testada. |
| **Kivy** | 2.3.1 | < 2.4 | O app usa `fit_mode` das imagens (Kivy 2.2 ou superior). |
| **certifi** | qualquer | | Necessário para baixar as cartas por HTTPS. |
| KivyMD, Pillow | | | **Não são usados.** Não instale o KivyMD. |

Sistemas: Windows 10 ou superior, Linux e macOS com OpenGL 2.0.

### Problemas de instalação

**`ERROR: No matching distribution found for kivy_deps.sdl2_dev~=0.7.0` (Windows, Python 3.14)**
O Kivy ainda não publica pacotes para Python 3.14, então o `pip` tenta compilar o Kivy e falha. Use Python 3.12 em um ambiente virtual:

```powershell
# opção 1: uv
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt

# opção 2: Python Launcher do Windows (com o Python 3.12 instalado)
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**`ImportError: cannot import name 'MDFillRoundFlatButton'`, `label.kv` não encontrado**
São erros de versões antigas deste app, que usavam KivyMD. A versão atual não precisa dele: desinstale (`pip uninstall kivymd`) e use apenas `requirements.txt`.

## ✧ Instalação em Dispositivos Móveis

O app é Kivy, então pode ser empacotado como app nativo. Os passos abaixo não foram testados em dispositivo; ajustes de versão do Buildozer podem ser necessários.

### Android (APK)

Use Linux, macOS, WSL2 ou um contêiner Docker com Buildozer.

```bash
pip install buildozer cython
cd app
./preparar_android.sh          # baixa as cartas e copia ../assets para app/assets
buildozer -v android debug     # gera bin/arcanumvitae-2.1-*-debug.apk
```

Instale o APK no celular:

1. Copie o arquivo `.apk` para o aparelho (cabo, nuvem ou `adb install bin/*.apk`).
2. Em Configurações, permita "Instalar apps de fontes desconhecidas" para o app que abrir o arquivo.
3. Toque no APK e instale.

Para publicar na Play Store, gere um pacote assinado (`buildozer android release`) conforme a documentação do Buildozer.

### Testar sem compilar (Android)

Instale o Pydroid 3, adicione `kivy` pelo gerenciador de pacotes, copie as pastas `app` e `assets` para o aparelho e abra `main.py`. O app procura `assets` ao lado dele ou na pasta acima.

### iOS

Requer um Mac com Xcode. Use o [kivy-ios](https://github.com/kivy/kivy-ios): crie o projeto com `toolchain build python3 kivy`, depois `toolchain create ArcanumVitae /caminho/para/app` e abra o projeto no Xcode. Copie `assets` para dentro da pasta do app antes.

## ✧ Regras em Resumo

1. Todos começam em Malkuth com 2 Recursos e 0 PV. Começa o jogador mais jovem.
2. No turno: **Fase Tática** (opcional), **Movimento** (1d6; Esferas só param com número exato) e **Encontro**.
3. Em um **Caminho**: vale a Regra Ambiental do Arcano Maior, saque um Arcano Menor (dois no Abismo), declare **Opção A** (avançar) ou **B** (atacar) e faça o **Teste**: 1d6, **4 ou mais vence**.
4. Em uma **Sephira**: zona segura, Mercado (3 por 1) e Consagração para ganhar PV.
5. Para entrar em **Keter**: número exato, ter consagrado Tiferet e pagar o **Tributo da Harmonia** (1 Recurso de cada naipe). O primeiro a entrar ganha +5 PV e encerra a partida.
6. Limite de 5 Tokens de cada tipo por jogador.

Detalhes completos no [Guia do Jogo](docs/GUIA_DO_JOGO.md) e no Manual de Regras.

## ✧ Registro

**v2.2**

- Visual redesenhado: cartografia celeste, Tarot e identidade DEVA, com animações e transições entre telas.
- Mapa da Árvore interativo na tela Tabuleiro.
- Interface sem KivyMD: instalação só com Kivy e certifi, em Python 3.9 a 3.13.

**v2.1**

- Regras fechadas: Teste de 1d6 (4+), numeração Rider-Waite, Mercado 3:1, bônus único de Keter, limites de Recursos e duração de efeitos.
- Aplicativo reescrito: regras completas, 22 Maiores, 56 Menores, Sephiroth, Recursos e seção de Tarot.
- Cartas oficiais Rider-Waite-Smith no lugar das imagens anteriores.
- Manual e Guia atualizados; marca DEVA aplicada.

## ✧ Créditos

- **Concept, game design e desenvolvimento:** Vitor Araújo.
- **Ilustrações das cartas:** Pamela Colman Smith, baralho Rider-Waite-Smith (1909), domínio público, via Wikimedia Commons.
- **Arte do tabuleiro, logo e tokens:** material original do projeto Arcanum Vitae.
- **Revisão de regras, expansão do app, guia e organização do repositório (v2.1):** com apoio do Claude, da Anthropic.

<div align="center">

✦ . * DEVA ARCHIVE * . ✦

<sub>Projetado e desenvolvido por Vitor Araújo sob o ecossistema DEVA.</sub>

<sub><a href="https://github.com/jvitoraraujo">GitHub</a> · <a href="https://www.linkedin.com/in/vitor-ara%C3%BAjo-55a98942b">LinkedIn</a></sub>

</div>
