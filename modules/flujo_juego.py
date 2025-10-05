import pygame

COLOR_TEXTO = (0, 0, 0)
COLOR_TITULO = (0, 120, 0)
COLOR_FONDO = (230, 255, 230)
COLOR_GAMEOVER = (200, 0, 0)

class Pantallas:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_texto = pygame.font.Font(None, 36)

    def pantalla_inicio(self, ventana):
        """Muestra la pantalla de inicio hasta que el jugador presione Enter."""
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        esperando = False
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                elif evento.type == pygame.VIDEORESIZE:
                    self.ancho, self.alto = evento.w, evento.h
                    ventana = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)

            ventana.fill(COLOR_FONDO)

            titulo = self.fuente_titulo.render("FROGGER", True, COLOR_TITULO)
            texto1 = self.fuente_texto.render("Usa las flechas para mover la rana", True, COLOR_TEXTO)
            texto2 = self.fuente_texto.render("Evita los coches y cruza el río saltando sobre los troncos", True, COLOR_TEXTO)
            texto3 = self.fuente_texto.render("Presiona ENTER para comenzar", True, COLOR_TEXTO)

            ventana.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, self.alto // 3))
            ventana.blit(texto1, (self.ancho // 2 - texto1.get_width() // 2, self.alto // 2))
            ventana.blit(texto2, (self.ancho // 2 - texto2.get_width() // 2, self.alto // 2 + 40))
            ventana.blit(texto3, (self.ancho // 2 - texto3.get_width() // 2, int(self.alto * 0.75)))

            pygame.display.flip()

    def pantalla_game_over(self, ventana, puntaje_final):
        """Muestra la pantalla de Game Over y espera Enter o ESC."""
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        return "reiniciar"
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                elif evento.type == pygame.VIDEORESIZE:
                    self.ancho, self.alto = evento.w, evento.h
                    ventana = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)

            ventana.fill((255, 255, 255))
            titulo = self.fuente_titulo.render("GAME OVER", True, COLOR_GAMEOVER)
            texto_puntaje = self.fuente_texto.render(f"Tu puntaje final: {puntaje_final}", True, COLOR_TEXTO)
            texto_reinicio = self.fuente_texto.render("Presiona ENTER para reiniciar o ESC para salir", True, COLOR_TEXTO)

            ventana.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, self.alto // 3))
            ventana.blit(texto_puntaje, (self.ancho // 2 - texto_puntaje.get_width() // 2, self.alto // 2))
            ventana.blit(texto_reinicio, (self.ancho // 2 - texto_reinicio.get_width() // 2, int(self.alto * 0.7)))

            pygame.display.flip()
