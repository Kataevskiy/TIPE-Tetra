import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import random as rd

ROUGE = 2 #Les couleurs
BLEU = 1
BLANC = 0

def lire(emplacement): #Charger la grille initiale.
    grille = plt.imread(emplacement)
    n = len(grille)
    grille_texte = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if np.array_equal(grille[i][j], [1., 0., 0.]):
                grille_texte[i][j] = ROUGE
            elif np.array_equal(grille[i][j], [0., 0., 1.]):
                grille_texte[i][j] = BLEU
            else:
                grille_texte[i][j] = BLANC
    return grille_texte

def convertir(grille): #Convertir la grille en image.
    n = len(grille)
    grille_nombres = np.zeros((n, n, 3), dtype=float)
    for i in range(n):
        for j in range(n):
            if grille[i][j] == ROUGE:
                grille_nombres[i][j] = [1., 0., 0.]
            elif grille[i][j] == BLEU:
                grille_nombres[i][j] = [0., 0., 1.]
            else:
                grille_nombres[i][j] = [1., 1., 1.]
    return grille_nombres

def grille_vide(taille): #Renvoie une grille vide.
    grille = np.zeros( (taille, taille))
    for i in range(taille):
        for j in range(taille):
            grille[i][j] = BLANC
    return grille

def grille_aleatoire(taille, nb_voitures): #Peut devenir très lente si le nombre de voitures est très grand.
    grille = grille_vide(taille)
    positions = rd.sample([(i, j) for j in range(1, taille - 1) for i in range(1, taille - 1)], nb_voitures)
    couleurs = rd.sample([ROUGE, BLEU] * nb_voitures, nb_voitures)
    for i in range(nb_voitures):
        grille[positions[i][0]][positions[i][1]] = couleurs[i]
    return grille

def suivant(grille_precedente): #Renvoie la grille à l'étape suivante.
    n = len(grille_precedente)
    grille = grille_vide(n)
    
    for i in range(1, n - 1): #Les voitures avancent d'abord horizontalement.
        for j in range(1, n - 2):
            if grille_precedente[i][j] == BLEU: #Si la voiture peut s'avancer, elle s'avance.
                if grille_precedente[i][j + 1] == BLANC:
                    grille[i][j + 1] = BLEU
                else:
                    grille[i][j] = BLEU
        if grille_precedente[i][n - 2] == BLEU: #la dernière colonne doit être traitée séparemment.
            if grille_precedente[i][1] == BLANC:
                grille[i][1] = BLEU
            else:
                grille[i][n - 2] = BLEU

    for j in range(1, n - 1): #Les voitures avancent ensuite verticalement.
        for i in range(1, n - 2):
            if grille_precedente[i][j] == ROUGE:
                if grille[i + 1][j] == BLANC and grille_precedente[i + 1][j] != ROUGE: #Si une voiture bleu a avancé, cele peut libérer une place.
                    grille[i + 1][j] = ROUGE
                else:
                    grille[i][j] = ROUGE
        if grille_precedente[n - 2][j] == ROUGE:
            if grille[1][j] == BLANC and grille_precedente[1][j] != ROUGE:
                grille[1][j] = ROUGE
            else:
                grille[n - 2][j] = ROUGE
    return grille

def animation(grille, duree):
    fig, ax = plt.subplots()
    images = []
    for i in range(duree):
        cadre = ax.imshow(convertir(grille), animated=True)
        images.append([cadre])
        grille = suivant(grille)
    ani = anim.ArtistAnimation(fig, images, interval=10, blit=True, repeat_delay=1000)
    plt.show()

# grille1 = lire("Data/5 voitures.png")
# grille = grille_aleatoire(100, 5500)
# animation(grille, 500)

def analyse_1(nb_min, nb_max, pas, duree, afficher = True):
    y = []
    x = np.arange(nb_min, nb_max, pas)
    for i in range(nb_min, nb_max, pas):
        y.append(duree)
        grille = grille_aleatoire(50, i)
        for j in range(1, duree):
            nouvelle_grille = suivant(grille)
            if np.array_equal(nouvelle_grille, grille):
                y[-1] = j
                break
            grille = nouvelle_grille
        print(i, "/", nb_max)
    if afficher:
        plt.plot(x, y)
        plt.xlabel("Nombre de voitures")
        plt.ylabel("Nombre d'étapes")
        plt.title("Nombre moyen d'étapes avant le blocage de la route")
        plt.show()
    return x, y

# analyse_1(10, 2200, 10, 1000)

def analyse_2(nb_essais, nb_min, nb_max, pas, duree):
    Y = [0] * ((nb_max - nb_min) // pas)
    x = []
    for i in range(nb_essais):
        x, y = analyse_1(nb_min, nb_max, pas, duree, False)
        for i in range(len(y)):
            if y[i] < duree:
                Y[i] += 1 / nb_essais
    plt.plot(x, Y)
    plt.xlabel("Nombre de voitures")
    plt.ylabel("Probabilité de blocage")
    plt.title("Probabilité de blocage de la route")
    plt.show()

analyse_2(20, 800, 1300, 20, 500)