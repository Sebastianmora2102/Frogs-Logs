import pygame
import sys

class Rana:
    def __init__(self, posiciones_hojas):
        #se instancia el uso del arreglo posiciones_hojas para la clase Rana
        self.posiciones_hojas = posiciones_hojas
        #inicializacion de la posicion de la rana (aparece en la primera hoja del arreglo)
        self.x, self.y = posiciones_hojas[0]
        #representacion de posiciones en el arreglo posiciones_hojas
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.posicion_actual = 0
        #velocidad de movimiento
        self.velocidad = 0.5

    def mover(self, direccion):
        #se inicializa una nueva variable como la actual para programar el recorrido de la rana
        posicion_nueva = self.posicion_actual
        #validaciones para verificar que el movimiento sea posible con residuo
        #si direccion es izquierda y la rana este en alguna posicion de la columna izquierda
        if direccion == "izquierda" and self.posicion_actual % 3 > 0:
            #permite movimiento a la izquierda
            posicion_nueva -= 1
        #si direccion es derecha y la rana no esta en la ultima columna
        elif direccion == "derecha" and self.posicion_actual % 3 < 2:
            #permite movimiento a la derecha
            posicion_nueva += 1
        #si direccion es arriba y la rana no esta en la primera fila
        elif direccion == "arriba" and self.posicion_actual >= 3:
            #permite movimiento hacia arriba
            posicion_nueva -= 3
        #si direccion es abajo y la rana no esta en la ultima fila
        elif direccion == "abajo" and self.posicion_actual < 6:
            #permite movimiento hacia abajo
            posicion_nueva += 3
        #validacion para verificar si la nueva posicion es diferente a la actual y si ese es el caso que se mueva
        if posicion_nueva != self.posicion_actual:
            self.posicion_actual = posicion_nueva
            self.x, self.y = self.posiciones_hojas[self.posicion_actual]

class Ventana:
    def __init__(self, ancho, alto, titulo):
        #inicialización de la ventana principal y sus atributos
        self.ancho = ancho
        self.alto = alto
        self.rana_puede_mover = True
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        #nombre la de interfaz
        pygame.display.set_caption(titulo)
        #---------------------------------------------------------------------------------------------------
        # RIO
        #---------------------------------------------------------------------------------------------------
        #definicion de fondo y su animacion
        self.fondo = pygame.image.load('images/8bitwater.png')
        #autoescalado de la imagen para que se ajuste al tamaño de la interfaz
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.alto))
        #se definen dos variables de posicion para para generar un bucle infinito sin distorcion del fondo
        #posicion inicial del fondo en la interfaz
        self.fondo_x1 = 0
        #la segunda posicion del fondo se define al tamaño del ancho para evitar distorcion del fondo
        #asi al acabar de moverse el primero siempre habra otro concatenado
        self.fondo_x2 = self.ancho
        #velocidad de movimiento del fondo
        self.velocidad_fondo = 0.5
        #---------------------------------------------------------------------------------------------------
        # HOJAS
        #---------------------------------------------------------------------------------------------------
        #se carga la imagen de la hoja
        self.hoja = pygame.image.load('images/nenufar.png')
        #redimencionanmiento de la imagen para que alcanze en la ventana
        self.hoja = pygame.transform.scale(self.hoja, (130, 130)) 
        #arreglo de ubicaciones de cada hoja en ventana
        self.posiciones_hojas = [
            (75, 60),  (325, 60),  (575, 60), 
            (75, 250), (325, 250), (575, 250), 
            (75, 440), (325, 440), (575, 440)
        ]
        #---------------------------------------------------------------------------------------------------
        # RANA
        #---------------------------------------------------------------------------------------------------
        #se crea un objeto rana para ser manipulado en las posiciones de las hojas
        self.rana = Rana(self.posiciones_hojas)
        #se carga la imagen de la rana
        self.imagen_rana = pygame.image.load('images/frog.png')
        #redimencionanmiento de la imagen
        self.imagen_rana = pygame.transform.scale(self.imagen_rana, (150, 150))

    def dibujar_rana(self):
        #calculo de desplazamiento necesario para que la rana se centre en la hoja
        desplazamiento_x = (130 - 150) // 2  
        desplazamiento_y = (130 - 150) // 2    
        #se dibuja la rana en la ventana con blit 
        #se tiene en cuenta las variables desplazamiento para centrar la rana en la hoja
        self.ventana.blit(self.imagen_rana, (self.rana.x + desplazamiento_x, self.rana.y + desplazamiento_y))

    def eventos_teclado(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #obtiene el estado actual de todas las teclas del teclado
        keys = pygame.key.get_pressed()
        #si la tecla de flecha izquierda está presionada y la rana puede moverse
        if keys[pygame.K_LEFT] and self.rana_puede_mover:
            self.rana.mover("izquierda")
            self.rana_puede_mover = False
        elif keys[pygame.K_RIGHT] and self.rana_puede_mover:
            self.rana.mover("derecha")
            self.rana_puede_mover = False
        elif keys[pygame.K_UP] and self.rana_puede_mover:
            self.rana.mover("arriba")
            self.rana_puede_mover = False
        elif keys[pygame.K_DOWN] and self.rana_puede_mover:
            self.rana.mover("abajo")
            self.rana_puede_mover = False
        #si ninguna tecla de dirección está presionada indica que la rana puede moverse nuevamente
        elif not any(keys):
            self.rana_puede_mover = True

    def manejo_fondo(self):
        #se define una reduccion en la posicion actual del fondo en base a la velocidad establecida
        #esto simula un efecto de movimiento de derecha a izquiera
        self.fondo_x1 -= self.velocidad_fondo
        self.fondo_x2 -= self.velocidad_fondo
        #validacion para cuando el primer fondo cruce el ancho total de la ventana este se ubique nuevamente de donde salio
        if self.fondo_x1 <= -self.ancho:
            self.fondo_x1 = self.ancho
        #validacion para cuando el segundo fondo cruce el ancho total de la ventana este se ubique nuevamente de donde salio
        if self.fondo_x2 <= -self.ancho:
            self.fondo_x2 = self.ancho
        #atraves de la funcion blit se imprimen los fondos en pantalla
        self.ventana.blit(self.fondo, (self.fondo_x1, 0))
        self.ventana.blit(self.fondo, (self.fondo_x2, 0))

    def hojas(self):
        #atraves de blit imprime la imagen de la hoja redimenzionada en las posiciones del arreglo posiciones_hojas
        for posicion in self.posiciones_hojas:
            self.ventana.blit(self.hoja, posicion)
    
    def cierre(self):
        #detecta y trae los eventos que suceden en pantalla
        for evento in pygame.event.get():
            #si el evento representa un cierra de la aplicacion
            if evento.type == pygame.QUIT:
                #función que libera la carga de recursos que se hayan ejecutado para cerrar la aplicación
                pygame.quit()
                #cierre de forma inmediata
                sys.exit()     
    
    def actualizar(self):  
        self.manejo_fondo()
        self.cierre()
        self.hojas()
        self.dibujar_rana()
        self.eventos_teclado()
        #actualiza eventos para que se ejecuten en la ventana
        pygame.display.update()

#inicializacion pygame
pygame.init()
#definicion de atributos para inicialización de la pantalla del juego a través de la clase Ventana
pantalla = Ventana(900, 600, "Frogs & Logs")
#bucle principal del juego
while True:
    pantalla.actualizar()

