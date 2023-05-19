import pygame
import math

pygame.init()
ecran = pygame.display.set_mode((1600, 800))
horloge = pygame.time.Clock()
active = True
texture_rouge = pygame.image.load("Data/red car.png")
texture_bleu = pygame.image.load("Data/blue car.png")
texture_route = pygame.image.load("Data/green land.png")
texture_carrefour = pygame.image.load("Data/crossroad.png")

class vecteur:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def produit_scalaire(self, autre):
        return self.x * autre.x + self.y * autre.y
    
    def norme_euclidienne(self):
        return math.sqrt(self.x**2 + self.y**2)

    def distance_euclidienne(self, autre):
        return math.sqrt((self.x - autre.x)**2 + (self.y - autre.y)**2)

    def __add__(self, autre):
        return vecteur(self.x + autre.x, self.y + autre.y)

    def __sub__(self, autre):
        return vecteur(self.x - autre.x, self.y - autre.y)
    
    def __mul__(self, autre):
        if isinstance(autre, (int, float)):
            return vecteur(self.x * autre, self.y * autre)
        else:
            return vecteur(self.x * autre.x, self.y * autre.y)

    def __truediv__(self, a):
        return vecteur(self.x / a, self.y / a)

    def __pow__(self, a):
        return vecteur(self.x**a, self.y**a)


ROUGE = 1
BLEU = 2

class voiture:

    voitures = []
    vitesse_finale = 200
    distance_minimale = 50
    duree_minimale = 1
    acceletarion_maximale = 100
    deceleration_maximale = 100

    def __init__(self, couleur, x, y):
        self.position = vecteur(x, y) # position
        self.vitesse = vecteur(0, 0) # vitesse
        self.acceleration = vecteur(0, 0) # accélération
        self.couleur = couleur
        if couleur == ROUGE:
            self.texture = texture_rouge
            self.angle = 0
        else:
            self.texture = texture_bleu
            self.angle = math.radians(90)
        self.taille = self.texture.get_height() 

    def afficher(self):
        ecran.blit(self.texture, (self.position.x - self.taille // 2, self.position.y - self.taille // 2))

    def voiture_suivante(self, voitures): # la distance par rapport à la voiture suivante et sa vitesse
        min_dist = 10**12
        dv = vecteur(0, 0)
        for autre in voitures:
            d_pos = autre.position - self.position
            if self.couleur == ROUGE:
                d_pos.x %= 1600
                if d_pos.x > self.taille and abs(d_pos.y) < self.taille * 1:
                    min_dist = min(d_pos.x, min_dist)
                    dv = self.vitesse - autre.vitesse
            else:
                d_pos.y %= 800
                if d_pos.y > self.taille and abs(d_pos.x) < self.taille * 1:
                    min_dist = min(d_pos.y, min_dist)
                    dv = self.vitesse - autre.vitesse
        return min_dist, dv
    
    def nouvelle_acceleration(self, dist, dv, v_max, d_min, t_min, a_max, da_max):
        if self.vitesse.x < 0:
            self.vitesse.x = 0
        if self.vitesse.y < 0:
            self.vitesse.y = 0
        facteur_libre = (vecteur(1, 1) - (self.vitesse / v_max)**4) * a_max * vecteur(math.cos(self.angle), math.sin(self.angle))
        facteur_interaction = ((vecteur(d_min, d_min) + self.vitesse * t_min + (self.vitesse * dv / (2 * math.sqrt(a_max * da_max)))) / dist)**2 * (-a_max) * vecteur(math.cos(self.angle), math.sin(self.angle))
        return facteur_libre + facteur_interaction

    def logique(self, dt):
        distance, dv = self.voiture_suivante(self.voitures)
        self.acceleration = self.nouvelle_acceleration(distance, dv, self.vitesse_finale, self.distance_minimale, self.duree_minimale, self.acceletarion_maximale, self.deceleration_maximale)
        
        self.position += self.vitesse * dt
        self.vitesse += self.acceleration * dt

        self.position.x %= 1600 # si on dépasse l'écran, on reapparait de l'autre côté
        self.position.y %= 800

for i in range(10):
    voiture.voitures.append(voiture(ROUGE, 100 + 50 * i, 390 - 19))
    voiture.voitures.append(voiture(ROUGE, 100 + 50 * i, 390))
    voiture.voitures.append(voiture(ROUGE, 100 + 50 * i, 390 + 19))
    voiture.voitures.append(voiture(ROUGE, 100 + 50 * i, 390 + 19 + 19))
for i in range(10):
    voiture.voitures.append(voiture(BLEU, 390 - 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 390, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 390 + 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 390 + 19 + 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 790 - 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 790, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 790 + 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 790 + 19 + 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 1190 - 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 1190, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 1190 + 19, 100 + 50 * i))
    voiture.voitures.append(voiture(BLEU, 1190 + 19 + 19, 100 + 50 * i))

while active:
    dt = horloge.tick(165)/1000  # limite FPS to 165

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    ecran.blit(texture_carrefour, (0, 0))
    for v in voiture.voitures:
        v.logique(dt)
        v.afficher()
    pygame.display.flip()

pygame.quit()