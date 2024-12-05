import os
import pygame
import random
import csv
import json
from datetime import datetime

# Iniciar Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Preguntas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
GRIS = (169, 169, 169)

# Fuentes
fuente = pygame.font.SysFont("Arial", 30)
fuente_pequeña = pygame.font.SysFont("Arial", 24)
fuente_nombre = pygame.font.SysFont("Arial", 24)

# Variables de juego
vidas = 3
puntos = 0
respuestas_correctas = 0
categoria_seleccionada = None
comodin_duplicar_puntos_usado = False
comodin_pasado_usado = False

# Cargar preguntas desde el archivo CSV
def cargar_preguntas(categoria):
    preguntas = []
    with open(f"preguntas.csv", newline="") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            preguntas.append(fila)
    return preguntas

# Función para mostrar texto en pantalla
def mostrar_texto(texto, x, y, color, fuente):
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))

# Función para mostrar el menú
def mostrar_menu():
    pantalla.fill(BLANCO)
    mostrar_texto("Bienvenido al juego de preguntas!", 250, 100, NEGRO, fuente)
    
    # Botón "Jugar"
    pygame.draw.rect(pantalla, AZUL, (300, 300, 200, 50))  # Rectángulo de color para el botón
    mostrar_texto("Jugar", 350, 310, BLANCO, fuente)
    
    # Botón "TOP 10"
    pygame.draw.rect(pantalla, AZUL, (300, 400, 200, 50))  # Rectángulo de color para el botón
    mostrar_texto("TOP 10", 350, 410, BLANCO, fuente)

    pygame.display.flip()

# Función para mostrar las categorías
def mostrar_categorias():
    global categoria_seleccionada
    pantalla.fill(BLANCO)
    mostrar_texto("Elige una categoría:", 250, 100, NEGRO, fuente)

    categorias = ['Historia', 'Matematica', 'Entretenimiento', 'Deportes']
    for i, categoria in enumerate(categorias):
        pygame.draw.rect(pantalla, AZUL, (300, 200 + i * 60, 200, 50))  # Rectángulo de color para cada botón
        mostrar_texto(categoria, 350, 210 + i * 60, BLANCO, fuente)

    pygame.display.flip()

    # Esperar a que el jugador seleccione una categoría
    esperando_categoria = True
    while esperando_categoria:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, categoria in enumerate(categorias):
                    if 300 < pos[0] < 500 and 200 + i * 60 < pos[1] < 250 + i * 60:
                        categoria_seleccionada = categoria
                        esperando_categoria = False
                        break

# Función para mostrar la pregunta y respuestas
def mostrar_pregunta(pregunta):
    pantalla.fill(BLANCO)
    mostrar_texto(pregunta[1], 50, 100, NEGRO, fuente)
    
    for i in range(4):
        mostrar_texto(f"{i+1}. {pregunta[i+2]}", 50, 200 + i*50, NEGRO, fuente_pequeña)

    # Botón "Duplicar Puntos"
    if not comodin_duplicar_puntos_usado:
        pygame.draw.rect(pantalla, AZUL, (600, 200, 150, 50))  # Rectángulo para el botón
        mostrar_texto("Duplicar Puntos", 610, 210, BLANCO, fuente_pequeña)
    else:
        pygame.draw.rect(pantalla, GRIS, (600, 200, 150, 50))  # Botón desactivado (gris)
        mostrar_texto("Duplicar Puntos", 610, 210, BLANCO, fuente_pequeña)
    
    # Botón "Pasar Pregunta"
    if not comodin_pasado_usado:
        pygame.draw.rect(pantalla, AZUL, (600, 270, 150, 50))  # Rectángulo para el botón
        mostrar_texto("Pasar Pregunta", 610, 280, BLANCO, fuente_pequeña)
    else:
        pygame.draw.rect(pantalla, GRIS, (600, 270, 150, 50))  # Botón desactivado (gris)
        mostrar_texto("Pasar Pregunta", 610, 280, BLANCO, fuente_pequeña)

# Función para usar el comodín de Duplicar Puntos
def usar_comodin_duplicar_puntos():
    global comodin_duplicar_puntos_usado
    comodin_duplicar_puntos_usado = True

# Función para pasar a la siguiente pregunta sin afectar puntos ni vidas
def pasar_siguiente_pregunta():
    global comodin_pasado_usado
    comodin_pasado_usado = True

# Función para verificar la respuesta
def verificar_respuesta(respuesta_usuario, pregunta):
    global puntos, vidas, respuestas_correctas
    respuesta_correcta = int(pregunta[6]) - 1  # Convertir la respuesta correcta a índice (0-3)
    
    if respuesta_usuario == respuesta_correcta:
        # Si el comodín de duplicar puntos no ha sido usado, sumar 10 puntos
        if not comodin_duplicar_puntos_usado:
            puntos += 10
        else:
            puntos += 20  # Duplicar los puntos si se usó el comodín
        respuestas_correctas += 1
        if respuestas_correctas == 5:  # Si ha acertado 5 veces seguidas
            vidas += 1
            respuestas_correctas = 0
    else:
        puntos -= 5
        vidas -= 1
        respuestas_correctas = 0

