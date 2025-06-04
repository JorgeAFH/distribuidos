import pygame
import threading
import time
import sys

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Resolución de Interbloqueo Vehicular")

# Fuentes y Colores
font = pygame.font.SysFont("segoeui", 28)
small_font = pygame.font.SysFont("segoeui", 20)
very_small_font = pygame.font.SysFont("segoeui", 14)

AZUL_AUTO = (52, 152, 219)
ROJO_AUTO = (192, 57, 43)
GRIS_PASILLO = (220, 221, 225)
FONDO = (245, 246, 250)
NEGRO = (44, 62, 80)
VERDE_BOTON = (39, 174, 96)
AZUL_BANNER = (41, 128, 185)
SOMBRA_COLOR = (0, 0, 0, 60)
RUEDA = (60, 60, 60)

# Locks simulando los recursos compartidos
entrada_norte = threading.Lock()
entrada_sur = threading.Lock()

# Variables compartidas
auto_azul_x = -100
auto_azul_y = 40
auto_rojo_y = HEIGHT - 140
auto_rojo_x = WIDTH // 2 - 100
salir = False
mostrar_boton_reinicio = False
simulacion_finalizada = False
mensaje_mostrado = False

# Locks para posiciones
pos_lock = threading.Lock()

# Estados
auto_azul_estado = "Esperando"
auto_rojo_estado = "Esperando"

# Dibujar sombra

def dibujar_sombra(rect, offset=(4, 4), color=SOMBRA_COLOR):
    sombra = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    sombra.fill(color)
    screen.blit(sombra, (rect.x + offset[0], rect.y + offset[1]))

