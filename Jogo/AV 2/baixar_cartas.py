import os
import requests

# Cria a pasta 'assets' se não existir
if not os.path.exists("assets"):
    os.makedirs("assets")

print("--- Iniciando Download do Tarot Rider-Waite ---")

# URL base de um repositório público com as imagens Rider-Waite (RWS)
BASE_URL = "https://raw.githubusercontent.com/tpphub/tarot-images/master/Rider-Waite"

# Mapeamento para traduzir nomes dos arquivos (Inglês -> Padrão do App em PT-BR)
# Estrutura do repo original: ar00.jpg (maiores), cu01.jpg (copas), etc.

suits_map = {
    "wands": "paus",
    "cups": "copas",
    "swords": "espadas",
    "pentacles": "ouros"
}

ranks_map = {
    "01": "as", "02": "2", "03": "3", "04": "4", "05": "5",
    "06": "6", "07": "7", "08": "8", "09": "9", "10": "10",
    "page": "valete", "knight": "cavaleiro", "queen": "rainha", "king": "rei"
}

# 1. Baixar Arcanos Maiores (00 a 21)
# No repo: ar00.jpg, ar01.jpg ...
for i in range(22):
    num_str = f"{i:02d}" # 00, 01, ...
    url = f"{BASE_URL}/ar{num_str}.jpg"
    filename = f"assets/maior_{i}.jpg"
    
    print(f"Baixando: {filename}...")
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)

# 2. Baixar Arcanos Menores
# No repo: cu01.jpg (Copas Ás), swking.jpg (Espadas Rei), etc.
repo_prefixes = {
    "wands": "wa",
    "cups": "cu",
    "swords": "sw",
    "pentacles": "pe"
}

for eng_suit, prefix in repo_prefixes.items():
    pt_suit = suits_map[eng_suit]
    
    for code, pt_rank in ranks_map.items():
        # URL source construction
        # O repo usa 'wa01.jpg' para números e 'waking.jpg' para corte
        # Precisamos ajustar o 'code' para bater com o repo source
        
        repo_rank_code = code # padrao '01', '02'
        if pt_rank in ['valete', 'cavaleiro', 'rainha', 'rei']:
            # No repo original as cartas da corte são: page, knight, queen, king
            # Mas o code no meu dicionario ranks_map chaves 'page', 'knight' ja estão corretos
            repo_rank_code = code 

        url = f"{BASE_URL}/{prefix}{repo_rank_code}.jpg"
        
        # Nome final no app: paus_as.jpg, copas_rei.jpg
        filename = f"assets/{pt_suit}_{pt_rank}.jpg"
        
        print(f"Baixando: {filename}...")
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
        else:
            print(f"ERRO ao baixar {url}")

print("\n--- Concluído! Imagens salvas na pasta 'assets' ---")