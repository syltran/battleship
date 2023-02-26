# AOUDIA HAKIM / TRAN SYLVAIN
# ****CODE DU JEU****
import fltk
from random import randint


def init_plateau(n):
    """
    Renvoie une liste de liste représentant un plateau de
    n cases de côté, comportant seulement des 0.
    :param n: int
    :return value : liste de liste

    >>> init_plateau(2)
    [[0, 0], [0, 0]]
    >>> init_plateau(4)
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    """
    lst = []
    for i in range(n):
        lst.append([0] * n)
    return lst


def draw_grille(plateau, xPlateau, yPlateau):
    """
    Permet de dessiner la grille d'un plateau
    Les variables xPlateau et yPlateau permettent
    de positionner le plateau ou on veut.

    La fonction ne retourne rien elle dessine seulement
    à l'écran des traits et des numéros indiquant les lignes
    et les colonnes

    :param plateau: list
    :param xPlateau: int
    :param yPlateau: int
    """
    for i in range(len(plateau) + 1):
        fltk.ligne(xPlateau, yPlateau+i*cote_case, xPlateau+cote_case*nb_case,
                   yPlateau + i*cote_case, couleur='DarkOrange')  # ligne
        fltk.ligne(xPlateau+i*cote_case, yPlateau, xPlateau+i*cote_case,
                   yPlateau+cote_case*nb_case, couleur='DarkOrange')  # colonne

    for i in range(len(plateau)):
        fltk.texte(xPlateau-10, yPlateau + cote_case/2 + i*cote_case, str(i),
                   ancrage='center', taille=10, couleur='white')  # num ligne
        fltk.texte(xPlateau + cote_case/2 + i*cote_case, yPlateau-10, str(i),
                   ancrage='center', taille=10, couleur='white')  # num colonne


def affiche_choixBoats(cmptBoats, xpos, ypos):
    """
    Affiche à l'écran l'ensemble des bateaux à poser.
    Ne retourne rien la fonction écrit
    seulement du texte à l'écran.

    :param cmptBoats: list
    :param xpos: int
    :param ypos: int
    """
    for i in range(len(cmptBoats)):
        msg1, msg2 = "  navire de ", " case"
        if cmptBoats[i] >= 2:
            msg1 = "  navires de "
        if i > 0:
            msg2 = " cases"
        fltk.texte(xpos, ypos+i*50, str(cmptBoats[i]) + msg1 + str(i+1) + msg2,
                   couleur='white', taille=22,
                   ancrage="nw", tag='choixBoats')


# --------------------PARTIE BATEAU--------------------
def choisir_boats(xFleche, yFleche):
    """
    Permet de choisir quel bateau placer parmis
    l'ensemble des bateaux disponibles avec une
    flèche contrôlée à l'aide des touches directionnelles
    du clavier.
    En appuyant sur la touche p, les bateaux seront posés automatiquement.
    Si des bateaux ont déjà été placé sur le plateau, il est possible de placer
    automatiquement les bateaux restants en appuyant sur la même touche p.

    :param xFleche: int
    :param yFleche: int

    :return -1: int
    :return pos_fleche: int
    """
    pos_fleche = 0

    while True:
        fltk.efface('fleche')
        fltk.efface('choixBoats')
        fltk.rectangle(457, 55, 740, 338,
                       remplissage='black', tag='choixBoats')
        affiche_choixBoats(cmptBoats, 460, 50)
        fltk.image(xFleche, yFleche, "fleche.png", tag='fleche')
        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Touche':
            if fltk.touche(ev) == "Up":
                if pos_fleche > 0:
                    yFleche -= 50
                    pos_fleche -= 1

            elif fltk.touche(ev) == "Down":
                if pos_fleche < 5:
                    yFleche += 50
                    pos_fleche += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                if cmptBoats[pos_fleche] > 0:
                    cmptBoats[pos_fleche] -= 1
                    fltk.efface('fleche')
                    fltk.efface('choixBoats')
                    return pos_fleche

            elif fltk.touche(ev) == 'p':
                poseAuto_boats(cmptBoats)
                affiche_boats(plateau)
                fltk.efface('fleche')
                fltk.efface('choixBoats')
                return -1


def creer_boat(nb):
    """
    Créer un bateau de nb+1 cases au centre du plateau.
    Chaque bateau est représenté par une liste de couples de coordonnées.
    Ces couples représentent les cases du bateaux.
    :param : int
    :return value: list

    >>> creer_boat(0)
    [(10, 10)]
    >>> creer_boat(2)
    [(10, 10), (11, 10), (12, 10)]
    >>> creer_boat(4)
    [(10, 10), (11, 10), (12, 10), (13, 10), (14, 10)]
    """
    lst = []
    for i in range(nb+1):
        lst.append((int(nb_case / 2) + i, int(nb_case / 2)))
    return lst


