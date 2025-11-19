import pygame
import os

# Configurações
IMG_DIR = "images"
SOUND_DIR = "sounds"

# Cores
COLORS = {
    "hero": (0, 128, 255),   # Azul
    "enemy": (255, 0, 0),    # Vermelho
    "coin": (255, 215, 0),   # Dourado (AQUI ESTÁ A MOEDA)
    "floor": (50, 50, 50),   # Cinza escuro
    "bg": (30, 30, 30)       # Cinza quase preto
}

def create_image(name, color, size=(32, 32), shape="rect"):
    surface = pygame.Surface(size, pygame.SRCALPHA) # Transparência
    
    if shape == "circle":
        # Desenha circulo 
        pygame.draw.circle(surface, color, (16, 16), 14)
        pygame.draw.circle(surface, (255, 255, 255), (16, 16), 14, 2)
    else:
        # Desenha quadrado 
        surface.fill(color)
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, size[0], size[1]), 2)
    
    path = os.path.join(IMG_DIR, f"{name}.png")
    pygame.image.save(surface, path)
    print(f"Criado: {path}")

def create_dirs():
    if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
    if not os.path.exists(SOUND_DIR): os.makedirs(SOUND_DIR)

def main():
    pygame.init()
    create_dirs()

    # Personagens
    for state in ["idle", "run"]:
        for i in range(1, 3):
            c = COLORS["hero"]
            if i == 2: c = (100, 200, 255) 
            create_image(f"hero_{state}_{i}", c)
            
            c = COLORS["enemy"]
            if i == 2: c = (255, 100, 100)
            create_image(f"enemy_{state}_{i}", c)

    # CRIAR A IMAGEM DA MOEDA
    create_image("coin", COLORS["coin"], shape="circle")

    # Cenário
    create_image("menu_bg", COLORS["bg"], size=(800, 600))
    create_image("tile_floor", COLORS["floor"], size=(800, 600))
    
    print("\n Imagens atualizadas com a MOEDA!")

if __name__ == "__main__":
    main()
