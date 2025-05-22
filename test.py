import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Cartel de prueba")
font = pygame.font.Font(None, 48)

# Crear texto
texto = font.render("¡Hola Mundo!", True, (255, 255, 255))  # Blanco
pos_texto = texto.get_rect(center=(320, 240))  # Centrado

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fondo negro
    screen.blit(texto, pos_texto)
    pygame.display.flip()

pygame.quit()
sys.exit()