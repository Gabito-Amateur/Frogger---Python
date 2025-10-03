import pygame

# Color y tamaño de la rana
VERDE_RANA = (0, 255, 0)

# Tamaño de la celda en píxeles
TAM_CELDA = 25  

class Rana:
    def __init__(self, ancho_ventana, alto_ventana):
        self.tam_celda = TAM_CELDA
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.reset_posicion()

    def reset_posicion(self):
        """Reinicia la rana a la posición inicial (parte inferior, centrada)."""
        columnas = self.ancho_ventana // self.tam_celda
        filas = self.alto_ventana // self.tam_celda
        self.x = (columnas // 2) * self.tam_celda
        self.y = (filas - 1) * self.tam_celda

    def mover(self, direccion):
        """Mueve la rana una celda en la dirección indicada, sin salirse de la ventana."""
        if direccion == "arriba":
            self.y = max(0, self.y - self.tam_celda)
        elif direccion == "abajo":
            self.y = min(self.alto_ventana - self.tam_celda, self.y + self.tam_celda)
        elif direccion == "izquierda":
            self.x = max(0, self.x - self.tam_celda)
        elif direccion == "derecha":
            self.x = min(self.ancho_ventana - self.tam_celda, self.x + self.tam_celda)

    def dibujar(self, ventana):
        """Dibuja la rana en pantalla (rectángulo verde más pequeño)."""
        rana_rect = pygame.Rect(self.x, self.y, self.tam_celda, self.tam_celda)
        pygame.draw.rect(ventana, VERDE_RANA, rana_rect)