def dibujar_fondo():
    screen.fill(FONDO)

    # Estilo de carretera
    ASFALTO = (50, 50, 50)
    LINEA_CENTRO = (255, 255, 255)
    LINEA_BORDE = (255, 204, 0)

    carretera_ancho = 100
    horizontal_alto = 100
    centro_x = WIDTH // 2 - carretera_ancho // 2

    carretera_vertical = pygame.Rect(centro_x, 0, carretera_ancho, HEIGHT)
    pygame.draw.rect(screen, ASFALTO, carretera_vertical)

    pygame.draw.line(screen, LINEA_BORDE, (centro_x, 0), (centro_x, HEIGHT), 4)
    pygame.draw.line(screen, LINEA_BORDE, (centro_x + carretera_ancho, 0), (centro_x + carretera_ancho, HEIGHT), 4)

    pygame.draw.rect(screen, ASFALTO, (0, 0, WIDTH, horizontal_alto))
    pygame.draw.rect(screen, ASFALTO, (0, HEIGHT - horizontal_alto, WIDTH, horizontal_alto))

    pygame.draw.line(screen, LINEA_BORDE, (0, horizontal_alto), (WIDTH, horizontal_alto), 4)
    pygame.draw.line(screen, LINEA_BORDE, (0, HEIGHT - horizontal_alto), (WIDTH, HEIGHT - horizontal_alto), 4)

    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, LINEA_CENTRO, (WIDTH // 2, y), (WIDTH // 2, y + 20), 4)

    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, LINEA_CENTRO, (x, horizontal_alto // 2), (x + 20, horizontal_alto // 2), 4)
        pygame.draw.line(screen, LINEA_CENTRO, (x, HEIGHT - horizontal_alto // 2), (x + 20, HEIGHT - horizontal_alto // 2), 4)

def dibujar_auto(x, y, color):
    pygame.draw.rect(screen, color, (x, y, 80, 40), border_radius=8)
    pygame.draw.circle(screen, RUEDA, (x + 15, y + 38), 5)
    pygame.draw.circle(screen, RUEDA, (x + 65, y + 38), 5)
    pygame.draw.circle(screen, (255, 255, 200), (x + 10, y + 10), 4)
    pygame.draw.circle(screen, (255, 255, 200), (x + 70, y + 10), 4)

def auto_azul_trayectoria():
    global auto_azul_x, auto_azul_y, auto_azul_estado
    auto_azul_estado = "Avanzando"
    with entrada_norte:
        while auto_azul_x < WIDTH // 2 - 40:
            with pos_lock:
                auto_azul_x += 1
            time.sleep(0.003)

        auto_azul_estado = "Descendiendo"
        while auto_azul_y < HEIGHT - 140:
            with pos_lock:
                auto_azul_y += 1
            time.sleep(0.003)

        auto_azul_estado = "Avanzando Este"
        while auto_azul_x < WIDTH:
            with pos_lock:
                auto_azul_x += 1
            time.sleep(0.003)

    auto_azul_estado = "Finalizado"

def auto_rojo_trayectoria():
    global auto_rojo_y, auto_rojo_x, auto_rojo_estado, simulacion_finalizada
    while auto_azul_estado != "Finalizado":
        time.sleep(0.1)

    auto_rojo_estado = "Cruzando"
    with entrada_sur:
        while auto_rojo_x < WIDTH // 2 - 40:
            with pos_lock:
                auto_rojo_x += 1
            time.sleep(0.003)

        auto_rojo_estado = "Ascendiendo"
        while auto_rojo_y > 40:
            with pos_lock:
                auto_rojo_y -= 1
            time.sleep(0.003)


        auto_rojo_estado = "Avanzando Este"
        while auto_rojo_x < WIDTH:
            with pos_lock:
                auto_rojo_x += 1
            time.sleep(0.003)

    auto_rojo_estado = "Finalizado"
    simulacion_finalizada = True

def dibujar_panel_estado():
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, 40))
    estado_azul = small_font.render(f"🚗 Azul: {auto_azul_estado}", True, NEGRO)
    estado_rojo = small_font.render(f"🚗 Rojo: {auto_rojo_estado}", True, NEGRO)
    screen.blit(estado_azul, (10, 10))
    screen.blit(estado_rojo, (WIDTH - 250, 10))

def dibujar_explicacion_resolucion():
    modal_width, modal_height = 720, 240
    modal_x = WIDTH // 2 - modal_width // 2
    modal_y = HEIGHT // 2 - modal_height // 2

    banner_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
    dibujar_sombra(banner_rect)

    # Fondo del banner
    pygame.draw.rect(screen, AZUL_BANNER, banner_rect, border_radius=20)
    pygame.draw.rect(screen, (180, 200, 255), banner_rect, 2, border_radius=20)

    # Tipografías
    titulo_font = pygame.font.SysFont("segoeui", 32, bold=True)
    subtitulo_font = pygame.font.SysFont("segoeui", 22)
    detalle_font = pygame.font.SysFont("segoeui", 18)

    # Título
    titulo = titulo_font.render("✅ Simulación Finalizada", True, (255, 255, 255))
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, modal_y + 25))

    # Subtítulo
    subtitulo = subtitulo_font.render("El interbloqueo fue evitado exitosamente.", True, (255, 255, 255))
    screen.blit(subtitulo, (WIDTH // 2 - subtitulo.get_width() // 2, modal_y + 75))

    # Detalles adicionales
    linea1 = detalle_font.render("🔵 El Auto Azul cruzó primero completando su trayectoria sin interrupciones.", True, (230, 230, 230))
    linea2 = detalle_font.render("🔴 El Auto Rojo esperó hasta que fue seguro avanzar, evitando el bloqueo.", True, (230, 230, 230))

    screen.blit(linea1, (WIDTH // 2 - linea1.get_width() // 2, modal_y + 120))
    screen.blit(linea2, (WIDTH // 2 - linea2.get_width() // 2, modal_y + 150))

def dibujar_boton_reinicio():
    boton_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 80, 120, 40)
    dibujar_sombra(boton_rect)
    pygame.draw.rect(screen, VERDE_BOTON, boton_rect, border_radius=10)
    texto = small_font.render("\u21bb Reiniciar", True, (255, 255, 255))
    screen.blit(texto, (boton_rect.centerx - texto.get_width() // 2, boton_rect.centery - texto.get_height() // 2))
    return boton_rect

def dibujar_escena():
    dibujar_fondo()
    with pos_lock:
        dibujar_auto(auto_azul_x, auto_azul_y, AZUL_AUTO)
        dibujar_auto(auto_rojo_x, auto_rojo_y, ROJO_AUTO)
    dibujar_panel_estado()

    boton = None
    if simulacion_finalizada:
        dibujar_explicacion_resolucion()
        boton = dibujar_boton_reinicio()

    pygame.display.flip()
    return boton

def reiniciar_simulacion():
    global auto_azul_x, auto_azul_y, auto_rojo_y, auto_rojo_x
    global auto_azul_estado, auto_rojo_estado, mostrar_boton_reinicio, simulacion_finalizada, mensaje_mostrado
    auto_azul_x = -100
    auto_azul_y = 40
    auto_rojo_y = HEIGHT - 140
    auto_rojo_x = WIDTH // 2 - 100
    auto_azul_estado = "Esperando"
    auto_rojo_estado = "Esperando"
    mostrar_boton_reinicio = False
    simulacion_finalizada = False
    mensaje_mostrado = False

clock = pygame.time.Clock()
t1 = None
t2 = None

reiniciar_simulacion()
t1 = threading.Thread(target=auto_azul_trayectoria)
t2 = threading.Thread(target=auto_rojo_trayectoria)
t1.start()
t2.start()

while True:
    boton_reinicio = dibujar_escena()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and boton_reinicio and boton_reinicio.collidepoint(event.pos):
            reiniciar_simulacion()
            t1 = threading.Thread(target=auto_azul_trayectoria)
            t2 = threading.Thread(target=auto_rojo_trayectoria)
            t1.start()
            t2.start()


    clock.tick(60)