def affiche_tmpBoat(tmpBoats):
    """
    Permet d'afficher le bateau qu'on essaye de poser sur le plateau.
    :param : liste
    """
    for coord in tmpBoats:
        x, y = coord
        fltk.rectangle(xPlateau + x*cote_case, yPlateau + y*cote_case,
                       xPlateau + (x+1)*cote_case, yPlateau + (y+1)*cote_case,
                       couleur='black', remplissage='grey', tag='tmpBoat')


def placer_boats(plateau, allBoats, nb):
    """
    Permet d'ajouter un bateau sur le plateau
    en cliquant sur la touche Entrée.
    Les coordonnées du bateau seront ajoutées dans la liste allBoats
    contenant toutes les autres positions des bateaux.
    Elles seront également codées par des 1 dans le plateau.

    :param plateau: list
    :param allBoats: list
    :param nb: int

    :return allBoats: list
    """
    tmpBoats = creer_boat(nb)  # creer le bateau à nb+1 case

    tourner = 1
    while True:
        fltk.efface('tmpBoat')
        fltk.efface('voisines')

        affiche_tmpBoat(tmpBoats)
        voisines(tmpBoats, plateau)
        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Touche':
            direction(tmpBoats, fltk.touche(ev))
            tmpBoats, tourner = rotation(tmpBoats, fltk.touche(ev), tourner)

            if fltk.touche(ev) == 'Return':
                if voisines(tmpBoats, plateau) is False:
                    # servira pour la fonction toucher_couler()
                    allBoats.append(tmpBoats)
                    coderby1(tmpBoats, plateau)

                    fltk.efface('tmpBoat')
                    return allBoats


def direction(tmpBoats, touche):
    """
    Permet de bouger les bateaux (à gauche, à droite, en bas, en haut)
    sur le plateau à l'aide des touches directionnelles du clavier.
    :param tmpBoats: list
    :param touche: string
    :return tmpBoats: list

    >>> direction([(0, 0), (0, 1), (0, 2)], "Right")
    [(1, 0), (1, 1), (1, 2)]
    >>> direction([(9, 6), (9, 7), (9, 8)], "Down")
    [(9, 7), (9, 8), (9, 9)]
    """
    if touche == 'Left':
        x0, y0 = tmpBoats[0]
        if x0 >= 1:
            for i in range(len(tmpBoats)):
                x, y = tmpBoats[i]
                tmpBoats[i] = x - 1, y

    elif touche == 'Right':
        x0, y0 = tmpBoats[-1]
        if x0 < nb_case - 1:
            for i in range(len(tmpBoats)):
                x, y = tmpBoats[i]
                tmpBoats[i] = x + 1, y

    elif touche == 'Down':
        x0, y0 = tmpBoats[-1]
        if y0 < nb_case - 1:
            for i in range(len(tmpBoats)):
                x, y = tmpBoats[i]
                tmpBoats[i] = x, y + 1

    elif touche == 'Up':
        x0, y0 = tmpBoats[0]
        if y0 >= 1:
            for i in range(len(tmpBoats)):
                x, y = tmpBoats[i]
                tmpBoats[i] = x, y - 1
    return tmpBoats


def rotation(tmpBoats, touche, tourner):
    """
    Permet de changer la rotation (horizontale ou verticale)
    du bateaux sur le plateau à l'aide de la touche r du clavier.
    :param tmpBoats: list
    :param touche: string
    :param tourner: int

    :return tmpBoats: list
    :return tourner: int

    >>> rotation([(0, 0),(1, 0),(2, 0)], "r", 1)
    ([(0, 0), (0, 1), (0, 2)], 0)
    >>> rotation([(0, 0),(0, 1),(0, 2)], "r", 0)
    ([(0, 0), (1, 0), (2, 0)], 1)
    >>> rotation([(0, 16), (1, 16), (2, 16), (3, 16)], "r", 1)
    ([(0, 16), (0, 17), (0, 18), (0, 19)], 0)
    """
    if touche == 'r':
        if tourner == 1:
            x0, y0 = tmpBoats[-1]
            if y0 + (len(tmpBoats) - 1) <= nb_case - 1:
                for i in range(len(tmpBoats)):
                    x, y = tmpBoats[0]
                    tmpBoats[i] = x, y + i
            tourner = 0

        elif tourner == 0:
            x0, y0 = tmpBoats[-1]
            if x0 + (len(tmpBoats) - 1) <= nb_case - 1:
                for i in range(len(tmpBoats)):
                    x, y = tmpBoats[0]
                    tmpBoats[i] = x + i, y
            tourner = 1
    return tmpBoats, tourner


