import pygame
import threading
import time
import sys
import random

pygame.init()
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Interbloqueo Vehicular")

# Fuentes
font = pygame.font.SysFont("segoeui", 24)
small_font = pygame.font.SysFont("segoeui", 18)
very_small_font = pygame.font.SysFont("segoeui", 14)

# Colores
AZUL_AUTO = (41, 128, 185)
ROJO_AUTO = (192, 57, 43)
GRIS_CARRETERA = (60, 60, 60)
LINEAS_CENTRALES = (255, 255, 0)
LINEAS_BORDES = (240, 240, 240)
VERDE_CESPED = (39, 174, 96)
NEGRO = (0, 0, 0)
BANNER_BLOQUEO = (231, 76, 60)
VERDE_BOTON = (46, 204, 113)
SOMBRA_AUTO = (0, 0, 0, 50)
BLANCO = (255, 255, 255)

# Recursos compartidos
entrada_norte = threading.Lock()
entrada_sur = threading.Lock()
pos_lock = threading.Lock()

# Variables de estado
auto_norte_y = 50
auto_sur_y = HEIGHT - 100
interbloqueo_detectado = False
salir = False
mostrar_boton_reinicio = False
mostrar_mensaje_interbloqueo = False
auto_norte_estado = "Esperando"
auto_sur_estado = "Esperando"
bloqueo_timestamp = None

