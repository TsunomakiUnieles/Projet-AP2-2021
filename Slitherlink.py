# Projet Slitherlink AP2, BAKHTI Walid / NGUYEN Herve / TD-E

# Tache 1


from fltk import cercle, type_ev, abscisse, ordonnee, efface_tout
from fltk import image, texte, rectangle, cree_fenetre, ferme_fenetre
from fltk import attend_clic_gauche, mise_a_jour, ligne
from fltk import attend_ev
from pathlib import Path

import doctest

doctest.testmod()


def est_trace(etat, segment):
    """
    Vérifie si le segment est tracé, renvoie True sinon False.
    :param: dict, tuple
    :return: bool

    >>> est_trace({((0, 1), (1, 1)) : -1}, ((0, 1),(1,1)))
    False
    >>> est_trace({((0, 1), (1, 1)) : 1}, ((0, 1),(1,1)))
    True
    """
    if etat[segment] == 1:
        return True
    else:
        return False


def est_interdit(etat, segment):
    """
    Vérifie si le segment est interdit, renvoie False sinon True.
    :param: dict, tuple
    :return: bool

    >>> est_interdit({((0, 1), (1, 1)) : -1}, ((0, 1),(1,1)))
    True
    >>> est_interdit({((0, 1), (1, 1)) : 1}, ((0, 1),(1,1)))
    False
    """
    if etat[segment] == -1:
        return True
    else:
        return False


def est_vierge(etat, segment):
    """
    Vérifie si le segment est vide dans le dict etat, renvoie True
    sinon False.
    :param: dict, tuple
    :return: bool

    >>> est_vierge({((0, 1), (1, 1)) : 1}, ((0, 1),(1,1)))
    False
    >>> est_vierge({}, ((0, 1),(1,1)))
    True
    """
    if segment not in etat:
        return True
    else:
        return False


def tracer_segment(etat, segment):
    """
    Permet de tracer un segment
    :param: dict, tuple
    :return: None
    """
    etat[segment] = 1


def interdire_segment(etat, segment):
    """
    Permet d'interdit un segment
    :param: dict, tuple
    :return: None
    """
    etat[segment] = -1


def effacer_segment(etat, segment):
    """
    Permet d'effacer un segment du dict etat.
    :param: dict, tuple
    :return: None
    """
    del etat[segment]


def segments_traces(etat, sommet):
    """
    Renvoie la liste des segments tracés adjacents au sommet.
    :param: dict, tuple
    :return: list

    >>> segments_traces({((0, 1), (1, 1)) : -1}, (0, 1))
    []
    >>> segments_traces({((0, 1), (1, 1)) : 1}, (0, 1))
    [((0, 1), (1, 1))]
    """
    (a, b) = sommet
    liste_traces = []
    if ((a - 1, b), (a, b)) in etat and etat[((a - 1, b), (a, b))] == 1:
        liste_traces.append(((a - 1, b), (a, b)))
    if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == 1:
        liste_traces.append(((a, b), (a + 1, b)))
    if ((a, b - 1), (a, b)) in etat and etat[((a, b - 1), (a, b))] == 1:
        liste_traces.append(((a, b - 1), (a, b)))
    if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == 1:
        liste_traces.append(((a, b), (a, b + 1)))
    return liste_traces


def segments_interdits(etat, sommet):
    """
    Renvoie la liste des segments interdits adjacents au sommet.
    :param: dict, tuple
    :teturn: list

    >>> segments_interdits({((2, 3), (2, 4)) : 1}, (2, 3))
    []
    >>> segments_interdits({((2, 3), (2, 4)) : -1}, (2, 3))
    [((2, 3), (2, 4))]
    """
    (a, b) = sommet
    liste_interdits = []
    if ((a - 1, b), (a, b)) in etat and etat[((a - 1, b), (a, b))] == -1:
        liste_interdits.append(((a - 1, b), (a, b)))
    if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == -1:
        liste_interdits.append(((a, b), (a + 1, b)))
    if ((a, b - 1), (a, b)) in etat and etat[((a, b - 1), (a, b))] == -1:
        liste_interdits.append(((a, b - 1), (a, b)))
    if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == -1:
        liste_interdits.append(((a, b), (a, b + 1)))
    return liste_interdits


