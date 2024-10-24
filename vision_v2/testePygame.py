import pygame
import cv2
import os

# Inicializa o Pygame
pygame.init()

# Definições da tela e cores
screen_width, screen_height = 1366, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Visight")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)

# Configurar feed de webcam com OpenCV
cap = cv2.VideoCapture(0)  # Webcam padrão

# Carregar imagem de fundo
background_image = pygame.image.load("/mnt/data/VISIGHT.png")

# Função para capturar imagem da webcam e mostrar no Pygame
def draw_webcam_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte de BGR (OpenCV) para RGB (Pygame)
        frame = cv2.resize(frame, (300, 300))  # Redimensiona para o quadrado da interface
        frame_surface = pygame.surfarray.make_surface(frame)
        screen.blit(frame_surface, (900, 200))  # Posicionar na área correta

# Função para desenhar o texto na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Variáveis para os campos de texto
input_boxes = {
    "Alimento": "",
    "Peso Bruto": "",
    "Peso Líquido": ""
}

active_input = None  # Campo de texto ativo

# Loop principal do Pygame
running = True
while running:
    screen.fill(WHITE)
    
    # Desenhar a imagem de fundo
    screen.blit(background_image, (0, 0))
    
    # Verificar eventos de input do teclado e mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_input] = input_boxes[active_input][:-1]
                else:
                    input_boxes[active_input] += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Verificar qual campo de texto foi clicado
            if 200 < x < 600 and 200 < y < 240:
                active_input = "Alimento"
            elif 200 < x < 600 and 300 < y < 340:
                active_input = "Peso Bruto"
            elif 200 < x < 600 and 400 < y < 440:
                active_input = "Peso Líquido"
            else:
                active_input = None

    # Desenhar a caixa da webcam
    draw_webcam_frame()

    # Desenhar os campos de texto e o texto já digitado
    draw_text("Alimento:", font, BLACK, screen, 200, 200)
    pygame.draw.rect(screen, WHITE, (400, 200, 200, 40))
    draw_text(input_boxes["Alimento"], font, BLACK, screen, 400, 200)

    draw_text("Peso Bruto:", font, BLACK, screen, 200, 300)
    pygame.draw.rect(screen, WHITE, (400, 300, 200, 40))
    draw_text(input_boxes["Peso Bruto"], font, BLACK, screen, 400, 300)

    draw_text("Peso Líquido:", font, BLACK, screen, 200, 400)
    pygame.draw.rect(screen, WHITE, (400, 400, 200, 40))
    draw_text(input_boxes["Peso Líquido"], font, BLACK, screen, 400, 400)

    # Atualizar a tela
    pygame.display.flip()
    
    # Controlar o frame rate
    clock.tick(30)

# Fechar a captura de vídeo e a janela do Pygame
cap.release()
pygame.quit()
