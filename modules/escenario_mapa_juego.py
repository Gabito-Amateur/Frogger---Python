import pygame

# Colores
VERDE = (0, 200, 0)       # Inicio
GRIS = (50, 50, 50)       # Carretera
AZUL = (0, 100, 200)      # Río
AMARILLO = (255, 215, 0)  # Meta
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

def calcular_secciones(ancho, alto):
    """Devuelve rectángulos de las secciones en base al tamaño actual de la ventana."""
    altura_seccion = alto // 8
    zonas = {
        "meta": pygame.Rect(0, 0, ancho, altura_seccion),
        "rio": pygame.Rect(0, altura_seccion, ancho, altura_seccion * 3),
        "carretera": pygame.Rect(0, altura_seccion * 4, ancho, altura_seccion * 3),
        "inicio": pygame.Rect(0, altura_seccion * 7, ancho, altura_seccion),
        "altura_seccion": altura_seccion
    }
    return zonas

def dibujar_mapa(ventana, ancho, alto):
    """Dibuja el escenario base adaptado al tamaño actual de la ventana."""
    ventana.fill(BLANCO)
    zonas = calcular_secciones(ancho, alto)

    # Dibujar secciones
    pygame.draw.rect(ventana, AMARILLO, zonas["meta"])
    pygame.draw.rect(ventana, AZUL, zonas["rio"])
    pygame.draw.rect(ventana, GRIS, zonas["carretera"])
    pygame.draw.rect(ventana, VERDE, zonas["inicio"])

    # Opcional: dibujar líneas divisorias
    for i in range(1, 8):
        pygame.draw.line(ventana, NEGRO, (0, zonas["altura_seccion"] * i), (ancho, zonas["altura_seccion"] * i), 2)

    return zonas  # Devolvemos coordenadas actualizadas (útil para colisiones o victoria)