def segments_vierges(etat, sommet):
    """
    Renvoie la liste des segments vierges adjacents au sommet.
    :param: dict, tuple
    :return: list

    >>> segments_vierges({((2, 3), (2, 4)) : -1}, (2, 3))
    [((1, 3), (2, 3)), ((2, 3), (3, 3)), ((2, 2), (2, 3))]
    >>> segments_vierges({}, (2, 3))
    [((1, 3), (2, 3)), ((2, 3), (3, 3)), ((2, 2), (2, 3)), ((2, 3), (2, 4))]
    """
    (a, b) = sommet
    liste_vierges = []
    if ((a - 1, b), (a, b)) not in etat:
        liste_vierges.append(((a - 1, b), (a, b)))
    if ((a, b), (a + 1, b)) not in etat:
        liste_vierges.append(((a, b), (a + 1, b)))
    if ((a, b - 1), (a, b)) not in etat:
        liste_vierges.append(((a, b - 1), (a, b)))
    if ((a, b), (a, b + 1)) not in etat:
        liste_vierges.append(((a, b), (a, b + 1)))
    return liste_vierges


def statut_case(indices, etat, case):
    """
    Vérifie si les segments tracés autour d'une case correspondent
    à l'indice de cette même case.
    Renvoie 0 si cette indice est respecté, 1 si il manque encore des
    segments et -1 si le nombre de segments est trop important.
    :param: list, dict, tuple
    :return: int or bool

    >>> statut_case([[2, 2],[2, 2]], {((0, 0), (0, 1)) : 1 ,((0, 1), (1, 1)) : 1 ,((1, 0), (1, 1)) : 1}, (0, 0))
    -1
    >>> statut_case([[2, 2],[2, 2]], {}, (1, 1))
    1
    >>> statut_case([[2, 2],[2, 2]], {((0, 0), (0, 1)) : 1 ,((0, 1), (1, 1)) : 1}, (0, 0))
    0
    """
    (a, b) = case
    if indices[a][b] == None:
        return None
    else:
        count = 0
        if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == 1:
            count += 1
        if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == 1:
            count += 1
        if ((a + 1, b), (a + 1, b + 1)) in etat and etat[
            ((a + 1, b), (a + 1, b + 1))
        ] == 1:
            count += 1
        if ((a, b + 1), (a + 1, b + 1)) in etat and etat[
            ((a, b + 1), (a + 1, b + 1))
        ] == 1:
            count += 1
        if count == indices[a][b]:
            return 0
        elif count > indices[a][b]:
            return -1
        elif count < indices[a][b]:
            return 1


def statut_case_spec(indices, etat, case):
    """
    Fonction variante de cette dernière, qui renvoie 1 pour les cases
    qui contiennent None. (Pour le solveur, qui malheureusment ne marche pas)
    :param: list, dict, tuple
    :return: int or bool
    """
    (a, b) = case
    if indices[a][b] == None:
        return 1
    else:
        count = 0
        if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == 1:
            count += 1
        if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == 1:
            count += 1
        if ((a + 1, b), (a + 1, b + 1)) in etat and etat[
            ((a + 1, b), (a + 1, b + 1))
        ] == 1:
            count += 1
        if ((a, b + 1), (a + 1, b + 1)) in etat and etat[
            ((a, b + 1), (a + 1, b + 1))
        ] == 1:
            count += 1
        if count == indices[a][b]:
            return 0
        elif count > indices[a][b]:
            return -1
        elif count < indices[a][b]:
            return 1


# Tache 2


def longueur_boucle(etat, segment):
    """Permets de savoir si le segment pris en paramètre fais parti
    d'une boucle, renvoie None si le segment n'est pas d'une boucle
    sinon renvoie la longeur de la boucle.
    :param: dict, tuple
    :return: int or bool

    >>> print(longueur_boucle({((0, 0), (0, 1)):1, ((0, 1), (1, 1)):1, ((1, 0),\
    (1, 1)):1, ((0, 0), (1, 0)):1}, ((0, 0), (0, 1))))
    4
    >>> print(longueur_boucle({((0, 0), (0, 1)):1, ((0, 1), (1, 1)):1, ((1, 0),\
    (1, 1)):1, ((0, 0), (1, 0)):1}, ((2, 3), (2, 4))))
    None
    >>> print(longueur_boucle({}, ((0, 0), (0, 1))))
    None
    """
    ((a, b), (c, d)) = segment
    depart = (a, b)
    last = (a, b)
    courant = (c, d)
    boucle = 0
    if segment in etat:
        while courant != depart:
            liste_trace = segments_traces(etat, courant)
            if len(liste_trace) != 2:
                boucle = None
                break
            else:
                for k in range(2):
                    if liste_trace[k][0] == courant:
                        if last != liste_trace[k][1]:
                            courant = liste_trace[k][1]
                            last = liste_trace[k][0]
                            boucle += 1
                            break
                    elif liste_trace[k][1] == courant:
                        if last != liste_trace[k][0]:
                            courant = liste_trace[k][0]
                            last = liste_trace[k][1]
                            boucle += 1
                            break
        if boucle == None:
            return None
        else:
            return boucle + 1
    else:
        return None


