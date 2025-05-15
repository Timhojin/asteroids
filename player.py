from circleshape import CircleShape
from constants import *
from shot import Shot
import pygame

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.time = 0
        self.shield_time = 0
        self.shield = False


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if self.shield_time > 0:
            pygame.draw.polygon(screen, "red", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        self.time -= dt
        if self.shield_time > 0:
            self.shield_time -= dt
        else:
            self.shield = False
            self.radius = PLAYER_RADIUS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        
        if keys[pygame.K_SPACE]:
            self.shoot()
            
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.time > 0:
            return
        x = self.position.x
        y = self.position.y
        shot = Shot(x, y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        self.time = PLAYER_SHOOT_COOLDOWN

    def revive(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius *= 3
        self.shield = True
        self.shield_time = 3
    
    def check_shield(self, asteroid):
        if self.shield:
            asteroid.kill()
            return True
        return False