def coderby1(boats, plateau):
    """
    Permet de coder les couples de coordonnées des bateaux
    par des 1 dans le plateau.
    :param boats: list
    :return plateau: list

    >>> plateau = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    >>> coderby1([(0, 0), (1, 0), (2, 0), (3, 0)], plateau)
    [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    """
    for coord in boats:
        x, y = coord
        plateau[y][x] = 1
    return plateau


def voisines(tmpBoats, plateau):
    """"
    Fonction permettant d'éviter que les bateaux se situent
    sur des cases voisines lors de la pose des bateaux.
    Pour cela, on regarde les cases adjacentes
    des cases du bateau et s'il y a un 1,
    cela veut dire qu'il y a forcément un bateau sur les cases voisines
    vu que chaque bateau déjà posé a été codé par un 1 dans le plateau.
    On return True dans ce cas, sinon False

    :param tmpBoats: list
    :param plateau: list
    :return sup: bool

    >>> voisines([(0, 1), (1, 1)], [[1, 1, 0], [0, 0, 0], [0, 0, 0]])
    True
    >>> voisines([(0, 1)], [[0, 0, 0], [0, 0, 1], [0, 0, 1]])
    False
    """
    vsn = False
    for coord in tmpBoats:
        x, y = coord
        if rien_envue(y, x, plateau) is True or plateau[y][x] == 1:
            fltk.rectangle(xPlateau + x*cote_case, yPlateau + y*cote_case,
                           xPlateau + (x+1)*cote_case,
                           yPlateau + (y+1)*cote_case,
                           remplissage='red', tag="voisines")
            vsn = True
    return vsn


# -------------------POSE AUTO BATEAUX------------------
def poseAuto_boats(cmptBoats):
    """
    Permet de poser automatiquement les bateaux sur le plateau.
    Pour chaque bateau, on choisit aléatoirement une position (x, y)
    à partir duquel il va être crée et une rotation r
    (0 pour horizontale et 1 pour verticale).
    On vérifie que chaque bateau peut être
    placé sur le plateau avant de les poser.

    :param cmptBoats: liste ou chaque élément représente le nombre de bateau
    à i+1 cases à poser (i représentant les indices de la liste)
    :return cmptBoats: list

    >>> poseAuto_boats([2, 1, 3])
    [0, 0, 0]
    """
    for i in range(len(cmptBoats)):
        for j in range(cmptBoats[i]):
            r = randint(0, 1)
            x, y = randint(0, nb_case - 1), randint(0, nb_case - 1)
            boat = creerAuto(x, y, r, i)
            while pose_valide(plateau, boat) is True:
                r = randint(0, 1)
                x, y = randint(0, nb_case - 1), randint(0, nb_case - 1)
                boat = creerAuto(x, y, r, i)
            # va etre utilisé dans la fonction toucher_couler()
            allBoats.append(boat)
            coderby1(boat, plateau)

        cmptBoats[i] = 0
    return cmptBoats


def pose_valide(plateau, boat):
    """
    Vérifie si un bateau peut etre posé sur le plateau.
    Pour que la pose soit valide, le bateau crée ne doit
    pas sortir de la grille et les cases voisines où va
    être placé le bateau doivent être différentes de 1
    (c'est à dire 0).
    Si la pose est valide, la fonction return False, sinon True

    :param plateau: list
    :param boat: list
    :return value: bool

    >>> pose_valide([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [(0, 3), (4, 0)])
    True
    >>> pose_valide([[1, 1, 0], [0, 0, 0], [0, 0, 0]], [(0, 1), (1, 1)])
    True
    >>> pose_valide([[0, 0, 0], [0, 0, 0], [1, 1, 0]], [(0, 0)])
    False
    """
    pos = False
    lst = indice_vers_coordonnees(plateau)
    for coord in boat:
        x, y = coord
        if (y, x) not in lst:
            pos = True

        elif (y, x) in lst:
            if rien_envue(y, x, plateau) is True:
                pos = True
    return pos


def creerAuto(x, y, r, nb):
    """
    Créer un bateau de nb+1 case à partir de la case (x, y)
    Si r = 0, le bateau sera à l'horizontal, sinon à la vertical.
    Si r = 0, (x, y) représente la case la plus à gauche.
    Si r = 1, (x, y) représente la case la plus en haut.

    :param x: int
    :param y: int
    :param r: int
    :param nb: int
    :return value: list

    >>> creerAuto(10, 10, 0, 2)
    [(10, 10), (11, 10), (12, 10)]
    >>> creerAuto(10, 10, 1, 1)
    [(10, 10), (10, 11)]
    """
    boat = []
    if r == 0:  # horizontale, donc y c'est le meme
        for i in range(nb + 1):
            boat.append((x + i, y))
    elif r == 1:  # verticale, donc x c'est le meme
        for i in range(nb + 1):
            boat.append((x, y + i))
    return boat


