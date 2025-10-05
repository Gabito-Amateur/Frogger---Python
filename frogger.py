import pygame
from modules import escenario_mapa_juego as escenario
from modules.movimiento_rana import Rana
from modules.obstaculos_carrera import Carretera
from modules.obstaculos_rio import Rio
from modules.vidas_puntaje import HUD

pygame.init()

# Configuración inicial
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Frogger - Juego Completo")

# Rana
rana = Rana(ANCHO, ALTO)

# HUD
hud = HUD(vidas_iniciales=3)

# Escenario base
zonas = escenario.calcular_secciones(ANCHO, ALTO)
carretera_rect = zonas["carretera"]
rio_rect = zonas["rio"]
meta_rect = zonas["meta"]

# ===================== #
#  CARRILES DE CARRETERA
# ===================== #
filas_carretera = []
fila_inicio_c = carretera_rect.top // rana.tam_celda
fila_fin_c = carretera_rect.bottom // rana.tam_celda
for fila in range(fila_inicio_c, fila_fin_c):
    filas_carretera.append(fila)
carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

# ===================== #
#  CARRILES DE RÍO
# ===================== #
filas_rio = []
fila_inicio_r = rio_rect.top // rana.tam_celda
fila_fin_r = rio_rect.bottom // rana.tam_celda
for fila in range(fila_inicio_r, fila_fin_r):
    filas_rio.append(fila)
rio = Rio(ANCHO, ALTO, rana.tam_celda, filas_rio)

# ===================== #
#      CONTROL FPS
# ===================== #
clock = pygame.time.Clock()
FPS = 60
game_over = False

# ===================== #
#     BUCLE PRINCIPAL
# ===================== #
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif not game_over:
                if evento.key == pygame.K_UP:
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
            rio_rect = zonas["rio"]
            meta_rect = zonas["meta"]

            # Recalcular carriles
            filas_carretera = [fila for fila in range(carretera_rect.top // rana.tam_celda,
                                                     carretera_rect.bottom // rana.tam_celda)]
            filas_rio = [fila for fila in range(rio_rect.top // rana.tam_celda,
                                               rio_rect.bottom // rana.tam_celda)]
            carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)
            rio = Rio(ANCHO, ALTO, rana.tam_celda, filas_rio)
            rana.ancho_ventana, rana.alto_ventana = ANCHO, ALTO
            rana.reset_posicion()

    # Si el juego terminó, mostrar mensaje y congelar lógica
    if game_over:
        ventana.fill((255, 255, 255))
        texto_game_over = pygame.font.Font(None, 64).render("GAME OVER", True, (255, 0, 0))
        ventana.blit(texto_game_over, (ANCHO // 2 - 150, ALTO // 2 - 30))
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # ===================== #
    #   LÓGICA DE JUEGO
    # ===================== #
    carretera.mover()
    rio.mover()

    # Verificar colisión con coches
    rana_rect = pygame.Rect(rana.x, rana.y, rana.tam_celda, rana.tam_celda)
    if carretera.verificar_colision(rana_rect):
        print("💥 ¡Colisión con coche!")
        rana.reset_posicion()
        if hud.restar_vida():
            game_over = True
            continue

    # Actualizar rana respecto al río
    # Si la rana cae al agua, el método imprime mensaje y resetea
    y_antes = rana.y
    rio.actualizar_rana(rana)
    if rana.y != y_antes and rana.y == (rana.alto_ventana // rana.tam_celda - 1) * rana.tam_celda:
        # Esto ocurre cuando la rana fue reseteada por caer al agua
        if hud.restar_vida():
            game_over = True
            continue

    # Verificar si llegó a la meta
    if rana_rect.colliderect(meta_rect):
        hud.sumar_puntos(100)
        rana.reset_posicion()

    # ===================== #
    #   DIBUJAR TODO
    # ===================== #
    zonas = escenario.dibujar_mapa(ventana, ANCHO, ALTO)
    rio.dibujar(ventana)
    carretera.dibujar(ventana)
    rana.dibujar(ventana)
    hud.dibujar(ventana, ANCHO)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
