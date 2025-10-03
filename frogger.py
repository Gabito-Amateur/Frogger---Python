import pygame
from modules import escenario_mapa_juego as escenario
from modules.movimiento_rana import Rana
from modules.obstaculos_carrera import Carretera

pygame.init()

# Configuración inicial
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Frogger - Test Integración")

# Rana
rana = Rana(ANCHO, ALTO)

# Carretera: vamos a ubicar coches en la zona de carretera que nos da el escenario
zonas = escenario.calcular_secciones(ANCHO, ALTO)
carretera_rect = zonas["carretera"]

# Carriles = filas dentro de la carretera, en base al grid de la rana
filas_carretera = []
fila_inicio = carretera_rect.top // rana.tam_celda
fila_fin = carretera_rect.bottom // rana.tam_celda
for fila in range(fila_inicio, fila_fin):
    filas_carretera.append(fila)

carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

# Clock para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.key == pygame.K_UP:
                rana.mover("arriba")
            elif evento.key == pygame.K_DOWN:
                rana.mover("abajo")
            elif evento.key == pygame.K_LEFT:
                rana.mover("izquierda")
            elif evento.key == pygame.K_RIGHT:
                rana.mover("derecha")

        elif evento.type == pygame.VIDEORESIZE:
            ANCHO, ALTO = evento.w, evento.h
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            zonas = escenario.calcular_secciones(ANCHO, ALTO)
            carretera_rect = zonas["carretera"]

            # Recalcular carriles al hacer resize
            filas_carretera = []
            fila_inicio = carretera_rect.top // rana.tam_celda
            fila_fin = carretera_rect.bottom // rana.tam_celda
            for fila in range(fila_inicio, fila_fin):
                filas_carretera.append(fila)

            rana.ancho_ventana, rana.alto_ventana = ANCHO, ALTO
            carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

    # Mover coches
    carretera.mover()

    # Dibujar escenario
    zonas = escenario.dibujar_mapa(ventana, ANCHO, ALTO)

    # Dibujar rana
    rana.dibujar(ventana)

    # Dibujar coches
    carretera.dibujar(ventana)

    # Verificar colisión rana–coche
    rana_rect = pygame.Rect(rana.x, rana.y, rana.tam_celda, rana.tam_celda)
    if carretera.verificar_colision(rana_rect):
        print("💥 ¡Colisión detectada! Reiniciando rana...")
        rana.reset_posicion()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
