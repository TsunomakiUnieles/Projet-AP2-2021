# Tache 1

def est_trace(etat, segment):
    if etat[segment] == 1:
        return True
    else:
        return False


def est_interdit(etat, segment):
    if etat[segment] == -1:
        return False
    else:
        return True


def est_vierge(etat, segment):
    if segment not in etat:
        return True
    else:
        return False


def tracer_segment(etat, segment):
    etat[segment] = 1


def interdire_segment(etat, segment):
    etat[segment] = -1


def effacer_segment(etat, segment):
    del etat[segment]


def segments_traces(etat, sommet):
    (a, b) = sommet
    liste_traces = []
    if ((a - 1, b), (a, b)) in etat and etat[((a - 1, b), (a, b))] == 1:
        liste_traces.append(((a - 1, b), (a, b)))
    if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == 1:
        liste_traces.append(((a, b), (a+1, b)))
    if ((a, b - 1), (a, b)) in etat and etat[((a, b - 1), (a, b))] == 1:
        liste_traces.append(((a, b-1), (a, b)))
    if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == 1:
        liste_traces.append(((a, b), (a, b + 1)))
    return liste_traces


def segments_interdits(etat, sommet):
    (a, b) = sommet
    liste_interdits = []
    if ((a - 1, b), (a, b)) in etat and etat[((a - 1, b), (a, b))] == -1:
        liste_interdits.append(((a - 1, b), (a, b)))
    if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == -1:
        liste_interdits.append(((a, b), (a + 1, b)))
    if ((a, b - 1), (a, b)) in etat and etat[((a, b - 1), (a, b))] == -1:
        liste_interdits.append(((a, b - 1), (a, b)))
    if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == -1:
        liste_interdits.append(((a, b), (a, b+1)))
    return liste_interdits


def segments_vierges(etat, sommet):
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
    (a, b) = case
    if indices[a][b] == None:
        return None
    else:
        count = 0
        if ((a, b), (a + 1, b)) in etat and etat[((a, b), (a + 1, b))] == 1:
            count += 1
        if ((a, b), (a, b + 1)) in etat and etat[((a, b), (a, b + 1))] == 1:
            count += 1
        if (((a + 1, b), (a + 1, b + 1)) in etat and
           etat[((a + 1, b), (a + 1, b + 1))] == 1):
            count += 1
        if (((a, b + 1), (a + 1, b + 1)) in etat and
           etat[((a, b + 1), (a + 1, b + 1))] == 1):
            count += 1
        if count == indices[a][b]:
            return 0
        elif count > indices[a][b]:
            return -1
        elif count < indices[a][b]:
            return 1

# Tache 2


def longueur_boucle(etat, segment):
    (x, y) = segment
    ((a, b), (c, d)) = (x, y)
    depart = (a, b)
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
                        courant = liste_trace[k][1]
                        boucle += 1
                        break
        return boucle
    else:
        return None


def status_slither(etat, indices):
    nb_segments = 0
    status_all_case = True
    for k in etat.keys():
        if etat[k] == 1:
            segment = k
            nb_segments += 1
    len_boucle = longueur_boucle(etat, segment)
    if len_boucle != nb_segments:
        if len_boucle == None:
            print('Pas de boucle !')
        else:
            print("Total de segments tracés non conforme au nombre \
                 de segments d'une boucle !")
    else:
        print("Boucle bien fermée sans segments non connectés !")
    print("Nombre total de segments tracés : " + str(nb_segments))
    print("Nombre de segments d'une boucle choisie au hasard : "
          + str(len_boucle))
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if statut_case(indices, etat, (i, j)) != 0:
                status_all_case = False
    print("Les indices sont-ils satisfaits : " + str(status_all_case))
