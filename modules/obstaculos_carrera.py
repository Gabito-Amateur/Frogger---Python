import pygame
import random

# Colores de coches
COLORES_COCHES = [
    (255, 0, 0),    # rojo
    (0, 0, 255),    # azul
    (255, 165, 0),  # naranja
    (128, 0, 128),  # morado
]

class Coche:
    def __init__(self, x, y, ancho, alto, velocidad, direccion="derecha"):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = velocidad
        self.direccion = direccion
        self.color = random.choice(COLORES_COCHES)

    def mover(self, ancho_ventana):
        """Mueve el coche horizontalmente y lo reinicia si sale de pantalla."""
        if self.direccion == "derecha":
            self.rect.x += self.velocidad
            if self.rect.left > ancho_ventana:  
                self.rect.right = 0
        else:  # izquierda
            self.rect.x -= self.velocidad
            if self.rect.right < 0:
                self.rect.left = ancho_ventana

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)


class Carretera:
    def __init__(self, ancho_ventana, alto_ventana, tam_celda, filas_carretera):
        """
        filas_carretera: lista con filas del grid donde estarán los carriles.
        """
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.tam_celda = tam_celda
        self.carriles = filas_carretera
        self.coches = []

        self._crear_coches()

    def _crear_coches(self):
        """Genera coches en los carriles con diferentes velocidades y direcciones."""
        for fila in self.carriles:
            y = fila * self.tam_celda
            # Tamaño estándar de coche (más ancho que la rana)
            ancho_coche = self.tam_celda * 2
            alto_coche = self.tam_celda

            # Dirección aleatoria por carril
            direccion = random.choice(["izquierda", "derecha"])
            velocidad = random.randint(2, 5)

            # Posiciones iniciales (espaciadas)
            for i in range(3):
                x = i * (self.ancho_ventana // 3)
                coche = Coche(x, y, ancho_coche, alto_coche, velocidad, direccion)
                self.coches.append(coche)

    def mover(self):
        for coche in self.coches:
            coche.mover(self.ancho_ventana)

    def dibujar(self, ventana):
        for coche in self.coches:
            coche.dibujar(ventana)

    def verificar_colision(self, rana_rect):
        """Revisa si la rana colisiona con algún coche."""
        for coche in self.coches:
            if rana_rect.colliderect(coche.rect):
                return True
        return False
