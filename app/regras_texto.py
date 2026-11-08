# -*- coding: utf-8 -*-
"""Regras de Arcanum Vitae por seção (alinhado a docs/MANUAL_ARCANUM_VITAE.docx).
Marcação Kivy: [b] [i] [color]."""

VERDE = "7FC4A0"
VERMELHO = "E8837C"
V = "[color=" + VERDE + "]"
R = "[color=" + VERMELHO + "]"
F = "[/color]"

SECOES = [
 ("Resumo do turno (consulta rápida)", [
  "[b]I. Fase Tática[/b] (opcional): gaste Tokens de Recurso em habilidades.",
  "[b]II. Fase de Movimento[/b]: role 1d6 e mova o peão. Esferas só param com número exato.",
  "[b]III. Fase de Encontro[/b]:",
  "• Parou em um [b]Caminho[/b]: vale a Regra Ambiental do Arcano Maior, saque Arcano(s) Menor(es), declare Opção A ou B e faça o Teste (1d6, 4+ vence).",
  "• Parou em uma [b]Sephira[/b]: zona segura, sem carta. Mercado e Consagração.",
  "[b]Fim:[/b] a partida termina quando alguém entra em Keter. Vence quem tiver mais PV.",
 ]),
 ("1. Premissa e objetivo", [
  "[b]Jogadores:[/b] 2 a 4. [b]Tempo:[/b] 45 a 90 min. [b]Estilo:[/b] competitivo e estratégico.",
  "Os jogadores são iniciados percorrendo os caminhos místicos da Cabala. O tabuleiro é a Árvore da Vida: [b]10 Esferas de Luz (Sephiroth)[/b] e [b]22 Caminhos de Provação (Arcanos Maiores)[/b].",
  "A meta não é só chegar ao topo, é chegar [i]iluminado[/i]: dominando os quatro elementos e acumulando a maior Sabedoria.",
  "O jogo é uma corrida. O fim é disparado imediatamente quando um jogador pousa [b]exatamente[/b] em Keter.",
  "[b]Vitória:[/b] ao final, vence quem tiver a maior soma de Pontos de Sabedoria (PV). Chegar primeiro dá bônus, mas não a vitória automática.",
 ]),
 ("2. Componentes", [
  "• 1 Tabuleiro: Árvore da Vida (10 Esferas, 22 Caminhos).",
  "• 1 Baralho de Desafios: 56 Arcanos Menores.",
  "• 4 Peões (Iniciados): O Desbravador (Paus/Fogo), O Intuitivo (Copas/Água), O Estrategista (Espadas/Ar), O Construtor (Ouros/Terra).",
  "• 1 Dado (d6) para movimento e para o Teste dos desafios. Um d4 (ou d6 ignorando 5 e 6) para o recuo.",
  "• Tokens de Elemento: Paus (Vontade): ação e movimento. Copas (Cura): defesa e emoção. Espadas (Insight): estratégia e lógica. Ouros (Riqueza): matéria e comércio.",
  "• [b]Limite de Recursos:[/b] cada jogador pode ter no máximo 5 Tokens de cada tipo (o excedente é perdido). O banco tem 100 Tokens de cada tipo.",
  "• Marcadores de Sabedoria (PV): Pontos de Vitória.",
 ]),
 ("3. Preparação", [
  "• [b]A Base:[/b] todos os peões começam em [b]Malkuth[/b] (O Reino).",
  "• [b]Mão inicial:[/b] cada jogador recebe 2 Recursos: 1 à sua escolha e 1 sorteado.",
  "• [b]Mente vazia:[/b] todos começam com 0 PV.",
  "• [b]Primeiro passo:[/b] o jogador mais jovem começa.",
 ]),
 ("4. Fase Tática", [
  "Opcional, no início do turno. O jogador pode gastar Tokens de Recurso para ativar habilidades (veja a tela [b]Recursos & Ações[/b]).",
  "Recursos também podem ser gastos como [b]Reação[/b] (defesa) durante o turno de outros.",
 ]),
 ("5. Movimento", [
  "O jogador rola 1d6 e move o peão.",
  "[b]Regra do Excesso:[/b] as Esferas [b]não[/b] interrompem o movimento. Se o dado for maior que a distância até a Esfera, o jogador passa direto, entra no próximo Caminho e para em uma casa de perigo.",
  "[b]Regra da Precisão:[/b] para entrar e parar em uma Esfera (zona segura) é preciso tirar o número [b]exato[/b].",
 ]),
 ("6. Encontro em um Caminho", [
  R + "O jogador está em perigo." + F,
  "• [b]Regra Ambiental:[/b] aplica-se o efeito passivo do Arcano Maior daquele caminho. Dura enquanto o peão estiver no trajeto.",
  "• [b]O Desafio:[/b] saque 1 Arcano Menor (2 nos Caminhos Críticos, ou se a regra do Arcano mandar).",
  "• [b]Quantidade:[/b] Caminhos Padrão (Níveis 1 a 3) = 1 carta. Caminhos Críticos (Nível 4, Abismo) = 2 cartas, e é preciso vencer ambas para ficar na casa.",
  "• [b]Resolução:[/b] declare a Opção A (Avanço) ou B (Ataque) e faça o Teste.",
  "• [b]O Teste:[/b] role 1d6. Com [b]4 ou mais[/b] você vence e aplica o efeito da opção escolhida; com [b]3 ou menos[/b], falha.",
  V + "Sucesso:" + F + " ganha 1 Recurso e 1 PV. Permanece na casa.",
  R + "Falha:" + F + " recua 1d4 casas e perde a vez. O recuo nunca passa da Esfera de origem do caminho.",
  R + "Falha Crítica (O Louco e A Torre):" + F + " volta para a Esfera de origem.",
 ]),
 ("7. Encontro em uma Sephira", [
  V + "O jogador está seguro. Nenhuma carta é sacada." + F,
  "• [b]Mercado Universal:[/b] troque 3 Recursos quaisquer por 1 Recurso à escolha (vale em qualquer Esfera, inclusive Malkuth).",
  "• [b]Consagração:[/b] se tiver os recursos exigidos pela Esfera, pague o custo e ganhe os PV indicados (ex.: pagar 2 Espadas em Hod rende 3 PV). Veja a tela [b]Sephiroth[/b].",
 ]),
 ("8. Zonas e Níveis", [
  "As [b]Esferas[/b] são organizadas em [b]Zonas[/b] e os [b]Caminhos[/b] em [b]Níveis[/b].",
  "Para ataques com cartas, ataques só atingem oponentes na [b]mesma Zona/Nível[/b] ou na [b]adjacente[/b] (imediatamente acima ou abaixo).",
  "• [b]Zona 1:[/b] Malkuth, Yesod.",
  "• [b]Zona 2:[/b] Hod, Netzach, Tiferet.",
  "• [b]Zona 3:[/b] Gevurah, Chesed.",
  "• [b]Zona 4 (O Abismo):[/b] Binah, Chokmah, Keter.",
  "• [b]Níveis dos Caminhos:[/b] de 1 a 4, nas mesmas faixas das Zonas. Cada Caminho pertence ao Nível da mais alta das duas Esferas que liga. O Nível 4 é o Abismo (Caminhos Críticos).",
  "Exceção: os ataques de [b]Reis e Rainhas[/b] têm alcance global.",
 ]),
 ("9. Os Desafios (Arcanos Menores)", [
  "[b]Quando:[/b] sempre que a fase de movimento termina em casa de Caminho (não Sephira).",
  "[b]O saque:[/b] 1 carta do topo do baralho de Arcanos Menores, ou 2 em Caminhos Perigosos (Abismo, ou regras como O Diabo).",
  "[b]A Escolha Tática (obrigatória):[/b] ao revelar a carta, leia as duas opções e [b]declare em voz alta[/b] a escolhida antes de rolar qualquer dado.",
  "• " + V + "Opção A (Avanço Pessoal):" + F + " beneficia você (recursos, movimento, bônus).",
  "• " + R + "Opção B (Ataque/Sabotagem):" + F + " prejudica um oponente (recuo, roubo, bloqueio). Só alcança a mesma Zona/Nível ou a adjacente.",
  "[b]Resolução:[/b] depois de escolher, pague o custo exigido pela carta (se houver) e faça o [b]Teste: role 1d6[/b]. 4 ou mais = Sucesso; 3 ou menos = Falha.",
  V + "Sucesso:" + F + " o peão fica onde está (seguro), ganha 1 Token de Recurso do naipe da carta e 1 PV.",
  R + "Falha:" + F + " sem recurso nem PV, o turno termina na hora e o jogador recua 1d4 casas (nunca além da Esfera de origem).",
  R + "Falha Crítica:" + F + " apenas em O Louco e A Torre: expulsão imediata para a Sephira de origem daquele turno.",
 ]),
 ("10. Realeza (Valete, Cavaleiro, Rainha, Rei)", [
  "As cartas da corte são [b]Chefes de Fase[/b].",
  "• [b]Recompensa dobrada:[/b] vencer concede 2 Tokens do naipe (em vez de 1).",
  "• [b]Imunidade a suborno:[/b] não podem ser puladas pagando recursos, a menos que você esteja no caminho d'O Mago. O desafio deve ser enfrentado.",
  "• [b]Alcance global:[/b] os ataques de Reis e Rainhas afetam oponentes em qualquer lugar do tabuleiro, ignorando as Zonas.",
 ]),
 ("11. Limites e durações", [
  "• [b]Limite de Recursos:[/b] máximo de 5 Tokens de cada tipo por jogador. O que passar disso é perdido.",
  "• [b]Banco:[/b] 100 Tokens de cada tipo.",
  "• [b]Duração dos efeitos:[/b] todo efeito sem duração indicada (bloqueios, banimentos, proibições) vale por [b]1 turno[/b]. Efeitos instantâneos (ganhar, perder, mover) acontecem uma única vez.",
  "• [b]Recuo:[/b] nunca passa da Esfera de origem do caminho.",
 ]),
 ("12. Keter e o Tributo da Harmonia", [
  "Para entrar na Coroa e encerrar o jogo o jogador deve:",
  "• Chegar com a contagem [b]exata[/b] do dado.",
  "• Ter [b]consagrado Tiferet[/b] durante a partida (pagando 1 Recurso de cada tipo).",
  "• Pagar o [b]Tributo da Harmonia:[/b] entregar 1 Recurso de [b]cada[/b] naipe (1 Paus, 1 Copas, 1 Espadas, 1 Ouros).",
  R + "Sem Tributo?" + F + " O movimento é cancelado e o jogador permanece na esfera anterior.",
  "Recompensa: fim de jogo e +5 PV de [b]Bônus de Pioneiro[/b]. É um único bônus, recebido só por quem entra primeiro.",
 ]),
 ("13. Contagem final", [
  "Quando os portões de Keter se abrem:",
  "• Quem encerrou o jogo ganha o [b]Bônus de Pioneiro (+5 PV)[/b] (o mesmo bônus de Keter; não se acumulam).",
  "• Todos somam os PV: cartas vencidas, Sephiroth consagradas e bônus.",
  "• O jogador com a maior Sabedoria é declarado [b]Mestre de Arcanum Vitae[/b].",
 ]),
]

