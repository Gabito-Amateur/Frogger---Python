import pygame
import sys
from modules import escenario_mapa_juego as escenario
from modules.movimiento_rana import Rana

def main(fullscreen=False):
    pygame.init()

    # Ventana inicial
    if fullscreen:
        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        ancho, alto = ventana.get_size()
    else:
        ancho, alto = 600, 800
        ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

    pygame.display.set_caption("Frogger - Movimiento de la Rana")
    clock = pygame.time.Clock()

    # Crear rana
    rana = Rana(ancho, alto)

    en_fullscreen = fullscreen

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE and not en_fullscreen:
                ancho, alto = event.size
                ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
                rana.ancho_ventana, rana.alto_ventana = ancho, alto
                rana.reset_posicion()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Alternar fullscreen
                    en_fullscreen = not en_fullscreen
                    if en_fullscreen:
                        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        ancho, alto = ventana.get_size()
                    else:
                        ancho, alto = 600, 800
                        ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
                    rana.ancho_ventana, rana.alto_ventana = ancho, alto
                    rana.reset_posicion()

                # Movimiento con teclado
                elif event.key == pygame.K_UP:
                    rana.mover("arriba")
                elif event.key == pygame.K_DOWN:
                    rana.mover("abajo")
                elif event.key == pygame.K_LEFT:
                    rana.mover("izquierda")
                elif event.key == pygame.K_RIGHT:
                    rana.mover("derecha")
                elif event.key == pygame.K_r:
                    rana.reset_posicion()

        # Dibujar
        escenario.dibujar_mapa(ventana, ancho, alto)
        rana.dibujar(ventana)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main(fullscreen=False)