def affiche_boats(plateau):
    """
    Permet d'afficher les bateaux sur le plateaux
    avec des cases grises.
    """
    for y in range(len(plateau)):
        for x in range(len(plateau[y])):
            if plateau[y][x] == 1:
                fltk.rectangle(xPlateau + x*cote_case, yPlateau + y*cote_case,
                               xPlateau + (x+1)*cote_case,
                               yPlateau + (y+1)*cote_case, couleur='black',
                               remplissage='grey', tag='bateaux')


def tous_placer(cmptBoats):
    """
    Vérifie si la liste cmptBoats ne contient que des 0.
    Si c'est le cas, cela veut dire que tous les bateaux ont été posé
    on return alors True, sinon False.

    :param cmptBoats: liste ou chaque élément représente le nombre de bateau
    à i+1 cases à poser (i représentant les indices de la liste)
    :return value: bool

    >>> tous_placer([0, 0, 0, 0, 0, 0])
    True
    >>> tous_placer([0, 0, 0, 1, 1, 0])
    False
    """
    cmpt = 0
    for elem in cmptBoats:
        cmpt += elem
    if cmpt == 0:
        return True
    return False


# -------------------PARTIE TIR--------------------
def indice_vers_coordonnees(plateau):
    """Convertit les indices du tableau en couple de coordonnées (i, j)
    :param : list
    :return value: list

    >>> indice_vers_coordonnees([[0, 0], [0, 0]])
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    """
    lst = []
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            lst.append((i, j))
    return lst


def saisie_tir_clavier():
    """
    Permet de saisir les coordonnées de notre tir au clavier.
    :return value: int, int
    """
    y, x = int(input("Quel ligne ? ")), int(input("Quelle colonne ? "))
    while valideTir(y, x, plateau) is True:
        print('Impossible !')
        y, x = int(input("Quel ligne ? ")), int(input("Quelle colonne ? "))
    return y, x


def saisie_tir_souris():
    """
    Permet de tirer sur une case du plateau avec un clic gauche de la souris.
    les coordonées du pixel renvoyées avec le clic
    seront convertit en position de case (y, x)
    Si le tir est valide, on renvera (y, x)
    A l'aide de la touche tab la fonction affiche
    les bateaux du jouer adverse ou bot sur le plateaux.
    """
    tab = 1
    while True:
        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)
        fltk.mise_a_jour()

        if ty == 'ClicGauche':
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            xCase, yCase = (x - xPlateau) // cote_case, \
                           (y - yPlateau) // cote_case

            if valideTir(yCase, xCase, plateau) is False:
                fltk.efface('bateaux')
                return yCase, xCase

        if ty == 'Touche':
            if fltk.touche(ev) == "Tab":
                if tab == 1:
                    affiche_boats(plateau)
                    tab = 0
                elif tab == 0:
                    fltk.efface('bateaux')
                    tab = 1


def valideTir(y, x, plateau):
    """
    Vérifie si les coordonnées du Tir sont valide.
    Pour que le tir soit valide, il faut qu'elle soit sur une case du plateau
    et que la case n'a pas déjà été tiré
    Si le tir est valide, alors on return False, sinon True

    :param y: int
    :param x: int
    :return val: bool

    >>> valideTir(1, 1, [[0, 0, 0], [0, -1, 0], [0, 0, 0]])
    True
    """
    val = False
    lst = indice_vers_coordonnees(plateau)
    if (y, x) not in lst:
        val = True
    elif (y, x) in lst and plateau[y][x] == -1 or plateau[y][x] == -2:
        val = True
    return val


def analyseTir(y, x, plateau):
    """
    Permet de transformer la valeur de la case où l'on a tiré en -1
    dans la list plateau si le tir n'atteint pas de bateau
    et en -2 si le tir touche un bateau.
    Ça va permettre de distinguer visuellement les tirs réussis des tirs ratés.
    Si le tir touche un bateau alors on return True, sinon False

    :param y: int
    :param x: int
    :param plateau: list
    :return: bool

    >>> analyseTir(1, 1, [[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    True
    >>> analyseTir(1, 1, [[1, 1, 0], [0, 0, 0], [0, 0, 0]])
    False
    """
    # si on atteint pas de bateau
    if plateau[y][x] != 1:
        plateau[y][x] = -1
        return False

    # si on atteint un bateau
    elif plateau[y][x] == 1:
        plateau[y][x] = -2
        return True