def status_slither(etat, indices):
    """Donne des informations sur la partie en cours, nombre de segment,
    si il y a des boucles, etc...
    :param: dict, list
    """
    segment = None
    nb_segments = 0
    status_all_case = True
    status_boucle_segment = False
    info_status_boucle = "Pas de boucle"
    if etat != {}:
        for k in etat.keys():
            if etat[k] == 1:
                segment = k
                nb_segments += 1
    if segment != None:
        len_boucle = longueur_boucle(etat, segment)
        if len_boucle != nb_segments:
            if len_boucle == None:
                print("Pas de boucle !")
            else:
                print(
                    "Total de segments tracés non conforme au nombre \
                    de segments d'une boucle !"
                )
                info_status_boucle = "Segments errant !"
        else:
            print("Boucle bien fermée sans segments non connectés !")
            status_boucle_segment = True
            info_status_boucle = "Boucle OK"
        print("Nombre total de segments tracés : " + str(nb_segments))
        print("Nombre de segments d'une boucle choisie au hasard : "
              + str(len_boucle))
        status_all_case = f_statut_all_case(indices, etat)
        print("Les indices sont-ils satisfaits : " + str(status_all_case))
    else:
        print("Aucun segments")
        status_all_case = False
    return (status_boucle_segment, status_all_case, info_status_boucle)


