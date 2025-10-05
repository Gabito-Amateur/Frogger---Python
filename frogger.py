import pygame
from modules import escenario_mapa_juego as escenario
from modules.movimiento_rana import Rana
from modules.obstaculos_carrera import Carretera
from modules.obstaculos_rio import Rio

pygame.init()

# Configuración inicial
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Frogger - Integración completa")

# Rana
rana = Rana(ANCHO, ALTO)

# Escenario base
zonas = escenario.calcular_secciones(ANCHO, ALTO)

# ===================== #
#   CARRILES CARRETERA  #
# ===================== #
carretera_rect = zonas["carretera"]
filas_carretera = []
fila_inicio = carretera_rect.top // rana.tam_celda
fila_fin = carretera_rect.bottom // rana.tam_celda
for fila in range(fila_inicio, fila_fin):
    filas_carretera.append(fila)
carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

# ===================== #
#       CARRILES RÍO     #
# ===================== #
rio_rect = zonas["rio"]
filas_rio = []
fila_inicio_rio = rio_rect.top // rana.tam_celda
fila_fin_rio = rio_rect.bottom // rana.tam_celda
for fila in range(fila_inicio_rio, fila_fin_rio):
    filas_rio.append(fila)
rio = Rio(ANCHO, ALTO, rana.tam_celda, filas_rio)

# ===================== #
#        CONTROL FPS     #
# ===================== #
clock = pygame.time.Clock()
FPS = 60

# ===================== #
#       BUCLE PRINCIPAL  #
# ===================== #
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
            # Recalcular todo al cambiar tamaño
            ANCHO, ALTO = evento.w, evento.h
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            zonas = escenario.calcular_secciones(ANCHO, ALTO)

            # Recalcular carretera
            carretera_rect = zonas["carretera"]
            filas_carretera = []
            fila_inicio = carretera_rect.top // rana.tam_celda
            fila_fin = carretera_rect.bottom // rana.tam_celda
            for fila in range(fila_inicio, fila_fin):
                filas_carretera.append(fila)
            carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

            # Recalcular río
            rio_rect = zonas["rio"]
            filas_rio = []
            fila_inicio_rio = rio_rect.top // rana.tam_celda
            fila_fin_rio = rio_rect.bottom // rana.tam_celda
            for fila in range(fila_inicio_rio, fila_fin_rio):
                filas_rio.append(fila)
            rio = Rio(ANCHO, ALTO, rana.tam_celda, filas_rio)

            rana.ancho_ventana, rana.alto_ventana = ANCHO, ALTO
            rana.reset_posicion()

    # ===================== #
    #    LÓGICA DE JUEGO    #
    # ===================== #
    carretera.mover()
    rio.mover()
    rio.actualizar_rana(rana)

    # ===================== #
    #    DIBUJAR ELEMENTOS  #
    # ===================== #
    zonas = escenario.dibujar_mapa(ventana, ANCHO, ALTO)
    rio.dibujar(ventana)
    carretera.dibujar(ventana)
    rana.dibujar(ventana)

    # Colisión con coches
    rana_rect = pygame.Rect(rana.x, rana.y, rana.tam_celda, rana.tam_celda)
    if carretera.verificar_colision(rana_rect):
        print("💥 ¡Colisión con coche! Reiniciando rana...")
        rana.reset_posicion()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
