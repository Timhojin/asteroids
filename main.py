import pygame
from constants import * 
from player import Player
from asteroid import Asteroid
from asteroid_field import AsteroidField
from shot import Shot

def main():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(x, y)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)

    score = 0
    font = pygame.font.Font(None, 32)
    text = font.render(f"Current score: {score}", True, "white", None)
    textRect = text.get_rect()
    textRect.center = (x, 15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        text = font.render(f"Current score: {score}", True, "white", None)
        
        screen.blit(text, textRect)

        updatable.update(dt)
        for asteroid in asteroids:
            for bullet in shots:
                if bullet.collisionCheck(asteroid):
                    bullet.kill()
                    asteroid.split()
                    score += 1
            if player.collisionCheck(asteroid):
                print("Game Over!")
                print(f"Your final score: {score}")
                return
        for thing in drawable:
            thing.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()