def f_statut_all_case(indices, etat):
    """
    Fonction vérifiant si toutes les cases ont leurs
    indice satisfait
    :param: list, dict
    :return: bool
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] != None:
                if statut_case(indices, etat, (i, j)) != 0:
                    return False
    return True


# Tache 3


def convert_indice(chaine):
    """Fonction permet de créer une liste de listes avec la grille de la
    chaine pour avoir un tableau d'indices.
    :param: str
    :return: list

    >>> convert_indice("3_0__\n230__\n10_3_\n")
    [[3, None, 0, None, None], [2, 3, 0, None, None], [1, 0, None, 3, None]]
    >>> convert_indice("3_0__\n230__\n10_3_\n_____\n")
    [[3, None, 0, None, None], [2, 3, 0, None, None], [1, 0, None, 3, None], [None, None, None, None, None]]
    >>> convert_indice("11\n21\n")
    [[1, 1], [2, 1]]
    """

    indice = []
    line = []
    for i in range(len(chaine)):
        if chaine[i] == "_":
            line.append(None)
        elif (
            chaine[i] == "1" or
            chaine[i] == "2" or
            chaine[i] == "3" or
            chaine[i] == "0"
        ):
            line.append(int(chaine[i]))
        elif chaine[i] == "\n":
            indice.append(line)
            line = []
    return indice


def verifie(chaine):
    """
    Cette fonction vérifie si la grille est de syntaxe correcte elle renvoie
    True sinon False.
    :param: str
    :return: bool

    >>> verifie("3_0__ \n 230__ \n 10_3_ \n 23_31 \n 3_2 \n")
    False
    >>> verifie("3_0__\n230__\n10_3_\n23_31")
    False
    >>> verifie("3_0__\n230__\n10_3_\n23531\n")
    False
    >>> verifie("3_0__\n230__\n10_3_\n23_31\n3_2\n")
    False
    >>> verifie("3_0__\n230__\n10_3_\n23_31\n")
    True
    """
    line = 0
    cmp = 0
    nb_cmp_init = 0
    for i in range(len(chaine)):
        if (
            chaine[i] == "_"
            or chaine[i] == "0"
            or chaine[i] == "1"
            or chaine[i] == "2"
            or chaine[i] == "3"
        ):
            cmp += 1
        if chaine[i] == "\n":
            line += 1
            if nb_cmp_init == 0:
                if cmp == 0:
                    return False
                else:
                    nb_cmp_init = cmp
            else:
                if nb_cmp_init != cmp:
                    return False
            cmp = 0
    if chaine[len(chaine) - 1] != "\n":
        return False
    return True


def menu():
    """
    Fonction qui affiche le menu et gère le fonctionnement
    du menu selon les clics de l'utilisateur.
    :return: None
    """
    cree_fenetre(600, 600)
    texte(
        300,
        60,
        "Slitherlink",
        couleur="aquamarine",
        police="verdana",
        ancrage="center",
        taille=40,
    )
    rectangle(
        180,
        150,
        420,
        250,
        couleur="MediumPurple2",
        remplissage="MediumPurple2",
        epaisseur=2,
    )
    texte(220, 180, "Jouer", police="calibri", couleur="white")
    rectangle(
        180,
        301,
        420,
        401,
        couleur="MediumPurple2",
        remplissage="MediumPurple2",
        epaisseur=2,
    )
    texte(220, 331, "Crédits", police="calibri", couleur="white")
    rectangle(
        180,
        450,
        420,
        550,
        couleur="MediumPurple2",
        remplissage="MediumPurple2",
        epaisseur=2,
    )
    texte(220, 480, "Quitter", police="calibri", couleur="white")
    credit = False

    while True:
        ev = attend_ev()
        tev = type_ev(ev)

        # Action dépendant du type d'évènement reçu :
        if tev == "ClicGauche":
            abs, ord = abscisse(ev), ordonnee(ev)

            # Lancement du jeu
            if (((180 <= abs <= 420) and (150 <= ord <= 250))) \
               and credit is False:
                break

            # Aller au crédits
            if (((180 <= abs <= 420) and (301 <= ord <= 401))) \
               and credit is False:
                efface_tout()
                credit = True
                texte(
                    300,
                    80,
                    "Slitherlink",
                    ancrage="center",
                    couleur="aquamarine",
                    taille=40,
                    police="verdana",
                )
                texte(
                    300,
                    320,
                    "BAKHTI Walid - NGUYEN Hervé",
                    ancrage="center",
                    couleur="black",
                    taille=15,
                    police="calibri",
                )
                texte(
                    300,
                    350,
                    "L1 M-I / Projet AP2",
                    ancrage="center",
                    couleur="black",
                    taille=15,
                    police="calibri",
                )
                texte(
                    300,
                    380,
                    "Université Gustave Eiffel, 2021",
                    ancrage="center",
                    couleur="black",
                    taille=15,
                    police="calibri",
                )
                rectangle(
                    410,
                    505,
                    550,
                    555,
                    remplissage="MediumPurple2",
                    epaisseur=2,
                    couleur="MediumPurple2",
                )
                texte(420, 510, "Retour", police="calibri", couleur="white")

            # Retourner au menu principal depuis les crédits
            if ((410 <= abs <= 550) and (505 <= ord <= 555)) \
               and credit is True:
                efface_tout()
                credit = False
                texte(
                    300,
                    60,
                    "Slitherlink",
                    couleur="aquamarine",
                    police="verdana",
                    ancrage="center",
                    taille=40,
                )
                rectangle(
                    180,
                    150,
                    420,
                    250,
                    couleur="MediumPurple2",
                    remplissage="MediumPurple2",
                    epaisseur=2,
                )
                texte(220, 180, "Jouer", police="calibri", couleur="white")
                rectangle(
                    180,
                    301,
                    420,
                    401,
                    couleur="MediumPurple2",
                    remplissage="MediumPurple2",
                    epaisseur=2,
                )
                texte(220, 331, "Crédits", police="calibri", couleur="white")
                rectangle(
                    180,
                    450,
                    420,
                    550,
                    couleur="MediumPurple2",
                    remplissage="MediumPurple2",
                    epaisseur=2,
                )
                texte(220, 480, "Quitter", police="calibri", couleur="white")

            if (((180 <= abs <= 420) and (450 <= ord <= 550))) \
               and credit is False:
                efface_tout()
                texte(
                    300,
                    150,
                    "Fermeture du jeu !",
                    ancrage="center",
                    couleur="MediumPurple2",
                    taille=30,
                    police="calibri",
                )
                texte(
                    300,
                    240,
                    "Faites un clic gauche pour quitter.",
                    ancrage="center",
                    couleur="MediumPurple2",
                    taille=20,
                    police="calibri",
                )
                attend_clic_gauche()
                ferme_fenetre()
                return
        if tev == "Quitte":
            break
        mise_a_jour()

    ferme_fenetre()

    if __name__ == "__main__" and (tev != "Quitte"):
        selection_screen()


def selection_screen():
    """
    Fonction qui affiche un menu de selection, permettant
    de sélectionner soit 3 grilles prédéfinies ou une grille
    à importer. Cette grille à importer doit être dans le
    le répertoire du jeu, et devra être nommé "grille.txt".
    :return: None
    """
    cree_fenetre(600, 600)
    texte(
        300,
        50,
        "Slitherlink",
        couleur="MediumPurple2",
        ancrage="center",
        taille=30,
        police="verdanda",
    )
    rectangle(200, 100, 400, 200, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        300,
        150,
        "Facile",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )
    rectangle(200, 225, 400, 325, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        300,
        275,
        "Moyen",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )
    rectangle(200, 350, 400, 450, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        300,
        400,
        "Difficile",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )
    rectangle(200, 475, 400, 575, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        300,
        525,
        "Import",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )

    while True:
        ev = attend_ev()
        tev = type_ev(ev)

        if tev == "ClicGauche" or tev == "ClicDroit":
            cx, cy = abscisse(ev), ordonnee(ev)
            if (200 <= cx <= 400) and (100 <= cy <= 200):
                ferme_fenetre()
                chaine = Path("grille_easy.txt").read_text()
                indice = convert_indice(chaine)
                jeu(indice)
                break
            elif (200 <= cx <= 400) and (225 <= cy <= 325):
                ferme_fenetre()
                chaine = Path("grille_medium.txt").read_text()
                indice = convert_indice(chaine)
                jeu(indice)
                break
            elif (200 <= cx <= 400) and (350 <= cy <= 450):
                ferme_fenetre()
                chaine = Path("grille_hard.txt").read_text()
                indice = convert_indice(chaine)
                jeu(indice)
                break
            elif (200 <= cx <= 400) and (475 <= cy <= 575):
                ferme_fenetre()
                chaine = Path("grille.txt").read_text()
                valide = verifie(chaine)

                if valide is False:
                    print("Fichier non valide !")
                    break

                elif valide is True:
                    indice = convert_indice(chaine)
                    jeu(indice)
                    break


def affiche_points(len_indice, len_sous_indice, taille_case):
    """Fonction permet d'affichage de tous les points pendant la partie
    en parcourant la liste des indices et la longueur de chaque
    sous-liste et en dessinant un cercle noir à l'emplacement voulu.
    :param: int, int, int
    :return: None
    """
    for i in range(len_indice + 1):
        for k in range(len_sous_indice + 1):
            cercle(15 + k * taille_case, 15 + i *
                   taille_case, 2, remplissage="black")


def affiche_segments(etat, taille_case):
    """
    Cette fonction permet d'affichage des segments.
    En parcourant les états de chaque segment, on
    trace soit un segment soit une croix à son emplacement.
    :param: dict, int
    :return: None
    """

    if etat != {}:
        lst_etat = list(etat)

        for k in lst_etat:
            if etat[k] == 1:
                ((a, b), (c, d)) = k
                ligne(
                    b * taille_case + 15,
                    a * taille_case + 15,
                    d * taille_case + 15,
                    c * taille_case + 15,
                    couleur="gray17",
                    epaisseur=2,
                )

            else:
                ((a, b), (c, d)) = k
                (x, y) = (
                    ((b * taille_case + d * taille_case) / 2) + 15,
                    ((a * taille_case + c * taille_case) / 2) + 15,
                )
                image(x, y, "cross.gif", ancrage="center")


def type_clic(cx, cy, len_indice, len_sous_indice, t_case, t_marge):
    """
    Fonction qui renvoie tuple qui qualifie la nature de l'action du clic de
    l'utilisateur, que cela soit un clic sur segment ou sur un des boutons de
    jeu.
    :param: int, int, int, int, int, int
    :return: tuple
    """
    for x in range(len_sous_indice):
        for y in range(len_indice):
            if x == 0 and y == 0:
                if (15 + t_marge <= cx <= 15 + t_case - t_marge) and (
                    15 - t_marge <= cy <= 15 + t_marge
                ):
                    return ("segment", ((0, 0), (0, 1)))
                if (15 - t_marge <= cx <= 15 + t_marge) and (
                    15 + t_marge <= cy <= 15 + t_case - t_marge
                ):
                    return ("segment", ((0, 0), (1, 0)))
            elif x == 0:
                if (15 - t_marge <= cx <= 15 + t_marge) and (
                    15 + t_case * y + t_marge <= cy <= 15 +
                        (y + 1) * t_case - t_marge
                ):
                    return ("segment", ((y, 0), (y + 1, 0)))
            elif y == 0:
                if (
                    15 + t_case * x + t_marge <= cx <= 15 +
                        (x + 1) * t_case - t_marge
                ) and (15 - t_marge <= cy <= 15 + t_marge):
                    return ("segment", ((0, x), (0, x + 1)))
            if (
                15 + t_case * x + t_marge <= cx <= 15 +
                    (x + 1) * t_case - t_marge
            ) and (
                15 + t_case * (y + 1) - t_marge <= cy <= 15 +
                t_case * (y + 1) + t_marge
            ):
                return ("segment", ((y + 1, x), (y + 1, x + 1)))
            if (
                15 + t_case * (x + 1) - t_marge <= cx <= 15 +
                t_case * (x + 1) + t_marge
            ) and (
                15 + t_case * y + t_marge <= cy <= 15 + (y + 1) *
                t_case - t_marge
            ):
                return ("segment", ((y, x + 1), (y + 1, x + 1)))
    if (800 <= cx <= 950) and (700 <= cy <= 750):
        return ("quitter", None)
    if (800 <= cx <= 950) and (600 <= cy <= 650):
        return ("reset", None)
    if (800 <= cx <= 950) and (500 <= cy <= 550):
        return ("main_menu", None)
    if (800 <= cx <= 950) and (400 <= cy <= 450):
        return ("solve", None)
    return (None, None)


def affiche_indice(indices, len_indice, len_sous_indice, etat, t_case):
    """
    Cette fonction permet d'affiche les indices de chaque case durant la
    partie.
    :param: list, int, int, dict, int
    :return: None
    """
    for x in range(len_indice):
        for y in range(len_sous_indice):
            status = statut_case(indices, etat, (x, y))
            if status == -1 or status == 0 or status == 1:
                if status == -1:
                    texte(
                        15 + (y + 0.5) * t_case,
                        15 + (x + 0.5) * t_case,
                        str(indices[x][y]),
                        couleur="red",
                        taille=int(t_case / 3),
                        ancrage="center",
                    )
                elif status == 1:
                    texte(
                        15 + (y + 0.5) * t_case,
                        15 + (x + 0.5) * t_case,
                        str(indices[x][y]),
                        couleur="black",
                        taille=int(t_case / 3),
                        ancrage="center",
                    )
                elif status == 0:
                    texte(
                        15 + (y + 0.5) * t_case,
                        15 + (x + 0.5) * t_case,
                        str(indices[x][y]),
                        couleur="blue",
                        taille=int(t_case / 3),
                        ancrage="center",
                    )


def affiche_ui():
    """
    Fonction qui permette l'affichage pendant la partie les boutons
    permettant de quitter, réinitialiser, retourner vers le menu principal,
    lancer le solveur. (Le solveur ne marche pas.)
    :return: None
    """
    texte(
        875,
        25,
        "Slitherlink",
        couleur="MediumPurple2",
        ancrage="center",
        taille=30,
        police="verdanda",
    )
    rectangle(800, 700, 950, 750, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        875,
        725,
        "Quit",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )
    rectangle(800, 600, 950, 650, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        875,
        625,
        "Reset",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )
    rectangle(800, 500, 950, 550, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        875,
        525,
        "Main Menu",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )
    rectangle(800, 400, 950, 450, remplissage="MediumPurple2",
              couleur="MediumPurple2")
    texte(
        875,
        425,
        "Solve",
        couleur="white",
        ancrage="center",
        taille=20,
        police="verdanda",
    )


def affiche_status(st_boucle, st_indices, info_boucle):
    """
    Fonction qui affiche durant la partie, la situation de la partie.
    :param: bool, bool, str
    :return: None
    """
    texte(
        875,
        125,
        "Statut de jeu :",
        couleur="deep sky blue",
        ancrage="center",
        taille=25,
        police="verdanda",
    )
    if st_boucle is True:
        texte(
            875,
            175,
            "Boucle OK",
            couleur="MediumPurple2",
            ancrage="center",
            taille=20,
            police="verdanda",
        )
    else:
        texte(
            875,
            175,
            info_boucle,
            couleur="MediumPurple2",
            ancrage="center",
            taille=20,
            police="verdanda",
        )
    if st_indices is True:
        texte(
            875,
            225,
            "Indices satisfaits",
            couleur="MediumPurple2",
            ancrage="center",
            taille=20,
            police="verdanda",
        )
    else:
        texte(
            875,
            225,
            "Indices non satisfaits",
            couleur="MediumPurple2",
            ancrage="center",
            taille=20,
            police="verdanda",
        )


def jeu(indices):
    """
    Cette fonction se charge de l'affichage et du déroulement
    du jeu, elle vérifie les conditions de victoires et se charge
    également du comportement du jeu selon les actions de l'utilisateur
    :param: list
    :return: None
    """
    cree_fenetre(1030, 780)
    etat = {}
    len_indice = len(indices)
    len_sous_indice = len(indices[0])
    taille_case = int(700 / (max(len_indice, len_sous_indice)))
    taille_marge = int(taille_case / 5)
    st_solveur = False

    while True:

        efface_tout()
        affiche_points(len_indice, len_sous_indice, taille_case)
        affiche_segments(etat, taille_case)
        affiche_indice(indices, len_indice, len_sous_indice, etat, taille_case)
        affiche_ui()
        (st_boucle, st_indices, info_boucle) = status_slither(etat, indices)
        affiche_status(st_boucle, st_indices, info_boucle)

        if st_indices and st_boucle and st_solveur is False:
            texte(
                875,
                300,
                "Gagné !",
                couleur="RoyalBlue1",
                ancrage="center",
                taille=45,
                police="verdanda",
            )
            mise_a_jour()
            ev = attend_ev()
            ferme_fenetre()
            menu()
            break

        ev = attend_ev()
        tev = type_ev(ev)

        if tev == "ClicGauche" or tev == "ClicDroit":
            cx, cy = abscisse(ev), ordonnee(ev)
            nc = type_clic(
                cx, cy, len_indice, len_sous_indice, taille_case, taille_marge
            )

            if nc[0] == "segment" and st_solveur is False:
                if est_vierge(etat, nc[1]):
                    if tev == "ClicDroit":
                        interdire_segment(etat, nc[1])

                    elif tev == "ClicGauche":
                        tracer_segment(etat, nc[1])

                elif (
                    est_interdit(etat, nc[1]) is True or est_trace(
                        etat, nc[1]) is True
                ):
                    effacer_segment(etat, nc[1])

            elif nc[0] == "quitter":
                ferme_fenetre()
                break

            elif nc[0] == "reset":
                etat = {}
            elif nc[0] == "main_menu":
                ferme_fenetre()
                menu()
                break
            elif nc[0] == "solve":
                st_solveur = True
                solution = solveur(indices, len_indice, len_sous_indice)
                if solution != {}:
                    etat = solution
        mise_a_jour()


# Tache 4


def liste_sommet(indices, len_indice, len_sous_indice):
    """
    Fonction qui renvoie une liste de tous les sommets
    adjacents à une case à 3 d'indice.
    Dans le cas où il n'y a pas de case de 3, même démarche pour
    les cases de 2. Puis de 1.
    Sinon renvoie ['Grille triviale']
    :param: list, int, int
    :return: list
    """
    lst_sommet = []
    for y in range(len_indice):
        for x in range(len_sous_indice):
            if indices[y][x] == 3:
                if (y, x) not in lst_sommet:
                    lst_sommet.append((y, x))
                if (y + 1, x) not in lst_sommet:
                    lst_sommet.append((y + 1, x))
                if (y, x + 1) not in lst_sommet:
                    lst_sommet.append((y, x + 1))
                if (y + 1, x + 1) not in lst_sommet:
                    lst_sommet.append((y + 1, x + 1))
    if lst_sommet != []:
        return lst_sommet
    else:
        for y in range(len_indice):
            for x in range(len_sous_indice):
                if indices[y][x] == 2:
                    if (y, x) not in lst_sommet:
                        lst_sommet.append((y, x))
                    if (y + 1, x) not in lst_sommet:
                        lst_sommet.append((y + 1, x))
                    if (y, x + 1) not in lst_sommet:
                        lst_sommet.append((y, x + 1))
                    if (y + 1, x + 1) not in lst_sommet:
                        lst_sommet.append((y + 1, x + 1))
    if lst_sommet != []:
        return lst_sommet
    else:
        for y in range(len_indice):
            for x in range(len_sous_indice):
                if indices[y][x] == 1:
                    if (y, x) not in lst_sommet:
                        lst_sommet.append((y, x))
                    if (y + 1, x) not in lst_sommet:
                        lst_sommet.append((y + 1, x))
                    if (y, x + 1) not in lst_sommet:
                        lst_sommet.append((y, x + 1))
                    if (y + 1, x + 1) not in lst_sommet:
                        lst_sommet.append((y + 1, x + 1))
    if lst_sommet != []:
        return lst_sommet
    else:
        return ["Grille triviale"]


def statut_case_adjacent(indices, len_indice, len_sous_indice, etat, segment):
    """
    Fonction qui renvoie un booléen concernant le statut des cases adjacent
    au segment entré en paramètre.
    :param: list, int, int, dict, tuple
    :return: bool
    """
    ((a, b), (c, d)) = segment
    if c == a + 1:
        if (0 < b - 1) and (b <= len_sous_indice - 1):
            return statut_case_spec(indices, etat, (a, b - 1)) > 0 and (
                statut_case_spec(indices, etat, (a, b)) > 0
            )
        elif 0 < b - 1:
            return statut_case_spec(indices, etat, (a, b - 1)) > 0
        elif b <= len_sous_indice - 1:
            return statut_case_spec(indices, etat, (a, b)) > 0
    elif d == b + 1:
        if (0 < a - 1) and (a <= len_indice - 1):
            return (
                statut_case_spec(indices, etat, (a - 1, b)) > 0
                and (statut_case_spec(indices, etat, (a, b))) > 0
            )
        elif 0 < a - 1:
            return statut_case_spec(indices, etat, (a - 1, b)) > 0
        elif a <= len_indice - 1:
            return statut_case_spec(indices, etat, (a, b)) > 0


def solveur(indices, len_indice, len_sous_indice):
    """
    Fonction qui devrais renvoyer soit un dictionnaire vide
    ou un dictionnaire qui correspond à une solution d'un
    tableau slitherlink

    :param: list, int, int
    :return: dict
    """
    lst_sommet = liste_sommet(indices, len_indice, len_sous_indice)
    if lst_sommet != ["Grille triviale"]:
        for sommet in lst_sommet:
            (a, b) = sommet
            etat_start = {}
            if a < len_indice:
                etat_start[((a, b), (a + 1, b))] = 1
                result_algo = algo_solveur(
                    indices, len_indice, len_sous_indice, sommet, etat_start
                )
                if result_algo[0] is True:
                    return result_algo[1]
                etat_start = {}
            if b < len_sous_indice:
                etat_start[((a, b), (a, b + 1))] = 1
                result_algo = algo_solveur(
                    indices, len_indice, len_sous_indice, sommet, etat_start
                )
                if result_algo[0] is True:
                    return result_algo[1]
                etat_start = {}
            if 0 < a:
                etat_start[((a - 1, b), (a, b))] = 1
                result_algo = algo_solveur(
                    indices, len_indice, len_sous_indice, sommet, etat_start
                )
                if result_algo[0] is True:
                    return result_algo[1]
                etat_start = {}
            if 0 < b:
                etat_start[((a, b - 1), (a, b))] = 1
                result_algo = algo_solveur(
                    indices, len_indice, len_sous_indice, sommet, etat_start
                )
                if result_algo[0] is True:
                    return result_algo[1]
        return {}


def algo_solveur(indices, len_indice, len_sous_indice, sommet, etat):
    (a, b) = sommet
    etat_2 = etat
    seg_trace = len(segments_traces(etat, sommet))
    if seg_trace == 2:
        if f_statut_all_case(indices, etat) is True:
            return (True, etat)
        else:
            return (False, etat)
    else:
        if seg_trace > 2:
            return (False, etat)
        if seg_trace == 1:
            if a < len_indice:
                if ((a, b), (a + 1, b)) not in etat:
                    etat_2[((a, b), (a + 1, b))] = 1
                    branch_1 = algo_solveur(
                        indices, len_indice, len_sous_indice, (
                            a + 1, b), etat_2
                    )
                    if branch_1[0] is True:
                        return branch_1
                    etat_2 = etat
            if b < len_sous_indice:
                if ((a, b), (a, b + 1)) not in etat:
                    etat_2[((a, b), (a, b + 1))] = 1
                    branch_2 = algo_solveur(
                        indices, len_indice, len_sous_indice, (
                            a, b + 1), etat_2
                    )
                    if branch_2[0] is True:
                        return branch_2
                    etat_2 = etat
            if 0 < a:
                if ((a - 1, b), (a, b)) not in etat:
                    etat_2[((a - 1, b), (a, b))] = 1
                    branch_3 = algo_solveur(
                        indices, len_indice, len_sous_indice, (
                            a - 1, b), etat_2
                    )
                    if branch_3[0] is True:
                        return branch_3
                    etat_2 = etat
            if 0 < b:
                if ((a, b - 1), (a, b)) not in etat:
                    etat_2[((a, b - 1), (a, b))] = 1
                    branch_4 = algo_solveur(
                        indices, len_indice, len_sous_indice, (
                            a, b - 1), etat_2
                    )
                    if branch_4[0] is True:
                        return branch_4
    return (False, etat)


# Lancement du jeu

menu()
