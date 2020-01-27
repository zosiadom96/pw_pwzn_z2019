import math
import itertools
from collections import Counter
import os
import pandas as pd
from collections import defaultdict


directory=input("Enter input file name")
directory2=input("Enter output file name")
d=defaultdict()


def read_data(directory):


    if not os.path.isfile(directory):
        raise ValueError("No file")
    
    x=pd.read_csv(directory,sep=";", header=None)    
    for i in x.values:
        d[i[0]] = i[1]
    return d

#mandaty_partii = Counter({'a':49, 'b':37, 'c':38, 'd':34, 'e':15, 'f':12, 'g':9, 'h':5, 'i':1})

def zsumuj_glosy_koalicji(mandaty_partii, czlonkowie_koalicji):
    return sum(mandaty_partii[partia] for partia in czlonkowie_koalicji)


def przelicz_jednostke(mandaty_partii):
    # suma wszystkich mandatow
    mandaty = sum(mandaty_partii.values())

    # ile wyniesie wiekszosc
    wiekszosc = math.floor(mandaty * 0.5) + 1

    # tworzymy listę partii
    partie = list(mandaty_partii.keys())

    # zlicza ile mamy partii
    ilosc_partii = len(partie)

    # deklaracja (na razie puste zmienne)
    #liczba koalicji wygranych, w ktorych bierze udzial dana part
    w_koalicje_partii = Counter()
    b_p_index = Counter()

    # koalicja [True, False, True] oznacza, ze pierwsza i trzecia partia naleza do koalicji (glosuja na tak)
    koalicje = itertools.product([True, False], repeat=ilosc_partii)

    # ilosc mozliwych koalicji
    n_koalicji = 2 ** (ilosc_partii - 1)

    #wygrywajace koalicje
    w_koalicje = 0
    for koalicja in koalicje:
        czlonkowie_koalicji = [partia for partia, czlonek in zip(partie, koalicja) if czlonek]
        n_glosow = zsumuj_glosy_koalicji(mandaty_partii, czlonkowie_koalicji)

        # koalicja nie jest w stanie osiagnac wiekszosci
        if n_glosow < wiekszosc:
            continue

        w_koalicje += 1
        for czlonek in czlonkowie_koalicji:
            w_koalicje_partii[czlonek] += 1

    # obliczamy c_i i indeks
    for partia in partie:
        c_partii = 2 * w_koalicje_partii[partia] - w_koalicje
        b_p_index[partia] = c_partii / n_koalicji

    
    return b_p_index

print("Banzhaf power index is a power index defined by the probability of changing an outcome of a vote where voting rights are not necessarily equally divided among \nthe voters or shareholders. To calculate the power of a voter using the Banzhaf index, list all the winning coalitions, then count the critical voters. A critical \nvoter is a voter who, if he changed his vote from yes to no, would cause the measure to fail. [Source: Wikipedia] \nCalculated values:",file=open(directory2,"w"))

read_data(directory)
mandaty_partii=Counter(d)
print(mandaty_partii)
przelicz_jednostke(mandaty_partii).keys()
for key, value in przelicz_jednostke(mandaty_partii).items():
    print(key, value, file=open(directory2,"a"))

