# 🏰 Dungeon Escape (Python Tutor Test)

## 📝 Sobre o Projeto
Este projeto é um jogo de aventura 2D desenvolvido como parte do **Teste Técnico para Tutores de Python**.

O objetivo foi criar um jogo completo utilizando a biblioteca **PgZero**, seguindo rigorosamente os requisitos de engenharia de software solicitados, como Programação Orientada a Objetos (POO), animação de sprites e código limpo (PEP8).

## ✨ Funcionalidades e Requisitos Atendidos

O jogo foi auditado para cumprir 100% das regras do desafio:

- [x] **Biblioteca:** Apenas `pgzero`, `math`, `random` e `pygame.Rect` foram utilizados.
- [x] **Gênero:** Aventura Top-Down (Mecânica de fuga e coleta de moedas).
- [x] **Menu Principal:** Sistema funcional com botões "Iniciar", "Som On/Off" e "Sair".
- [x] **POO (Classes):** Implementação de herança com classes `Character`, `Hero` e `Enemy`.
- [x] **Animação de Sprites:** Personagens animados tanto parados (`idle`) quanto em movimento, utilizando *Delta Time* (`dt`) para garantir fluidez independente do FPS.
- [x] **IA de Inimigos:** Inimigos patrulham territórios específicos e respeitam limites de área (não apenas perseguição simples).
- [x] **Código Limpo:** Variáveis semânticas em inglês e conformidade com PEP8.

## 🚀 Como Rodar o Jogo Localmente

### Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Jhennifer-Pozzer/dungeon-escape-pgzero.gitInstale a dependência:
Bash

pip install pgzero

(Nota: Se estiver usando Linux, pode ser necessário instalar sudo apt install python3-pygame ou similar dependendo da distro).

Gere os Assets (Importante!): Para garantir que o jogo seja leve e autocontido, os assets gráficos (sprites) são gerados proceduralmente por um script. Execute este passo antes de jogar:
Bash

python3 setup_assets.py

Você verá uma confirmação de que as imagens e a moeda foram criadas na pasta images.

Execute o jogo:
Bash

    pgzrun game.py

🎮 Controles

    Setas (🡡 🡣 🡠 🡢): Movimentam o Herói.

    Mouse: Interage com os botões do Menu (Start, Som, Sair).

📂 Estrutura do Projeto

    game.py: Código fonte principal contendo a lógica do jogo, classes (Hero, Enemy, Coin) e o loop de eventos do PgZero.

    setup_assets.py: Script auxiliar que gera os sprites (imagens) e estrutura de pastas necessárias para execução imediata.

Desenvolvido por Jhennifer.

