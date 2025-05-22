import pygame
import random
import time
import cv2
import sys


class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, life = 3):
        self.puntaje = 0
        super().__init__()
        self.img = pygame.image.load("menem.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (70,70))
        self.image = self.img
        self.life = life
        self.ultima_direccion = "derecha"
     

        # Colision para el jugador
        self.momento_muerte = None
        self.explosion_img = pygame.image.load("explosion.png").convert_alpha()
        self.explosion_img = pygame.transform.scale(self.explosion_img, (60,60))


        self.rect = self.image.get_rect(topleft=(x, y)) # Le asigno la posicion
        self.velocidad = velocidad

    def mover(self, direccion):
        if direccion == 'izq':
            self.rect.x -= self.velocidad
            angulo = 90
            self.ultima_direccion = "izquierda"
        elif direccion == 'der':
            self.rect.x += self.velocidad
            angulo = -90
            self.ultima_direccion = "derecha"
        elif direccion == 'arr':
            self.rect.y -= self.velocidad
            angulo = 0
            self.ultima_direccion = "arriba"
        elif direccion == 'abj':
            self.rect.y += self.velocidad
            angulo = 180
            self.ultima_direccion = "abajo"

        # Limitar al fondo segun el tamano de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1200:
            self.rect.right = 1200
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 1200:
            self.rect.bottom = 1200

        self.image = pygame.transform.rotate(self.img, angulo)

    def morir(self):
        self.image = self.explosion_img #se muestra la explosion
        self.velocidadx = 0
        self.velocidady = 0
        self.vivo = False
        self.momento_muerte = time.time()  # Marca el momento de la explosión
    
    def incrementarPuntaje(self):
        self.puntaje += 1
    
    def descontarVida(self):
        if self.life > 0: 
            self.life -= 1

    def jugadorVerVida(self):
        return self.life


class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, ruta, velocidad):
        self.vivo = True
        self.momento_muerte = None 
        super().__init__()
        self.img = pygame.image.load(ruta).convert_alpha()
        self.image = pygame.transform.scale(self.img, (60,60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = velocidad
        self.momento_colision = 0
        
        self.velocidadx = random.choice([-1,-1,0,1,1])*velocidad
        self.velocidady = random.choice([-1,-1,0,1,1])*velocidad

        self.momento_muerte = None
        self.explosion_img = pygame.image.load("explosion.png").convert_alpha()
        self.explosion_img = pygame.transform.scale(self.explosion_img, (60,60))

    def mover(self, ancho, alto):
        self.rect.x += self.velocidadx
        self.rect.y += self.velocidady


        #Mueve al personaje si toca los bordos      
        if self.rect.x + self.rect.width>=ancho or self.rect.x<=0:
            self.velocidadx *= -1
            
        if self.rect.y + self.rect.height>=alto or self.rect.y<=0:
            self.velocidady *= -1
            
    def morir(self):
        self.image = self.explosion_img
        self.velocidadx = 0
        self.velocidady = 0
        self.vivo = False
        self.momento_muerte = time.time()
    
    def revivir(self):
        self.image = self.img
        self.image = pygame.transform.scale(self.img, (60,60))
        self.velocidadx = random.choice([-1,-1,0,1,1])*self.velocidad
        self.velocidady = random.choice([-1,-1,0,1,1])*self.velocidad
        self.vivo = True
        self.momento_muerte = None

class Alien (Personaje): 
    def __init__(self, x, y):
        super().__init__(x, y, "alien.png", 6)

class Alien2(Personaje):
    def __init__(self, x, y):
        super().__init__(x, y, "alien2.png", 4)

class Alienk(Personaje):
    def __init__(self, x, y):
        super().__init__(x, y, "alienk.png", 4)
        self.image = pygame.transform.scale(self.img, (100,100))


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.image = pygame.image.load("bala.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10,7))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 10
        self.direccion = direccion

              
    def mover(self):
        if self.direccion == "derecha":
            self.rect.x += self.velocidad
        elif self.direccion == "izquierda":
            self.rect.x -= self.velocidad
        elif self.direccion == "arriba":
            self.rect.y -= self.velocidad
        elif self.direccion == "abajo":
            self.rect.y += self.velocidad



pygame.init()
pygame.font.init()

#Configura la pantalla
ancho, alto = 800, 600 # tuplas
pantalla = pygame.display.set_mode((ancho, alto)) # Se crea la ventana con las tuplas
fondo = pygame.image.load("saturno.jpg").convert()
fondo = pygame.transform.scale(fondo, (1200, 1200))  # que sea más grande que la pantalla, simula el scroling
pygame.display.set_caption("El MenemGame")
clock = pygame.time.Clock() 

video = cv2.VideoCapture("intro.mp4")

jugador = Jugador(120, 120, velocidad=4)

personajes = pygame.sprite.Group()
scroll_x = 0
scroll_y = 0

for _ in range(8):
    #creamos 3 walker
    x = random.randint(90, 1200 - 60)
    y = random.randint(90, 1200 - 60)
    personaje = Alien(x, y)
    personajes.add(personaje)

    #creamos 3 yelena
    x = random.randint(90, 1200 - 60)
    y = random.randint(90, 1200 - 60)
    personaje = Alien2(x, y)
    personajes.add(personaje)

#creamos 3 Alienk
    x = random.randint(90, 1200 - 60)
    y = random.randint(90, 1200 - 60)
    personaje = Alienk(x, y)
    personajes.add(personaje)


todos = pygame.sprite.Group()
todos.add(jugador)
todos.add(personajes)  

reloj = pygame.time.Clock() #Controlamos los frame del programa
corriendo = True
tiempo_colision = 0
tiempo_colision_Alienk = 0
colisionConAlienk = False

balas = pygame.sprite.Group()

fuente_final = pygame.font.SysFont(None, 60)  # Usar fuente del sistema, tamaño 60
imagen_menem = pygame.image.load("menemwin.png").convert_alpha()  
imagen_menem = pygame.transform.scale(imagen_menem, (120, 120)) 


while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            video.release()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Saltear video
                video.release()
                break

    # Convertir el frame de BGR a RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)  # Opcional: si lo ves rotado
    frame_surface = pygame.surfarray.make_surface(frame)

    # Escalar si es necesario
    frame_surface = pygame.transform.scale(frame_surface, (ancho, alto))

    # Mostrar en la ventana
    pantalla.blit(frame_surface, (0, 0))
    pygame.display.update()
    clock.tick(30)  # Asegurar FPS constante

video.release()

while corriendo: #Todo juego corre dentro de un bucle
    reloj.tick(40)
    for evento in pygame.event.get(): #Para cerrar la ventana del juego
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                nueva_bala = Bala(jugador.rect.centerx, jugador.rect.centery, jugador.ultima_direccion)
                balas.add(nueva_bala)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jugador.mover('izq')

    if keys[pygame.K_RIGHT]:
        jugador.mover('der')

    if keys[pygame.K_UP]:
        jugador.mover('arr')
        scroll_y -= jugador.velocidad

    if keys[pygame.K_DOWN]:
        jugador.mover('abj')
        scroll_y += jugador.velocidad

    for bala in list(balas):
        if (bala.rect.x < 0 or bala.rect.x > 1200 or bala.rect.y < 0 or bala.rect.y > 1200):
            balas.remove(bala)
   
    scroll_x = max(0, min(scroll_x, 1200 - ancho))
    scroll_y = max(0, min(scroll_y, 1200 - alto))

    # Centramos la cámara en el jugador
    offset_x = jugador.rect.centerx - ancho // 2
    offset_y = jugador.rect.centery - alto // 2
    offset_x = max(0, min(offset_x, fondo.get_width() - ancho))
    offset_y = max(0, min(offset_y, fondo.get_height() - alto))

   
    for p in personajes:
        p.mover(ancho, alto)
        # Eliminar personajes muertos después de 1 segundo
        if not p.vivo and p.momento_muerte and time.time() - p.momento_muerte > 1:
            personajes.remove(p)
            todos.remove(p)

        #devuelve el objeto con el que choque
    p = pygame.sprite.spritecollideany(jugador, personajes)

    if isinstance(p, Alienk) and time.time() - tiempo_colision_Alienk >= 3:
        jugador.descontarVida()
        tiempo_colision_Alienk = time.time()
        print("Vida Jugador:", jugador.jugadorVerVida())
    
    if not p:
        colisionConAlienk = False
  

    if p and p.vivo and time.time() - p.momento_colision>= 3:
        p.morir()
        p.momento_colision = time.time()  # Guarda el momento exacto de la colisión
      #  colision_habilitada = False
        jugador.incrementarPuntaje()
        print(jugador.puntaje)
        
    if p and not p.vivo and p.momento_colision and time.time() - p.momento_muerte >= 1:
        p.revivir()
        p.momento_colision = time.time()

        #  if time.time() - tiempo_colision >= 5:
        #   colision_habilitada = True
    
    for bala in balas:
        bala.mover()

    pantalla.blit(fondo, (-offset_x, -offset_y))

    for bala in list(balas):
        bala.mover()
        pantalla.blit(bala.image, (bala.rect.x - offset_x, bala.rect.y - offset_y))

    for p in personajes:
        pantalla.blit(p.image, (p.rect.x - offset_x, p.rect.y - offset_y))

    pantalla.blit(jugador.image, (jugador.rect.x - offset_x, jugador.rect.y - offset_y))

    for entidad in todos:
        pantalla.blit(entidad.image, (entidad.rect.x - offset_x, entidad.rect.y - offset_y))

    balas.update()

    if len(personajes) == 0:
        pantalla.fill((0, 0, 0))  # Fondo negro
        texto = fuente_final.render("Menem lo hizo!", True, (255, 0, 0))  # Texto rojo brillante

        # Centrar el texto y la imagen en la pantalla
        texto_rect = texto.get_rect(center=(ancho // 2 - 60, alto // 2))
        imagen_rect = imagen_menem.get_rect(midleft=(texto_rect.right + 10, texto_rect.centery))

        pantalla.blit(texto, texto_rect)
        pantalla.blit(imagen_menem, imagen_rect)
        pygame.display.flip()

        # Congela la pantalla por unos segundos o espera que se cierre
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    corriendo = False
            reloj.tick(10)
        continue  # Saltea el resto del bucle del juego

    pygame.display.update()

    for bala in balas:
        enemigos_danados = pygame.sprite.spritecollide(bala, personajes, False)
        pantalla.blit(bala.image, (bala.rect.x - offset_x, bala.rect.y - offset_y))
        for enemigo in enemigos_danados:
            if enemigo.vivo:
                enemigo.morir()
                jugador.incrementarPuntaje()
                print("Puntaje:", jugador.puntaje)
                bala.kill()
 
   

pygame.font.quit()
pygame.quit() 