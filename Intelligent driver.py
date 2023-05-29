import pygame
import math
import random as rd
import matplotlib.pyplot as plt

TAILLE_X = 800
TAILLE_Y = 800

pygame.init()
ecran = pygame.display.set_mode((TAILLE_X, TAILLE_Y))
horloge = pygame.time.Clock()
active = True
texture_rouge = pygame.image.load("Data/red car.png")
texture_bleu = pygame.image.load("Data/blue car.png")
texture_route = pygame.image.load("Data/green land.png")
texture_carrefour = pygame.image.load("Data/crossroad.png")
texture_vide = pygame.image.load("Data/empty road.png")

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
    duree_minimale = 1 # duree d'approche entre les 2 voitures successives
    acceletarion_maximale = 100
    deceleration_maximale = 100
    taille = 20
    facteur_zone = 1 # la largeur de la zone libre devant la voiture, par rapport à la taille de va voiture

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
        voiture.voitures.append(self)
    
    def effacer():
        voiture.voitures.clear()

    def afficher(self):
        ecran.blit(self.texture, (self.position.x - self.taille // 2, self.position.y - self.taille // 2))

    def voiture_suivante(self): # la distance par rapport à la voiture suivante et sa vitesse
        min_dist = 10**12
        dv = vecteur(0, 0)
        for autre in self.voitures:
            d_pos = autre.position - self.position
            if self.couleur == ROUGE:
                d_pos.x %= TAILLE_X
                if d_pos.x > self.taille and abs(d_pos.y) < self.taille * self.facteur_zone:
                    min_dist = min(d_pos.x, min_dist)
                    dv = self.vitesse - autre.vitesse
            else:
                d_pos.y %= TAILLE_Y
                if d_pos.y > self.taille and abs(d_pos.x) < self.taille * self.facteur_zone:
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
        distance, dv = self.voiture_suivante()
        self.acceleration = self.nouvelle_acceleration(distance, dv, self.vitesse_finale, self.distance_minimale, self.duree_minimale, self.acceletarion_maximale, self.deceleration_maximale)
        
        self.position += self.vitesse * dt
        self.vitesse += self.acceleration * dt

        self.position.x %= TAILLE_X # si on dépasse l'écran, on reapparait de l'autre côté
        self.position.y %= TAILLE_Y

def voitures_alealoires(nb_voitures):
    positions = rd.sample([(i * (voiture.taille) , j * (voiture.taille)) for j in range(1, TAILLE_X // voiture.taille) for i in range(1, TAILLE_Y // voiture.taille)], nb_voitures)
    couleurs = rd.sample([ROUGE, BLEU] * nb_voitures, nb_voitures)
    for i in range(nb_voitures):
        voiture(couleurs[i], positions[i][0], positions[i][1])

voitures_alealoires(300)

while active:
    dt = horloge.tick(165)/1000  # limite FPS to 165

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    ecran.blit(texture_vide, (0, 0))
    for v in voiture.voitures:
        v.logique(dt)
        v.afficher()
    pygame.display.flip()

pygame.quit()

def analyse_2(nb_valeurs, pas, nb_cycles_seconde, duree_totale, afficher = True):
    x = []
    y = []
    for i in range(1, nb_valeurs + 1):
        voiture.effacer()
        x.append(pas * i)
        voitures_alealoires(pas * i)
        for j in range(duree_totale):
            arretes = 0
            for v in voiture.voitures:
                v.logique(1 / nb_cycles_seconde)
                if v.vitesse.norme_euclidienne() < 1:
                    arretes += 1
            if arretes > (pas * i) * 0.75: # on considere que la route est bloquée si 75% de voitures sont bloqués
                break
            if j % 25 == 0:
                print("cycle:", i, "/", nb_valeurs, "duree:", j, "/", duree_totale)
        y.append(arretes / (pas * i))
    plt.plot(x, y)
    if afficher:
        plt.show()

# analyse_2(150, 1, 20, 40 * 20)

def analyse_3(nb_voitures, nb_cycles_seconde, duree_totale, afficher = True):
    x = []
    y = []
    voiture.effacer()
    voitures_alealoires(nb_voitures)
    for i in range(duree_totale):
        x.append(i / nb_cycles_seconde)
        arretes = 0
        for v in voiture.voitures:
            v.logique(1 / nb_cycles_seconde)
            if v.vitesse.norme_euclidienne() < 1:
                arretes += 1
        y.append(arretes / nb_voitures)
        if i % 25 == 0:
            print(i, "/", duree_totale)
    plt.plot(x, y, label=nb_voitures)
    plt.legend()
    if afficher:
        plt.show()

# analyse_3(100, 30, 40 * 30, False)
# analyse_3(200, 30, 40 * 30, False)
# analyse_3(300, 30, 40 * 30)

def moyenne_glissante(data, nb_points):
    resultat = []
    for i in range(len(data)):
        debut = max(i - nb_points, 0)
        longueur = i - debut + 1
        resultat.append(sum(data[debut:i + 1]) / longueur)
    return resultat

def analyse_4(nb_voitures, nb_cycles_seconde, duree_totale, afficher = True, plot = True):
    x = []
    y = []
    voiture.effacer()
    voitures_alealoires(nb_voitures)
    for i in range(duree_totale):
        if i % nb_cycles_seconde == 0:
            x.append(i // nb_cycles_seconde)
            y.append(0)
        passages = 0
        for v in voiture.voitures:
            pos_avant = v.position
            v.logique(1 / nb_cycles_seconde)
            if v.couleur == ROUGE:
                if pos_avant.x < (TAILLE_X // 2) and v.position.x >= (TAILLE_X // 2):
                    passages += 1
            else:
                if pos_avant.y < (TAILLE_Y // 2) and v.position.y >= (TAILLE_Y // 2):
                    passages += 1
        y[-1] += passages / nb_voitures
        if i % 25 == 0:
            print(i, "/", duree_totale)
    y = moyenne_glissante(y, 10) # moyenne glissante sur 10 secondes
    if plot:
        plt.plot(x, y, label=nb_voitures)
    if afficher:
        plt.legend()
        plt.show()
    return y

# plt.xlabel("temps (en s)")
# plt.ylabel("intensité de circulation (moyennée)")
# plt.title("intensité de circulation par seconde")
# analyse_4(25, 120, 90 * 120, False)
# analyse_4(50, 120, 90 * 120, False)
# analyse_4(75, 120, 90 * 120, False)
# analyse_4(100, 120, 90 * 120, False)
# analyse_4(125, 120, 90 * 120, False)
# analyse_4(150, 120, 90 * 120, False)
# analyse_4(200, 120, 90 * 120, False)
# analyse_4(300, 120, 90 * 120)

def moyenne_quart(lst):
    resultat = 0
    for i in range(3 * len(lst) // 4, len(lst)):
        resultat += lst[i] / (len(lst) // 4)
    return resultat

def analyse_5(nb_valeurs, pas, nb_cycles_seconde, duree_totale):
    x = []
    y = []
    for i in range(1, nb_valeurs + 1):
        print("cycle", i, "/", nb_valeurs)
        x.append(pas * i)
        y.append(moyenne_quart(analyse_4(pas * i, nb_cycles_seconde, duree_totale, False, False)))
    plt.plot(x, y)
    plt.xlabel("nombre de voitures")
    plt.ylabel("intensité de circulation finale")
    plt.title("intensité finale en donction du nombre de voitures")
    plt.show()

# analyse_5(30, 10, 120, 90 * 120)