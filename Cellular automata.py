import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import random as rd

def lire(emplacement): #Charger la grille initiale.
    grille = plt.imread(emplacement)
    n = len(grille)
    grille_texte = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if np.array_equal(grille[i][j], [1., 0., 0.]):
                grille_texte[i][j] = 2 #Rouge
            elif np.array_equal(grille[i][j], [0., 0., 1.]):
                grille_texte[i][j] = 1 #Bleu
            else:
                grille_texte[i][j] = 0 #Blanc
    return grille_texte

def convertir(grille): #Convertir la grille en image.
    n = len(grille)
    grille_nombres = np.zeros((n, n, 3), dtype=float)
    for i in range(n):
        for j in range(n):
            if grille[i][j] == 2:
                grille_nombres[i][j] = [1., 0., 0.]
            elif grille[i][j] == 1:
                grille_nombres[i][j] = [0., 0., 1.]
            else:
                grille_nombres[i][j] = [1., 1., 1.]
    return grille_nombres

def grille_vide(taille): #Renvoie une grille vide.
    grille = np.zeros( (taille, taille))
    for i in range(taille):
        for j in range(taille):
            grille[i][j] = 0
    return grille

def grille_aléatoire(taille, nb_voitures): #Peut devenir très lente si le nombre de voitures est très grand.
    grille = grille_vide(taille)
    libre = np.zeros((taille, taille), dtype=bool)
    k = 0
    while k < nb_voitures:
        couleur = rd.randint(1, 2)
        i = rd.randint(1, taille - 2)
        j = rd.randint(1, taille - 2)
        if not libre[i][j]:
            libre[i][j] = True
            grille[i][j] = couleur
            k += 1
    return grille

def suivant(grille_precedente): #Renvoie la grille à l'étape suivante.
    n = len(grille_precedente)
    grille = grille_vide(n)
    for i in range(1, n - 1): #Les voitures avancent d'abord horizontalement.
        for j in range(1, n - 2):
            if grille_precedente[i][j] == 1: #Si la voiture peut s'avancer, elle s'avance.
                if grille_precedente[i][j + 1] == 0:
                    grille[i][j + 1] = 1
                else:
                    grille[i][j] = 1
        if grille_precedente[i][n - 2] == 1: #la dernière colonne doit être traitée séparemment.
            if grille_precedente[i][1] == 0:
                grille[i][1] = 1
            else:
                grille[i][n - 2] = 1
    for j in range(1, n - 1): #Les voitures avancent ensuite verticalement.
        for i in range(1, n - 2):
            if grille_precedente[i][j] == 2:
                if grille[i + 1][j] == 0 and grille_precedente[i + 1][j] != 2: #Si une voiture bleu a avancé, cele peut libérer une place.
                    grille[i + 1][j] = 2
                else:
                    grille[i][j] = 2
        if grille_precedente[n - 2][j] == 2:
            if grille[1][j] == 0 and grille_precedente[1][j] != 2:
                grille[1][j] = 2
            else:
                grille[n - 2][j] = 2
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
grille = grille_aléatoire(200, 12000)
animation(grille, 1000)