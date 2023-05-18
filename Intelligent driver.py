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


class voiture:

    voitures = []
    vitesse_finale = 100
    distance_minimale = 50
    duree_minimale = 1
    acceletarion_maximale = 100
    deceleration_maximale = 100

    def __init__(self, texture, x, y, angle):
        self.position = vecteur(x, y) # position
        self.angle = angle # orientation par rapport à la horizontale
        self.vitesse = vecteur(0, 0) # vitesse
        self.acceleration = vecteur(0, 0) # accélération
        self.texture = texture
        self.taille = texture.get_height() 

    def afficher(self):
        ecran.blit(self.texture, (self.position.x - self.taille // 2, self.position.y - self.taille // 2))

    def voiture_suivante(self, voitures): # la distance par rapport à la voiture suivante et sa vitesse
        min_dist = 10**12
        dv = vecteur(0, 0)
        for autre in voitures:
            for correction_x in [-1600, 0, 1600]:
                for correction_y in [-800, 0, 800]:
                    autre_possibilite = vecteur(correction_x, correction_y) + autre.position
                    vecteur_distance = autre_possibilite - self.position
                    vecteur_direction = vecteur(math.cos(self.angle), math.sin(self.angle))
                    projete = vecteur.produit_scalaire(vecteur_distance, vecteur_direction)
                    distance_au_projete = vecteur.distance_euclidienne(vecteur_distance, vecteur_direction * projete)
                    if projete > self.taille and distance_au_projete < (1 * self.taille) and projete < min_dist:
                        min_dist = projete
                        dv = self.vitesse - autre.vitesse
        return min_dist, dv
    
    def nouvelle_acceleration(self, dist, dv, v_max, d_min, t_min, a_max, da_max):
        if self.vitesse.x < -self.vitesse_finale / 10:
            self.vitesse.x = -self.vitesse_finale / 10
        if self.vitesse.y < -self.vitesse_finale / 10:
            self.vitesse.y = -self.vitesse_finale / 10
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
    voiture.voitures.append(voiture(texture_rouge, 100 + 50 * i, 390 - 19, 0))
    voiture.voitures.append(voiture(texture_rouge, 100 + 50 * i, 390 + 19 + 19, 0))
for i in range(5):
    voiture.voitures.append(voiture(texture_bleu, 390 - 19, 100 + 50 * i, math.radians(90)))
    voiture.voitures.append(voiture(texture_bleu, 390 + 19 + 19, 100 + 50 * i, math.radians(90)))
    voiture.voitures.append(voiture(texture_bleu, 790 - 19, 100 + 50 * i, math.radians(90)))
    voiture.voitures.append(voiture(texture_bleu, 790 + 19 + 19, 100 + 50 * i, math.radians(90)))
    voiture.voitures.append(voiture(texture_bleu, 1190 - 19, 100 + 50 * i, math.radians(90)))
    voiture.voitures.append(voiture(texture_bleu, 1190 + 19 + 19, 100 + 50 * i, math.radians(90)))

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