def rien_envue(y, x, plateau):
    """
    Permet de savoir s'il y a ou non un bateau
    dans les cases adjacentes de la case où l'on a tiré.
    Si c'est le cas, on return True, sinon False

    :param y: int
    :param x: int
    :param plateau: list

    >>> rien_envue(1, 1, [[0, 0, 0], [0, 0, 0], [0, 1, 1]])
    True
    >>> rien_envue(0, 0, [[0, 0, 0], [0, 0, 0], [0, 1, 1]])
    False
    """
    lst = cases_adjacentes(y, x, nb_case)
    for elem in lst:
        y, x = elem
        if plateau[y][x] == 1:
            return True
    return False


def cases_adjacentes(y, x, nb_case):
    """
    Renvoie les coordonnées des cases adjacentes de la case (y, x)

    :param y: int
    :param x: int
    :param nb_case: int
    :return value : lst

    >>> cases_adjacentes(1, 2, 4)
    [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)]
    """
    lst = []
    for verY in range(y - 1, y + 2):
        for verX in range(x - 1, x + 2):
            if 0 <= verY < nb_case:
                if 0 <= verX < nb_case:
                    if verY == y and verX == x:
                        pass
                    else:
                        adjacentes = verY, verX
                        lst.append(adjacentes)
    return lst


def toucher_couler(y, x, allBoats):
    """
    Permet de savoir si on a touché ou coulé un bateau.
    Pour cela, on va utiliser la liste allBoats qui contient
    les emplacements (coordonnées de cases) de tous les bateaux posés.
    Chaque bateau étant représenté par une liste, on va regarder
    dans la liste allBoats dans quelle liste ce trouve la case (y, x)
    et on va la supprimer et si la liste concernée est vide alors
    cela veut forcément dire que le bateau a été coulé.
    Dans ce cas, on return True, sinon False

    :param y: int
    :param x: int
    :param allBoats : list
    :return value: bool

    >>> toucher_couler(0, 0, [[(0, 0)], [(0, 2), (1, 2)]])
    True
    >>> toucher_couler(0, 2, [[(0, 0)], [(0, 2), (1, 2)]])
    False
    """
    for boats in allBoats:
        if (x, y) in boats:
            boats.remove((x, y))
            # Ensuite on regarde si boat est vide.
            if boats == []:
                return True  # Si c'est le cas, alors le bateau est coulé
    return False  # si ce n'est pas le cas alors le bateau est touché


def affiche_tir(plateau):
    """
    Affiche les tirs sur le plateau sous forme
    de croix rouge pour les tirs réussis.
    Les tirs ratés sont affichés par des carrés bleu.
    """
    for y in range(len(plateau)):
        for x in range(len(plateau[y])):
            if plateau[y][x] == -2:  # tir réussi
                # dessin croix rouge X
                fltk.rectangle(xPlateau + x*cote_case, yPlateau + y*cote_case,
                               xPlateau + (x+1)*cote_case,
                               yPlateau + (y+1)*cote_case,
                               couleur='red', epaisseur=2, tag='tir')

                fltk.ligne(xPlateau + x*cote_case, yPlateau + y*cote_case,
                           xPlateau + (x+1)*cote_case,
                           yPlateau + (y+1)*cote_case,
                           couleur='red', epaisseur=2, tag='tir')  # \
                fltk.ligne(xPlateau + (x+1)*cote_case, yPlateau + y*cote_case,
                           xPlateau + x*cote_case, yPlateau + (y+1)*cote_case,
                           couleur='red', epaisseur=2, tag='tir')  # /

            elif plateau[y][x] == -1:  # tir raté
                # dessin carré bleu
                fltk.rectangle(xPlateau + x*cote_case, yPlateau + y*cote_case,
                               xPlateau + (x+1)*cote_case,
                               yPlateau + (y+1)*cote_case,
                               couleur='blue', remplissage='sky blue',
                               epaisseur=2, tag='tir')


def fin_jeu(plateau):
    """Pour gagner, il faut qu'il n'y ait plus de 1 dans le plateau.
    S'il n'y a plus de 1, cela veut dire qu'il n'y a plus de bateaux.
    si c'est le cas, True sera return, sinon False

    >>> fin_jeu([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
    True
    >>> fin_jeu([[1,1,0,0], [0,0,0,0], [1,1,0,0], [0,0,0,0]])
    False
    """
    fin = True
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == 1:
                fin = False
    return fin


