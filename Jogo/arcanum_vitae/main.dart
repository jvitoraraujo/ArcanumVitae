import 'package:flutter/material.dart';

void main() {
  runApp(const MeuApp());
}

class MeuApp extends StatelessWidget {
  const MeuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // Remove a faixa "Debug"
      title: 'Arcanum Vitae',
      theme: ThemeData(primarySwatch: Colors.deepPurple),
      home: const TelaInicial(),
    );
  }
}

// --- TELA 1: MENU PRINCIPAL ---
class TelaInicial extends StatelessWidget {
  const TelaInicial({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Menu Principal')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Função 1 (Genérica)
            ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => const TelaGenerica(titulo: "Configurações")));
              },
              child: const Padding(
                padding: EdgeInsets.all(15.0),
                child: Text('1. Configurações (Exemplo)', style: TextStyle(fontSize: 18)),
              ),
            ),
            const SizedBox(height: 20),

            // Função 2 (Genérica)
            ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => const TelaGenerica(titulo: "Perfil")));
              },
              child: const Padding(
                padding: EdgeInsets.all(15.0),
                child: Text('2. Meu Perfil (Exemplo)', style: TextStyle(fontSize: 18)),
              ),
            ),
            const SizedBox(height: 20),

            // Função 3 (A GALERIA) - Botão com destaque
            ElevatedButton.icon(
              icon: const Icon(Icons.photo_library),
              label: const Padding(
                padding: EdgeInsets.all(15.0),
                child: Text('3. Abrir Galeria', style: TextStyle(fontSize: 18)),
              ),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.deepPurple, foregroundColor: Colors.white),
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => TelaGaleria()));
              },
            ),
          ],
        ),
      ),
    );
  }
}

// --- TELA DA GALERIA (Lista de Imagens) ---
class TelaGaleria extends StatelessWidget {
  TelaGaleria({super.key});

  // Lista de dados (simulando um banco de dados)
  // Cada item tem a URL da imagem e o Texto descritivo
  final List<Map<String, String>> listaDeImagens = [
    {
      "imagem": "https://picsum.photos/id/10/400/400", // Imagem Floresta
      "titulo": "Floresta",
      "descricao": "Uma paisagem serena de uma floresta densa e verde."
    },
    {
      "imagem": "https://picsum.photos/id/11/400/400", // Imagem Montanha
      "titulo": "Montanha",
      "descricao": "Vista incrível de montanhas rochosas durante o dia."
    },
    {
      "imagem": "https://picsum.photos/id/12/400/400", // Imagem Praia
      "titulo": "Praia",
      "descricao": "A areia suave e o mar calmo em um dia de verão."
    },
    {
      "imagem": "https://picsum.photos/id/13/400/400", // Imagem Cidade
      "titulo": "Cidade",
      "descricao": "O horizonte urbano e a vida agitada da metrópole."
    },
     {
      "imagem": "https://picsum.photos/id/14/400/400", // Imagem Cidade
      "titulo": "Mar",
      "descricao": "Ondas batendo nas pedras."
    },
     {
      "imagem": "https://picsum.photos/id/17/400/400", // Imagem Cidade
      "titulo": "Caminho",
      "descricao": "Uma trilha calma no meio do campo."
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Galeria de Fotos')),
      body: GridView.builder(
        padding: const EdgeInsets.all(10),
        // Define quantas colunas terá a grade (aqui pus 2)
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
        ),
        itemCount: listaDeImagens.length,
        itemBuilder: (context, index) {
          final item = listaDeImagens[index];
          
          return GestureDetector(
            // Ao clicar na imagem da grade...
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  // ...Abre a tela de detalhe, ENVIANDO os dados daquele item
                  builder: (context) => TelaDetalheImagem(
                    urlImagem: item['imagem']!,
                    titulo: item['titulo']!,
                    descricao: item['descricao']!,
                  ),
                ),
              );
            },
            // O visual de cada quadradinho na grade
            child: GridTile(
              footer: GridTileBar(
                backgroundColor: Colors.black54,
                title: Text(item['titulo']!, textAlign: TextAlign.center),
              ),
              child: Image.network(
                item['imagem']!,
                fit: BoxFit.cover, // Faz a imagem preencher o quadrado todo
                loadingBuilder: (context, child, loadingProgress) {
                  if (loadingProgress == null) return child;
                  return const Center(child: CircularProgressIndicator());
                },
              ),
            ),
          );
        },
      ),
    );
  }
}

// --- TELA DE DETALHE (Abre ao clicar na imagem) ---
class TelaDetalheImagem extends StatelessWidget {
  // Variáveis para receber os dados
  final String urlImagem;
  final String titulo;
  final String descricao;

  const TelaDetalheImagem({
    super.key,
    required this.urlImagem,
    required this.titulo,
    required this.descricao,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // Fundo preto para destaque
      appBar: AppBar(
        title: Text(titulo),
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // A Imagem Grande
          Expanded(
            child: Image.network(urlImagem, fit: BoxFit.contain),
          ),
          // O Texto de Descrição
          Container(
            padding: const EdgeInsets.all(20),
            color: Colors.white,
            width: double.infinity,
            child: Column(
              children: [
                Text(
                  titulo.toUpperCase(),
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 10),
                Text(
                  descricao,
                  style: const TextStyle(fontSize: 16),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}

// --- TELA GENÉRICA (Só para preencher os botões 1 e 2) ---
class TelaGenerica extends StatelessWidget {
  final String titulo;
  const TelaGenerica({super.key, required this.titulo});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(titulo)),
      body: Center(child: Text('Aqui seria a tela de $titulo')),
    );
  }
}