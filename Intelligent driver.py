import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True
x, y = 100, 100
speed = 0
dt = 0

class car:

    def __init__(self, pos, speed):
        self.texture = pygame.image.load("Data/red car.png")
        self.x, self.y = pos
        self.dx, self.dy = speed

    def render(self):
        screen.blit(self.texture, (self.x, self.y))

    def avance(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
    
    def accelere(self, ddx, ddy):
        self.dx += ddx
        self.dy += ddy

carr = car((100, 100), (10, 10))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    carr.avance(dt)
    carr.render()
    pygame.display.flip()

    dt = clock.tick(120)/1000  # limits FPS to 60

pygame.quit()