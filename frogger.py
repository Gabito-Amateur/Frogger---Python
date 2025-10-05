import pygame
from modules import escenario_mapa_juego as escenario
from modules.movimiento_rana import Rana
from modules.obstaculos_carrera import Carretera
from modules.obstaculos_rio import Rio
from modules.vidas_puntaje import HUD
from modules.flujo_juego import Pantallas

pygame.init()

# ----------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Frogger - Juego Completo")

clock = pygame.time.Clock()
FPS = 60

# ----------------------------
# FUNCIÓN PARA INICIAR O REINICIAR PARTIDA
# ----------------------------
def iniciar_partida():
    rana = Rana(ANCHO, ALTO)
    hud = HUD(vidas_iniciales=3)
    zonas = escenario.calcular_secciones(ANCHO, ALTO)

    carretera_rect = zonas["carretera"]
    filas_carretera = [
        fila for fila in range(carretera_rect.top // rana.tam_celda, carretera_rect.bottom // rana.tam_celda)
    ]
    carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

    rio_rect = zonas["rio"]
    filas_rio = [
        fila for fila in range(rio_rect.top // rana.tam_celda, rio_rect.bottom // rana.tam_celda)
    ]
    rio = Rio(ANCHO, ALTO, rana.tam_celda, filas_rio)

    meta_rect = zonas["meta"]

    return rana, hud, carretera, rio, meta_rect

# ----------------------------
# PANTALLA DE INICIO
# ----------------------------
pantallas = Pantallas(ANCHO, ALTO)
pantallas.pantalla_inicio(ventana)

# ----------------------------
# BUCLE PRINCIPAL DEL JUEGO
# ----------------------------
ejecutando = True
while ejecutando:
    rana, hud, carretera, rio, meta_rect = iniciar_partida()
    game_over = False

    while not game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
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
                rana.ancho_ventana, rana.alto_ventana = ANCHO, ALTO

                # Recalcular zonas y obstáculos
                zonas = escenario.calcular_secciones(ANCHO, ALTO)
                carretera_rect = zonas["carretera"]
                filas_carretera = [
                    fila for fila in range(carretera_rect.top // rana.tam_celda,
                                            carretera_rect.bottom // rana.tam_celda)
                ]
                carretera = Carretera(ANCHO, ALTO, rana.tam_celda, filas_carretera)

                rio_rect = zonas["rio"]
                filas_rio = [
                    fila for fila in range(rio_rect.top // rana.tam_celda,
                                            rio_rect.bottom // rana.tam_celda)
                ]
                rio = Rio(ANCHO, ALTO, rana.tam_celda, filas_rio)
                meta_rect = zonas["meta"]

        # ----------------------------
        # LÓGICA DE JUEGO
        # ----------------------------
        carretera.mover()
        rio.mover()

        rana_rect = pygame.Rect(rana.x, rana.y, rana.tam_celda, rana.tam_celda)

        # Colisión con coches
        if carretera.verificar_colision(rana_rect):
            print("💥 ¡Colisión con coche!")
            rana.reset_posicion()
            if hud.restar_vida():
                game_over = True
                break

        # Caída al agua
        y_antes = rana.y
        rio.actualizar_rana(rana)
        if rana.y != y_antes and rana.y == (rana.alto_ventana // rana.tam_celda - 1) * rana.tam_celda:
            if hud.restar_vida():
                game_over = True
                break

        # Llegó a la meta
        if rana_rect.colliderect(meta_rect):
            hud.sumar_puntos(100)
            rana.reset_posicion()

        # ----------------------------
        # DIBUJAR TODO
        # ----------------------------
        zonas = escenario.dibujar_mapa(ventana, ANCHO, ALTO)
        rio.dibujar(ventana)
        carretera.dibujar(ventana)
        rana.dibujar(ventana)
        hud.dibujar(ventana, ANCHO)

        pygame.display.flip()
        clock.tick(FPS)

    # ----------------------------
    # GAME OVER - FLUJO DE REINICIO
    # ----------------------------
    accion = pantallas.pantalla_game_over(ventana, hud.puntaje)
    if accion == "reiniciar":
        continue  # vuelve a iniciar_partida()
    else:
        ejecutando = False

pygame.quit()
