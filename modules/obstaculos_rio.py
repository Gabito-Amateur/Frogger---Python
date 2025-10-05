import pygame
import random

# Colores de los troncos (tonos madera)
MADERA_CLARA = (181, 101, 29)
MADERA_OSCURA = (140, 70, 20)
COLORES_TRONCOS = [MADERA_CLARA, MADERA_OSCURA]

class Tronco:
    def __init__(self, x, y, ancho, alto, velocidad, direccion="derecha"):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = velocidad
        self.direccion = direccion
        self.color = random.choice(COLORES_TRONCOS)

    def mover(self, ancho_ventana):
        """Mueve el tronco horizontalmente y reaparece por el otro lado al salir."""
        if self.direccion == "derecha":
            self.rect.x += self.velocidad
            if self.rect.left > ancho_ventana:
                self.rect.right = 0
        else:
            self.rect.x -= self.velocidad
            if self.rect.right < 0:
                self.rect.left = ancho_ventana

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)


class Rio:
    def __init__(self, ancho_ventana, alto_ventana, tam_celda, filas_rio):
        """
        filas_rio: lista de filas del grid donde se colocarán los troncos.
        """
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.tam_celda = tam_celda
        self.carriles = filas_rio
        self.troncos = []

        self._crear_troncos()

    def _crear_troncos(self):
        """Genera troncos largos con distintas velocidades y direcciones."""
        self.troncos.clear()
        for fila in self.carriles:
            y = fila * self.tam_celda
            # Troncos más largos (4 celdas)
            ancho_tronco = self.tam_celda * 4
            alto_tronco = self.tam_celda

            direccion = random.choice(["izquierda", "derecha"])
            velocidad = random.randint(1, 3)  # más lentos que los coches

            # Crear 3 troncos espaciados horizontalmente
            for i in range(3):
                x = i * (self.ancho_ventana // 3)
                tronco = Tronco(x, y, ancho_tronco, alto_tronco, velocidad, direccion)
                self.troncos.append(tronco)

    def mover(self):
        for tronco in self.troncos:
            tronco.mover(self.ancho_ventana)

    def dibujar(self, ventana):
        for tronco in self.troncos:
            tronco.dibujar(ventana)

    def rana_sobre_tronco(self, rana_rect):
        """Devuelve el tronco sobre el que está la rana (si lo hay)."""
        for tronco in self.troncos:
            if rana_rect.colliderect(tronco.rect):
                return tronco
        return None

    def rana_en_agua(self, rana_rect):
        """Devuelve True si la rana está en el área del río pero no sobre un tronco."""
        tronco = self.rana_sobre_tronco(rana_rect)
        return tronco is None

    def actualizar_rana(self, rana):
        """
        Si la rana está sobre un tronco, se mueve con él.
        Si no, y está en el río, se resetea.
        """
        rana_rect = pygame.Rect(rana.x, rana.y, rana.tam_celda, rana.tam_celda)
        tronco = self.rana_sobre_tronco(rana_rect)

        if tronco:
            # La rana se mueve con el tronco
            if tronco.direccion == "derecha":
                rana.x += tronco.velocidad
            else:
                rana.x -= tronco.velocidad

            # Asegurarse de que no salga de la pantalla
            rana.x = max(0, min(rana.x, self.ancho_ventana - rana.tam_celda))

        else:
            # Verificar si la rana está realmente dentro del río (no solo tocando el borde)
            y_min = min(t * self.tam_celda for t in self.carriles)
            y_max = max(t * self.tam_celda for t in self.carriles) + self.tam_celda

            # Usamos el centro vertical de la rana para evitar falsos positivos en el borde
            rana_centro_y = rana.y + rana.tam_celda // 2

            if y_min < rana_centro_y < y_max:
                print("💦 ¡La rana cayó al agua! Reiniciando posición...")
                rana.reset_posicion()