def dibujar_fondo():
    screen.fill(VERDE_CESPED)
    carretera_ancho = 140
    carretera_x = WIDTH // 2 - carretera_ancho // 2
    pygame.draw.rect(screen, GRIS_CARRETERA, (carretera_x, 0, carretera_ancho, HEIGHT))
    pygame.draw.line(screen, LINEAS_BORDES, (carretera_x, 0), (carretera_x, HEIGHT), 6)
    pygame.draw.line(screen, LINEAS_BORDES, (carretera_x + carretera_ancho, 0), (carretera_x + carretera_ancho, HEIGHT), 6)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, LINEAS_CENTRALES, (WIDTH // 2, y), (WIDTH // 2, y + 20), 4)

def dibujar_auto(x, y, color):
    sombra_surface = pygame.Surface((80, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra_surface, SOMBRA_AUTO, (0, 20, 80, 15))
    screen.blit(sombra_surface, (x, y + 10))
    pygame.draw.rect(screen, color, (x, y, 80, 40), border_radius=10)
    pygame.draw.circle(screen, (30, 30, 30), (x + 20, y + 38), 6)
    pygame.draw.circle(screen, (30, 30, 30), (x + 60, y + 38), 6)
    pygame.draw.circle(screen, (250, 250, 180), (x + 10, y + 10), 3)
    pygame.draw.circle(screen, (250, 250, 180), (x + 70, y + 10), 3)

def dibujar_bocadillo(texto, x, y, lado):
    max_width = 200
    padding = 10
    text_surface = very_small_font.render(texto, True, NEGRO)
    w, h = text_surface.get_size()
    ancho = min(max_width, w + 2 * padding)
    alto = h + 2 * padding
    bocadillo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    bocadillo.fill((255, 255, 255, 230))
    pygame.draw.rect(bocadillo, NEGRO, (0, 0, ancho, alto), 1, border_radius=8)
    bocadillo.blit(text_surface, (padding, padding))
    screen.blit(bocadillo, (x if lado == "izq" else x - ancho + 80, y - alto - 10))

def dibujar_panel_estado():
    pygame.draw.rect(screen, (245, 245, 245), (0, 0, WIDTH, 40))
    estado_norte = small_font.render(f"\U0001F697 Norte: {auto_norte_estado}", True, NEGRO)
    estado_sur = small_font.render(f"\U0001F697 Sur: {auto_sur_estado}", True, NEGRO)
    screen.blit(estado_norte, (20, 10))
    screen.blit(estado_sur, (WIDTH - 280, 10))

def auto_desde_norte():
    global auto_norte_y, interbloqueo_detectado, salir, auto_norte_estado, mostrar_boton_reinicio, bloqueo_timestamp
    auto_norte_estado = "Entrando"
    with entrada_norte:
        while auto_norte_y < HEIGHT // 2 - 50:
            with pos_lock:
                auto_norte_y += 1
            time.sleep(0.01)

        auto_norte_estado = "Solicita salida"
        if entrada_sur.acquire(timeout=3):
            try:
                auto_norte_estado = "Cruzando"
                while auto_norte_y < HEIGHT // 2 + 50:
                    with pos_lock:
                        auto_norte_y += 1
                    time.sleep(0.01)
                auto_norte_estado = "Finalizado"
            finally:
                entrada_sur.release()
        else:
            auto_norte_estado = "Bloqueado"
            interbloqueo_detectado = True
            bloqueo_timestamp = time.time()
            salir = True
            mostrar_boton_reinicio = True

def auto_desde_sur():
    global auto_sur_y, interbloqueo_detectado, salir, auto_sur_estado, mostrar_boton_reinicio, bloqueo_timestamp
    auto_sur_estado = "Entrando"
    with entrada_sur:
        while auto_sur_y > HEIGHT // 2 + 50:
            with pos_lock:
                auto_sur_y -= 1
            time.sleep(0.01)

        auto_sur_estado = "Solicita salida"
        if entrada_norte.acquire(timeout=3):
            try:
                auto_sur_estado = "Cruzando"
                while auto_sur_y > HEIGHT // 2 - 50:
                    with pos_lock:
                        auto_sur_y -= 1
                    time.sleep(0.01)
                auto_sur_estado = "Finalizado"
            finally:
                entrada_norte.release()
        else:
            auto_sur_estado = "Bloqueado"
            interbloqueo_detectado = True
            bloqueo_timestamp = time.time()
            salir = True
            mostrar_boton_reinicio = True

def dibujar_animacion_bloqueo():
    for _ in range(8):
        radio = random.randint(5, 10)
        pygame.draw.circle(screen, (180, 180, 180), (
            WIDTH // 2 + random.randint(-15, 15),
            HEIGHT // 2 + random.randint(-15, 15)
        ), radio)

def dibujar_boton_reinicio():
    rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 150, 120, 45)

    pygame.draw.rect(screen, VERDE_BOTON, rect, border_radius=12)
    texto = small_font.render("Reiniciar", True, (255, 255, 255))
    screen.blit(texto, (rect.centerx - texto.get_width() // 2, rect.centery - texto.get_height() // 2))
    return rect

def dibujar_interbloqueo():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    modal_width, modal_height = 760, 320
    modal_x = WIDTH // 2 - modal_width // 2
    modal_y = HEIGHT // 2 - modal_height // 2

    pygame.draw.rect(screen, (250, 250, 250), (modal_x, modal_y, modal_width, modal_height), border_radius=24)
    pygame.draw.rect(screen, (180, 180, 180), (modal_x, modal_y, modal_width, modal_height), 2, border_radius=24)

    titulo_font = pygame.font.SysFont("Arial", 36, bold=True)
    texto_font = pygame.font.SysFont("Arial", 22)
    dialogo_font = pygame.font.SysFont("Arial", 20, italic=True)
    nota_font = pygame.font.SysFont("Arial", 18)

    titulo = titulo_font.render("⚠️ ¡Interbloqueo Detectado!", True, (200, 40, 40))
    screen.blit(titulo, (modal_x + 30, modal_y + 25))

    texto1 = texto_font.render("Ambos autos poseen un recurso (su carril) y esperan al otro para continuar.", True, (40, 40, 40))
    texto2 = texto_font.render("Ninguno puede avanzar porque ambos esperan indefinidamente: esto es un interbloqueo.", True, (40, 40, 40))
    screen.blit(texto1, (modal_x + 30, modal_y + 85))
    screen.blit(texto2, (modal_x + 30, modal_y + 115))

    comentario_azul = dialogo_font.render("Auto Azul (Izquierda): \"¡Yo llegué primero, no me voy a echar para atrás!\"", True, (60, 60, 60))
    comentario_rojo = dialogo_font.render("Auto Rojo (Derecha): \"¡Si tú no te mueves, yo tampoco lo haré!\"", True, (60, 60, 60))
    screen.blit(comentario_azul, (modal_x + 30, modal_y + 165))
    screen.blit(comentario_rojo, (modal_x + 30, modal_y + 195))

    nota = nota_font.render("💡 Clásico ejemplo de deadlock: espera circular + exclusión mutua + no-preempción + espera", True, (90, 90, 90))
    screen.blit(nota, (modal_x + 30, modal_y + 250))
    dibujar_animacion_bloqueo()

def dibujar_escena():
    global mostrar_mensaje_interbloqueo
    dibujar_fondo()
    dx = random.randint(-2, 2) if interbloqueo_detectado else 0
    with pos_lock:
        dibujar_auto(WIDTH // 2 - 40 + dx, auto_norte_y, AZUL_AUTO)
        dibujar_auto(WIDTH // 2 - 40 - dx, auto_sur_y, ROJO_AUTO)
    dibujar_panel_estado()

    if interbloqueo_detectado:
        dibujar_bocadillo("¡Yo pasé primero!", WIDTH // 2 - 40, auto_norte_y, "izq")
        dibujar_bocadillo("¡Muévete tú!", WIDTH // 2 - 40, auto_sur_y, "der")

        if time.time() - bloqueo_timestamp >= 5:
            mostrar_mensaje_interbloqueo = True

    boton = None
    if mostrar_mensaje_interbloqueo:
        dibujar_interbloqueo()
        if mostrar_boton_reinicio:
            boton = dibujar_boton_reinicio()
    pygame.display.flip()
    return boton

def reiniciar_simulacion():
    global auto_norte_y, auto_sur_y, interbloqueo_detectado, salir
    global auto_norte_estado, auto_sur_estado, mostrar_boton_reinicio, mostrar_mensaje_interbloqueo, bloqueo_timestamp
    auto_norte_y = 50
    auto_sur_y = HEIGHT - 100
    interbloqueo_detectado = False
    salir = False
    auto_norte_estado = "Esperando"
    auto_sur_estado = "Esperando"
    mostrar_boton_reinicio = False
    mostrar_mensaje_interbloqueo = False
    bloqueo_timestamp = None

def iniciar_simulacion():
    t1 = threading.Thread(target=auto_desde_norte)
    t2 = threading.Thread(target=auto_desde_sur)
    t1.start()
    t2.start()

# Main
clock = pygame.time.Clock()
reiniciar_simulacion()
iniciar_simulacion()

while True:
    boton_reinicio = dibujar_escena()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if interbloqueo_detectado and event.type == pygame.MOUSEBUTTONDOWN:
            if boton_reinicio and boton_reinicio.collidepoint(event.pos):
                reiniciar_simulacion()
                iniciar_simulacion()

    clock.tick(60)