# -----------------------MENU-------------------------
def menu(xFleche, yFleche):
    """
    Fonction qui gère l'interface du menu.
    Selon la position de la flèche, le joueur
    pourra choisir entre les 2 modes du jeu (J1 vs J2 ou J1 vs Bot)
    et Quitter.
    """
    pos_fleche = 0
    while True:
        fltk.efface('fleche')
        fltk.image(0, 0, "fondmenu.png", ancrage='nw')
        fltk.image(10, 320, 'choixmode.png', ancrage='nw')

        fltk.image(xFleche, yFleche, "fleche.png", tag='fleche')
        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Touche':
            if fltk.touche(ev) == "Up":
                if pos_fleche > 0:
                    yFleche -= 47
                    pos_fleche -= 1

            elif fltk.touche(ev) == "Down":
                if pos_fleche < 2:
                    yFleche += 47
                    pos_fleche += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                fltk.efface_tout()
                return pos_fleche


# ----------INITIALISATION DE L'ENSEMBLE DES BATEAUX----------
def initialisation_nb_boats(cmptBoats):
    """
    Permet de choisir l'ensemble des bateaux à poser à
    l'aide des flèches directionelles du clavier.
    La touche entrée renvoie cmptBoats qui est la liste
    ou chaque élément représente le nombre de bateau
    à i+1 cases à poser (i représentant les indices de la liste)

    :param cmptBoats: list
    :return value: list
    """
    xFle, yFle = 117, 167
    pos_fleche = 0
    while True:
        fltk.efface_tout()
        fltk.image(0, 0, "fondpseudo.png", ancrage='nw')
        fltk.texte(320, 100,
                   "Choisissez l'ensemble des bateaux à poser: ",
                   couleur='red', ancrage='center')
        affiche_choixBoats(cmptBoats, 125, 150)

        if 0 < cmptBoats[pos_fleche]:
            fltk.image(xFle, yFle, "fg.png", tag='flecheGauche')
        if cmptBoats[pos_fleche] < 6:
            fltk.image(xFle+33, yFle, "fd.png", tag='flecheDroite')

        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Touche':
            if fltk.touche(ev) == "Up":
                if pos_fleche > 0:
                    yFle -= 50
                    pos_fleche -= 1

            elif fltk.touche(ev) == "Down":
                if pos_fleche < 5:
                    yFle += 50
                    pos_fleche += 1

            elif fltk.touche(ev) == "Left":
                if cmptBoats[pos_fleche] > 0:
                    cmptBoats[pos_fleche] -= 1
            elif fltk.touche(ev) == "Right":
                if cmptBoats[pos_fleche] < 6:
                    cmptBoats[pos_fleche] += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                fltk.efface_tout()
                return cmptBoats


# -----------------------PSEUDO CHOIX-------------------------
def pseudo(J, xpos, ypos, tag):
    """Permet au Joueur de choisir un pseudo
    xpos et ypos permettent d'afficher le pseudo où l'on souhaite sur l'écran
    :param J: str
    :param xPos, Ypos: int
    :param tag: string
    :return value : str, nom du pseudo choisi par le Joueur
    """
    while True:
        fltk.efface(tag)

        fltk.texte(xpos, ypos, J, taille=23, couleur='white', tag=tag)
        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Touche':
            print(fltk.touche(ev))

        if ty == 'Touche':
            if fltk.touche(ev) in 'abcdefghijklmnopqrstuvwxyz\
                              ABCDEFGHIJKLMNOPQRSTUVWXYZ\
                              12345678901':
                J += fltk.touche(ev)

            if fltk.touche(ev) == 'BackSpace':
                newJ = list(J)
                if len(newJ) > 0:
                    newJ.pop(-1)
                    J = ''
                    for lettre in newJ:
                        J += lettre

            if fltk.touche(ev) == 'Return':
                if len(J) > 0:
                    return J


# -----------------------CHOIX NIVEAU DU BOT-------------------------
def choix_bot(xFleche, yFleche):
    """
    Choisis la difficulté de l'ordinateur à l'aide
    des touches Down et Up du clavier.
    2 difficultés possibles: EASY ou HARD

    :param xFleche: int
    :param yFleche: int
    :return pos_fleche: int
    """

    pos_fleche = 0
    while True:
        fltk.efface('fleche')
        fltk.texte(498, 350, "EASY", couleur='red', ancrage='nw')
        fltk.texte(498, 400, "HARD", couleur='red', ancrage='nw')

        fltk.image(xFleche, yFleche, "fleche.png", tag='fleche', ancrage='nw')
        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)

        if ty == 'Touche':
            if fltk.touche(ev) == "Up":
                if pos_fleche > 0:
                    yFleche -= 50
                    pos_fleche -= 1

            elif fltk.touche(ev) == "Down":
                if pos_fleche < 1:
                    yFleche += 50
                    pos_fleche += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                fltk.efface_tout()
                return pos_fleche


