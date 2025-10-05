import pygame

COLOR_TEXTO = (0, 0, 0)  # Negro
FUENTE_TAM = 28

class HUD:
    def __init__(self, vidas_iniciales=3):
        self.vidas = vidas_iniciales
        self.puntaje = 0
        self.fuente = pygame.font.Font(None, FUENTE_TAM)

    def restar_vida(self):
        """Resta una vida y devuelve True si el jugador se quedó sin vidas."""
        self.vidas -= 1
        print(f"💔 Vida perdida. Vidas restantes: {self.vidas}")
        if self.vidas <= 0:
            print("💀 ¡Game Over!")
            return True
        return False

    def sumar_puntos(self, puntos):
        """Aumenta el puntaje."""
        self.puntaje += puntos
        print(f"🏆 +{puntos} puntos | Total: {self.puntaje}")

    def dibujar(self, ventana, ancho):
        """Dibuja el HUD de vidas y puntaje."""
        # Texto de vidas
        texto_vidas = self.fuente.render(f"Vidas: {self.vidas}", True, COLOR_TEXTO)
        texto_puntaje = self.fuente.render(f"Puntaje: {self.puntaje}", True, COLOR_TEXTO)

        # Posiciones (arriba izquierda y arriba derecha)
        ventana.blit(texto_vidas, (20, 10))
        ventana.blit(texto_puntaje, (ancho - 180, 10))
