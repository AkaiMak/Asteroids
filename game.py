#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Студент
#
# Created:     04.03.2025
# Copyright:   (c) Студент 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Астероиды (Вертикальный Скроллер)")

# Цвета
myimage = pygame.image.load("img/stars-universe.gif")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/Hero.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.rotation = 0
        self.rotation_speed = 3
        self.lives = 3 # initial lives

    def update(self):
        keys = pygame.key.get_pressed()
        dx = self.speed
        if keys[pygame.K_LEFT]:
            self.rotation -= self.rotation_speed
            self.rect.x -= dx
        if keys[pygame.K_RIGHT]:
            self.rotation += self.rotation_speed
            self.rect.x += dx
        self.rotation = self.rotation

        # Calculate movement based on rotation
        rads = self.rotation
        dy = -self.speed  # Invert Y for Pygame coordinates

        if keys[pygame.K_UP]:
            self.rect.y += dy
        if keys[pygame.K_DOWN]:
            self.rect.y -= dy

        # Ограничение движения по краям экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Rotate the image (do not rotate self.image or it will become distorted)
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)  # Update rect after rotation

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.rotation)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            return True  # Game over
        else:
            return False # Game continues
            # Reset player position or apply some invincibility
            self.rect.center = (WIDTH // 2, HEIGHT - 50)


# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation, is_player=True):
        super().__init__()
        self.image = pygame.image.load("img/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.rotation = rotation
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        self.is_player = is_player

    def update(self):
        rads = math.radians(self.rotation)
        dx = math.cos(rads)
        dy = -self.speed

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

class Bullet_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation, is_player=True):
        super().__init__()
        self.image = pygame.image.load("img/enemy-bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.rotation = rotation
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        self.is_player = is_player  # Track if the bullet belongs to the player

    def update(self):
        rads = math.radians(self.rotation)
        dx = math.cos(rads) * self.speed
        dy = math.sin(rads) * -self.speed

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()


# Класс астероида
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/AsteroidMedium.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)
            self.speedx = random.randrange(-2, 2)


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 7)
        self.speedx = random.randrange(-3, 3)
        self.shoot_delay = 1000  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(3, 7)
            self.speedx = random.randrange(-3, 3)

        # Enemy shooting logic
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemy_bullet = Bullet_Enemy(self.rect.centerx, self.rect.bottom, 270, is_player=False) # Always shoot down
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)


# Создание спрайтов
player = Player(WIDTH // 2, HEIGHT - 50)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

asteroids = pygame.sprite.Group()
for i in range(5):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

enemies = pygame.sprite.Group()
for i in range(2):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_killed = 0

# Игровой цикл
clock = pygame.time.Clock()
running = True
game_over = False # Add game_over flag

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:  # Only shoot if not game over
                player.shoot()

    # Обновление
    if not game_over:
        all_sprites.update()

        # Проверка столкновений
        collisions = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for collision in collisions:
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        enemy_collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for collision in enemy_collisions:
            enemy_killed += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        player_hits = pygame.sprite.spritecollide(player, asteroids, False)
        if player_hits:
            game_over = player.lose_life() # Game continues? If false then game_over = true

        player_enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        if player_enemy_hits:
            game_over = player.lose_life()

        player_bullet_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if player_bullet_hits:
            game_over = player.lose_life()

    # Отрисовка
    surf = pygame.image.load('img/stars-universe.gif')
    rect = surf.get_rect(center=(0,0))
    surf = pygame.transform.scale(surf, (1600, 800))
    screen.fill(BLACK)
    screen.blit(surf, rect)
    all_sprites.draw(screen)

    # Draw lives
    font = pygame.font.Font(None, 30)
    lives_text = font.render(f"Жизни: {player.lives}", True, WHITE)
    enemy_killed_text = font.render(f"Убито врагов: {enemy_killed}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(enemy_killed_text, (10, 40))

    # Game over screen
    if game_over:
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.fill(BLACK)
        screen.blit(game_over_text, text_rect)
        lives_text = font.render(f"Жизни: {player.lives}", True, WHITE)
        enemy_killed_text = font.render(f"Убито врагов: {enemy_killed}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(enemy_killed_text, (10, 40))

    # Обновление экрана
    pygame.display.flip()

    # Контроль FPS
    clock.tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()