def change_joueur(plateau, allBoats, choix):
    """
    Permet de changer le plateau et la liste contenant
    l'emplacement des bateaux en fonction du mode de jeu choisis.
    Le choix 0 désigne des joueurs humain alors que 1
    un joueur humain et un Bot

    :param plateau: list
    :param allBoats: list
    :param choix: int
    :return plateau: list
    :return allBoats: list

    # >>> plateauJ1 = [[0, 0],[0, 0]]
    # >>> plateauJ2 = [[0, 0],[-1, 0]]
    # >>> allBoatsJ1 = [[(0, 0)]]
    # >>> allBoatsJ2 = [[(1, 1)]]
    # >>> change_joueur([[0, 0],[-1, 0]], [[(1, 1)]], 0)
    # [[0, 0],[0, 0]], [[(0, 0)]]
    """
    if plateau == plateauJ1 and allBoats == allBoatsJ1:
        if choix == 0:
            plateau = plateauJ2
            allBoats = allBoatsJ2
        elif choix == 1:
            plateau = plateauBot
            allBoats = allBoatsBot
    else:
        plateau = plateauJ1
        allBoats = allBoatsJ1
    return plateau, allBoats


def change_pseudo(pseudo, choix):
    """
    Change le pseudo utilisé lors des annonces graphiques.
    Le choix 0 désigne des joueurs humain alors que 1
    un joueur humain et un Bot
    :param pseudo: str
    :param choix: int, mode de jeu choisi avec la fonction menu()
    :return pseudo: str

    # >>> pseudoJ1 = "Hakim"
    # >>> pseudoJ2 = "Sylvain"
    # >>> change_pseudo("Hakim", 0)
    # "Sylvain"
    """
    if pseudo == pseudoJ1:
        if choix == 0:  # Joueur1 VS Joueur2
            pseudo = pseudoJ2
        elif choix == 1:  # Joueur1 VS Bot
            pseudo = pseudoBot
    else:
        pseudo = pseudoJ1
    return pseudo


# Initialisation
nb_case = 20
cote_case = 20
largeurEcran = 800
hauteurEcran = 500
fltk.cree_fenetre(largeurEcran, hauteurEcran)
xPlateau, yPlateau = 50, 50

# liste de liste représentant le plateau du JOUEUR1
plateauJ1 = init_plateau(nb_case)
# liste de liste contenant les emplacements de tous les bateaux du JOUEUR 1
allBoatsJ1 = []

# liste ou chaque élément représente le nombre de bateau à i+1 cases à poser
# (i représentant les indices de la liste)
cmptBoats = [6, 5, 4, 3, 2, 1]
choixMode = menu(305, 330)

if choixMode == 0:  # JOUEUR1 VS JOUEUR2
    fltk.image(0, 0, "fondpseudo.png", ancrage='nw')
    fltk.image(largeurEcran / 2, hauteurEcran / 2,
               'j1vsj2.png', ancrage='center')
    pseudoJ1 = pseudo('', 108, 350, 'J1')  # Speudo JOUEUR1
    pseudoJ2 = pseudo('', 498, 350, 'J2')
    fltk.efface_tout()

    cmptBoatsJ1 = initialisation_nb_boats(cmptBoats)

    plateauJ2 = init_plateau(nb_case)
    cmptBoatsJ2 = cmptBoatsJ1.copy()
    allBoatsJ2 = []


elif choixMode == 1:  # JOUEUR1 VS BOT
    fltk.image(0, 0, "fondpseudo.png", ancrage='nw')
    fltk.image(largeurEcran / 2, hauteurEcran / 2,
               'j1vsbot.png', ancrage='center')
    pseudoJ1 = pseudo('', 108, 350, 'J1')

    choixlevelBot = choix_bot(590, 350)
    if choixlevelBot == 0:
        pseudoBot = 'easyBot'
    else:
        pseudoBot = 'hardBot'
    fltk.efface_tout()

    cmptBoatsJ1 = initialisation_nb_boats(cmptBoats)

    plateauBot = init_plateau(nb_case)
    cmptBoatsBot = cmptBoatsJ1.copy()
    allBoatsBot = []

elif choixMode == 2:  # Quitter
    quit()


pseudo = pseudoJ1
plateau = plateauJ1
cmptBoats = cmptBoatsJ1
allBoats = allBoatsJ1


