import pygame

pygame.init()
ecran = pygame.display.set_mode((1600, 800))
horloge = pygame.time.Clock()
active = True
texture_rouge = pygame.image.load("Data/red car.png")
texture_route = pygame.image.load("Data/green land.png")
voitures = []

class voiture:

    def __init__(self, texture, x, y, vx = 0, vy = 0, vmax = 200):
        self.x, self.y = x, y #position
        self.vx, self.vy = 50, 0 #vitesse
        self.ax, self.ay = 0, 0 #accélération
        self.vmax = vmax
        self.texture = texture

    def afficher(self):
        ecran.blit(self.texture, (self.x - 8, self.y - 8))

    def distance_minimale(self, voitures): #la distance POSITIVE minimale par rapport aux autres voitures
        min_dist = 10**12
        for v in voitures:
            if v.x >= self.x:
                dx =  v.x - self.x
            else:
                dx = 1600 - self.x + v.x
            if v.y >= self.y:
                dy = v.y - self.y
            else:
                dy = 1600 - self.y + v.y
            dist = dx**2 + dy**2
            if dist > 0:
                min_dist = min(min_dist, dist)
        return min_dist
        
    def logique(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        distance = self.distance_minimale(voitures)

        if distance < 5000:
            self.ax = -200
        elif distance >= 5000:
            self.ax = 200
        if self.vx > self.vmax:
            self.ax = 0
            self.vx = self.vmax
        elif self.vx < 0:
            self.ax = 0
            self.vx = 0
        
        if self.x > 1600:
            self.x -= 1600
        if self.y > 800:
            self.y -= 800

voitures.append(voiture(texture_rouge, 0, 390, 200, 0, 200))
voitures.append(voiture(texture_rouge, 800, 390, 50, 0, 50))

while active:
    dt = horloge.tick(165)/1000  # limits FPS to 165

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    ecran.blit(texture_route, (0, 0))
    for v in voitures:
        v.logique(dt)
        v.afficher()
    pygame.display.flip()

pygame.quit()