ZONAS_TEXTO = [
 ("Zona 1", "Malkuth, Yesod"),
 ("Zona 2", "Hod, Netzach, Tiferet"),
 ("Zona 3", "Gevurah, Chesed"),
 ("Zona 4 (Abismo)", "Binah, Chokmah, Keter"),
]

NAIPES_INFO = {
 'paus':    dict(tema="Vontade, Ação, Velocidade, Combate Físico", recompensa="Token de Foco (Paus)", opb="Ataque ao Oponente", cor="ff9a4d"),
 'copas':   dict(tema="Emoção, Cura, Vínculos, Proteção", recompensa="Token de Cura (Copas)", opb="Ataque/Controle", cor="6ec3ff"),
 'espadas': dict(tema="Lógica, Verdade, Estratégia, Sabotagem", recompensa="Token de Insight (Espadas)", opb="Ataque/Sabotagem", cor="cfd6e0"),
 'ouros':   dict(tema="Material, Comércio, Ganância, Construção", recompensa="Token de Riqueza (Ouros)", opb="Ataque/Taxação", cor="f2c94c"),
}

NOTA_REALEZA = ("Carta da corte: Chefe de Fase. Vencer dá 2 Tokens do naipe, não pode ser pulada com suborno "
                "(exceto no caminho d'O Mago) e, para Reis e Rainhas, o ataque tem alcance global.")