fltk.image(0, 0, "sunny.png", ancrage='nw')
draw_grille(plateau, 50, 50)


tour = 1
# PLACEMENT BATEAU
while True:
    fltk.texte(90, 8, str(pseudo) + " doit positionner ses bateaux",
               taille=15, couleur='red', tag='PseudoPose')
    # si c'est un bot alors on pose aléatoirement les bateaux
    if pseudo == 'easyBot' or pseudo == 'hardBot':
        poseAuto_boats(cmptBoats)

    else:  # si ce n'est pas un bot
        nb = choisir_boats(750, 70)
        if nb != -1:
            # on place sur le plateau le bateau a nb+1 case
            placer_boats(plateau, allBoats, nb)
            fltk.efface('bateaux')
            affiche_boats(plateau)
    fltk.mise_a_jour()

    if tous_placer(cmptBoats) is True:
        if pseudo == 'easyBot' or pseudo == 'hardBot':
            fltk.texte(largeurEcran/2, hauteurEcran/2,
                       "Le BOT a placé tous ses bateaux",
                       ancrage='center', couleur='red', tag='Tousplacer')
        else:
            fltk.texte(largeurEcran/2, hauteurEcran/2,
                       "Vous avez placé tous vos bateaux !",
                       ancrage='center', couleur='red', tag='Tousplacer')

        fltk.attente(3)
        fltk.efface('bateaux')
        fltk.efface('PseudoPose')
        fltk.efface('Tousplacer')
        tour += 1

        if tour == 3:
            break

        if choixMode == 0:
            cmptBoats = cmptBoatsJ2
        else:
            cmptBoats = cmptBoatsBot
        pseudo = change_pseudo(pseudo, choixMode)
        plateau, allBoats = change_joueur(plateau, allBoats, choixMode)


pseudo = change_pseudo(pseudo, choixMode)
# liste servant pour le Bot diffculté Hard
hard = indice_vers_coordonnees(plateau)
# TIRS
while True:
    fltk.texte(90, 8, "C'est au tour de " + str(pseudo) + " de tirer",
               taille=15, couleur='red', tag='Tirer')

    # si c'est un bot qui tire
    if pseudo == "easyBot":
        y, x = randint(0, nb_case - 1), randint(0, nb_case - 1)
        while valideTir(y, x, plateau) is True:
            y, x = randint(0, nb_case - 1), randint(0, nb_case - 1)

    elif pseudo == "hardBot":
        y, x = randint(0, nb_case - 1), randint(0, nb_case - 1)
        while (y, x) not in hard or plateau[y][x] == -1 or plateau[y][x] == -2:
            y, x = randint(0, nb_case - 1), randint(0, nb_case - 1)

    else:  # si ce n'est un pas un bot qui tire
        y, x = saisie_tir_souris()
    fltk.efface('tir')

    # si le joueur ou bot réussi son tir, il a le droit de retirer
    if analyseTir(y, x, plateau) is True:
        affiche_tir(plateau)

        if toucher_couler(y, x, allBoats) is False:
            fltk.texte(250, 475, "Touché", ancrage='center',
                       couleur='red', tag='Résultat')
            if pseudo == 'hardBot':
                hard = cases_adjacentes(y, x, nb_case)
        else:
            fltk.texte(250, 475, "Coulé", ancrage='center',
                       couleur='red', tag='Résultat')
            if pseudo == 'hardBot':
                hard = indice_vers_coordonnees(plateau)

        fltk.attente(2)
        fltk.efface('Résultat')

    # si le joueur ou bot rate son tire c'est à l'autre joueur ou bot de tirer
    else:
        affiche_tir(plateau)
        if rien_envue(y, x, plateau) is False:
            fltk.texte(250, 475, "Rien", ancrage='center',
                       couleur='red', tag='Résultat')
        else:
            fltk.texte(250, 475, "En vue", ancrage='center',
                       couleur='red', tag='Résultat')
            if pseudo == 'hardBot':
                hard = cases_adjacentes(y, x, nb_case)

        fltk.attente(2)
        fltk.efface('Résultat')
        fltk.efface('tir')
        fltk.efface('Tirer')

        pseudo = change_pseudo(pseudo, choixMode)
        plateau, allBoats = change_joueur(plateau, allBoats, choixMode)
        # on affiche le plateau avec les tirs de l'autre joueur ou Bot
        affiche_tir(plateau)
    fltk.mise_a_jour()

    if fin_jeu(plateau) is True:
        break


fltk.texte(largeurEcran/2, hauteurEcran/2, str(pseudo)+" a gagné !",
           couleur='red', ancrage='center')
fltk.attend_clic_gauche()
fltk.ferme_fenetre()
