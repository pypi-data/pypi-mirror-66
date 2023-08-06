
__all__ = []

def est_triee(l):
    """ Vérifie si un liste est triée

    :param l: une liste de nombre

    :return: True si la liste est triée, False sinon

    :example:
    >>> est_triee([1, 2, 5, 6])
    True
    >>> est_triee([1, 2, 6, 5])
    False
    """
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]:
            return False
    return True

def tri_bulles(l):
    """ Trie la liste avec la méthode du tri à bulles

    :param l: Un tableau de nombre
    :return: une copie de la liste triée

    >> tri_bulles([1, 2, 6, 5])
    [1, 2, 5, 6]

    """
    tab = l[:]
    n = len(tab)
    for i in range(n):
        for j in range(n-i-1):
            if tab[j] > tab[j+1]:
                tab[j], tab[j+1] = tab[j+1], tab[j]
    return tab

def insert(elem, tab):
    if len(tab) == 0:
        return [elem]
    if tab[0] > elem:
        return [elem] + tab
    return [tab[0]] + insert(elem, tab[1:])

def tri_par_insertion(tab):
    ordered_tab = []
    for i in tab:
        ordered_tab = insert(i, ordered_tab)
    return ordered_tab

def extract_min(tab):
    vmin = tab[0]
    head = []
    stack = []
    for e in tab[1:]:
        if e < vmin:
            head.append(vmin)
            head += stack
            stack = []
            vmin = e
        else:
            stack.append(e)

    return (vmin, head + stack)

def tri_par_selection(tab):
    ordered = []
    to_order = tab[:]
    while len(to_order):
        vmin, to_order = extract_min(to_order)
        ordered.append(vmin)
    return ordered

def fusion(tab1, tab2):
    """ Fusion 2 ordered tab """
    i = 0
    j = 0
    l_tab1 = len(tab1)
    l_tab2 = len(tab2)
    fusionned = []

    while i < l_tab1 and j < l_tab2:
        if tab1[i] < tab2[j]:
            fusionned.append(tab1[i])
            i += 1
        else:
            fusionned.append(tab2[j])
            j += 1

    if i == len(tab1):
        fusionned += tab2[j:]
    if i == len(tab2):
        fusionned += tab1[i:]
    return fusionned

def triFusion(tab):
    if len(tab) == 1:
        return tab
    middle = len(tab) // 2
    return fusion(triFusion(tab[middle:]), triFusion(tab[:middle]))

def triRapide(tab):
    if len(tab) <= 1:
        return tab
    pivot = tab[-1]
    bigger = []
    smaller = []
    for i in tab[:-1]:
        if i > pivot:
            bigger.append(i)
        else:
            smaller.append(i)
    return triRapide(smaller) + [pivot] + triRapide(bigger)

def triComptage(L):
    vmin = min(L)
    vmax = max(L)
    hist = [0 for _ in range(vmin, vmax+1)]
    for l in L:
        hist[l-vmin] += 1

    ans = []
    for i, v in enumerate(hist):
        ans += [i]*v
    return ans
