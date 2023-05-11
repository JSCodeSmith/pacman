import pygame
from random import randint, choice

pygame.init()

width = 800
height = 600
speed = 5
fps = 30
counter = 0

clock = pygame.time.Clock()

surface = pygame.display.set_mode((width, height))

pygame.display.set_caption("Mi Juego Gracias a Codigo Facilito ")


pygame.mixer.init()
pygame.mixer.music.load("./Quetevayabien.mp3")
pygame.mixer.music.play(loops=-1)

icon_image = pygame.image.load("estudiante.png")
pygame.display.set_icon(icon_image)
font = pygame.font.SysFont("Courier New", 30)


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = choice(["up", "down", "left", "right"])

    def update(self):
        if self.direction == "up":
            self.rect.y -= speed
        elif self.direction == "down":
            self.rect.y += speed
        elif self.direction == "left":
            self.rect.x -= speed
        elif self.direction == "right":
            self.rect.x += speed

        if self.rect.top < 0:
            self.direction = choice(["down", "left", "right"])
        elif self.rect.bottom > height:
            self.direction = choice(["up", "left", "right"])
        elif self.rect.left < 0:
            self.direction = choice(["up", "down", "right"])
        elif self.rect.right > width:
            self.direction = choice(["up", "down", "left"])






player = Character(100, 100, "iconos.png")

circles = pygame.sprite.Group()
enemies = pygame.sprite.Group()


for i in range(0, 50):
    circle = Circle(randint(0, width), randint(0, height), 20, (255, 0, 0))
    circles.add(circle)

for i in range(0, 2):
    enemy = Enemy(randint(0, width), randint(0, height), "enemigo.png")
    enemies.add(enemy)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move(-speed, 0)
    if keys[pygame.K_RIGHT]:
        player.move(speed, 0)
    if keys[pygame.K_UP]:
        player.move(0, -speed)
    if keys[pygame.K_DOWN]:
        player.move(0, speed)

    surface.fill((255, 255, 255))

    circles.update()
    enemies.update()


    # Dibuja el personaje y los círculos
    surface.blit(player.image, player.rect)
    circles.draw(surface)
    enemies.draw(surface)

    # Detecta colisiones entre el personaje y los círculos
    for circle in circles:
        if pygame.sprite.collide_mask(player, circle):
            circles.remove(circle)
            counter += 1
        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
            pygame.quit()
            exit()
 
    text = font.render(f"Tus Puntuajes: {counter}", True, (0, 0, 0))
    surface.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(fps)