# Función para pedir el nombre del jugador
def pedir_nombre():
    pantalla.fill(BLANCO)
    mostrar_texto("Ingresa tu nombre:", 250, 200, NEGRO, fuente_nombre)
    pygame.display.flip()

    nombre = ""
    esperando_nombre = True
    while esperando_nombre:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre != "":
                    esperando_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.key <= 127:  # Aceptar caracteres
                    nombre += evento.unicode
        pantalla.fill(BLANCO)
        mostrar_texto("Ingresa tu nombre:", 250, 200, NEGRO, fuente_nombre)
        mostrar_texto(nombre, 250, 250, NEGRO, fuente_nombre)
        pygame.display.flip()
    return nombre

# Función para mostrar el mensaje "Perdiste"
def mostrar_mensaje_perdido():
    pantalla.fill(BLANCO)
    mostrar_texto("¡PERDISTE!", 350, 250, (255, 0, 0), fuente)
    pygame.display.flip()
    pygame.time.wait(1000)  # Mostrar el mensaje por 1 segundo

# Función para guardar la partida en JSON
def guardar_partida(nombre, puntaje):
    partida = {
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Cargar el archivo de partidas si existe
    if os.path.exists("partidas.json"):
        with open("partidas.json", "r") as archivo:
            partidas = json.load(archivo)
    else:
        partidas = []

    # Agregar la nueva partida
    partidas.append(partida)

    # Guardar el archivo
    with open("partidas.json", "w") as archivo:
        json.dump(partidas, archivo, indent=4)

# Función para obtener y mostrar el TOP 10 de puntajes
def mostrar_top_10():
    pantalla.fill(BLANCO)
    mostrar_texto("TOP 10 Puntajes", 300, 50, NEGRO, fuente)

    # Cargar el archivo de partidas
    if os.path.exists("partidas.json"):
        with open("partidas.json", "r") as archivo:
            partidas = json.load(archivo)

        # Ordenar las partidas por puntaje (de mayor a menor)
        partidas.sort(key=lambda x: x['puntaje'], reverse=True)

        # Mostrar las mejores 10 partidas
        for i in range(min(10, len(partidas))):
            mostrar_texto(f"{i+1}. {partidas[i]['nombre']} - {partidas[i]['puntaje']} puntos", 50, 100 + i * 40, NEGRO, fuente_pequeña)
    else:
        mostrar_texto("No hay partidas guardadas.", 250, 100, NEGRO, fuente_pequeña)

    pygame.display.flip()

    # Esperar que el jugador regrese al menú
    esperando_regreso = True
    while esperando_regreso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Volver al menú principal al hacer clic
                if 300 < pygame.mouse.get_pos()[0] < 500 and 500 < pygame.mouse.get_pos()[1] < 550:
                    esperando_regreso = False
                    return

# Función para iniciar el juego
def iniciar_juego(preguntas):
    global vidas, puntos, respuestas_correctas, comodin_duplicar_puntos_usado, comodin_pasado_usado
    while vidas > 0:
        pregunta = random.choice(preguntas)  # Seleccionar una pregunta aleatoria
        mostrar_pregunta(pregunta)
        pygame.display.flip()

        esperando_respuesta = True
        while esperando_respuesta:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        verificar_respuesta(0, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_2:
                        verificar_respuesta(1, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_3:
                        verificar_respuesta(2, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_4:
                        verificar_respuesta(3, pregunta)
                        esperando_respuesta = False
                    elif evento.key == pygame.K_d:  # Duplicar puntos
                        if not comodin_duplicar_puntos_usado:
                            usar_comodin_duplicar_puntos()
                    elif evento.key == pygame.K_p:  # Pasar pregunta
                        if not comodin_pasado_usado:
                            pasar_siguiente_pregunta()

        # Mostrar puntos y vidas restantes
        pantalla.fill(BLANCO)
        mostrar_texto(f"Puntos: {puntos}", 50, 50, NEGRO, fuente)
        mostrar_texto(f"Vidas: {vidas}", 50, 100, NEGRO, fuente)
        pygame.display.flip()
        pygame.time.wait(1000)  # Esperar un segundo antes de mostrar la siguiente pregunta

    # Fin del juego
    mostrar_mensaje_perdido()
    nombre = pedir_nombre()
    if nombre:
        guardar_partida(nombre, puntos)

# Función principal
def main():
    global categoria_seleccionada
    mostrar_menu()

    jugando = False
    while not jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detectar si el jugador hace clic en el botón "Jugar"
                if 300 < pygame.mouse.get_pos()[0] < 500 and 300 < pygame.mouse.get_pos()[1] < 350:
                    mostrar_categorias()

                    # Esperar la selección de categoría
                    while categoria_seleccionada is None:
                        pygame.time.wait(100)

                    # Cargar las preguntas para la categoría seleccionada
                    preguntas = cargar_preguntas(categoria_seleccionada)
                    iniciar_juego(preguntas)
                    jugando = True

                # Detectar si el jugador hace clic en el botón "TOP 10"
                if 300 < pygame.mouse.get_pos()[0] < 500 and 400 < pygame.mouse.get_pos()[1] < 450:
                    mostrar_top_10()

# Iniciar el juego
main()