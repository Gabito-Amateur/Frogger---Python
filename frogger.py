import pygame
import sys
from modules import escenario_mapa_juego as escenario

def main(fullscreen=False):
    pygame.init()

    # Estado inicial
    if fullscreen:
        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        ancho, alto = ventana.get_size()
    else:
        ancho, alto = 600, 800
        ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

    pygame.display.set_caption("Frogger - Escenario Base")
    clock = pygame.time.Clock()

    # Bandera para saber si está en fullscreen
    en_fullscreen = fullscreen

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.VIDEORESIZE and not en_fullscreen:
                # Actualizar dimensiones en modo ventana redimensionable
                ancho, alto = event.size
                ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Alternar entre fullscreen y ventana
                    en_fullscreen = not en_fullscreen
                    if en_fullscreen:
                        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        ancho, alto = ventana.get_size()
                    else:
                        ancho, alto = 600, 800
                        ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

        # Dibujar mapa con dimensiones actuales
        zonas = escenario.dibujar_mapa(ventana, ancho, alto)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    # Puedes iniciar en fullscreen con fullscreen=True
    main(fullscreen=False)
