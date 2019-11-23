"""
Jesteś informatykiem w firmie Noe's Animals Redistribution Center.
Firma ta zajmuje się międzykontynentalnym przewozem zwierząt.
---------
Celem zadania jest przygotowanie funkcji pozwalającej na przetworzenie
pliku wejściowego zawierającego listę zwierząt do trasnportu.
Funkcja ma na celu wybranie par (samiec i samica) z każdego gatunku,
tak by łączny ładunek był jak najlżeszy (najmniejsza masa osobnika
rozpatrywana jest względem gatunku i płci).
---------
Na 1 pkt.
Funkcja ma tworzyć plik wyjściowy zwierający listę wybranych zwierząt
w formacie wejścia (takim samym jak w pliku wejściowym).
Wyjście ma być posortowane alfabetycznie względem gatunku,
a następnie względem nazwy zwierzęcia.
---------
Na +1 pkt.
Funkcja ma opcję zmiany formatu wejścia na:
"<id>_<gender>_<mass>"
(paramter "compressed") gdzie:
- "id" jest kodem zwierzęcia (uuid),
- "gender" to jedna litera (F/M)
- "mass" zapisana jest w kilogramach w notacji wykładniczej
z dokładnością do trzech miejsc po przecinku np. osobnik ważący 456 gramów
ma mieć masę zapisaną w postaci "4.560e-01"
---------
Na +1 pkt.
* Ilość pamięci zajmowanej przez program musi być stałą względem
liczby zwierząt.
* Ilość pamięci może rosnąć liniowo z ilością gatunków.
---------
UWAGA: Możliwe jest wykonanie tylko jednej opcji +1 pkt.
Otrzymuje się wtedy 2 pkt.
UWAGA 2: Wszystkie jednoski masy występują w przykładzie.
"""
from pathlib import Path
import pandas as pd


def change_weight(weight):
    si_dict = {'kg': 1, 'g': 0.001, 'Mg': 1000, 'mg': 0.000001}
    value, si = weight.split()
    new_weight = si_dict[si] * float(value)
    return new_weight


def select_animals(input_path, output_path, compressed=False):
    animals = pd.read_csv(input_path)
    animals['unified_weight'] = animals['mass'].map(change_weight)
    animals = animals.sort_values(by='unified_weight')
    group = animals.groupby(by='genus')
    smallest_animals = []
    for genu, val in group:
        smallest_animals.append(val[val['gender'] == 'male'].iloc[0])
        smallest_animals.append(val[val['gender'] == 'female'].iloc[0])
    smallest_animals = pd.DataFrame(smallest_animals)
    smallest_animals = smallest_animals.sort_values(by=['genus', 'name'])

    if compressed:
        smallest_animals = smallest_animals.rename(columns={'id': 'uuid'})
        for i, anim in enumerate(smallest_animals['gender']):
            if anim == 'female':
                smallest_animals['gender'].iat[i] = 'F'
            else:
                smallest_animals['gender'].iat[i] = 'M'
        for i, mass in enumerate(smallest_animals['mass']):
            value = change_weight(mass)
            value_f = '%.3e' % float(value)
            smallest_animals['mass'].iat[i] = value_f
        smallest_animals.to_csv(output_path, index=False, sep='_', columns=['uuid', 'gender', 'mass'])
    else:
        smallest_animals.to_csv(output_path, index=False, columns=['id', 'mass',
                                                               'genus', 'name', 'gender'])


if __name__ == '__main__':
    input_path = Path('s_animals.txt')
    output_path = Path('s_animals_s.txt')
    select_animals(input_path, output_path)
    with open(output_path) as generated:
        with open('s_animals_se.txt') as expected:
            assert generated.read() == expected.read()

    output_path = Path('s_animals_sc.txt')
    select_animals(input_path, output_path, True)
    with open(output_path) as generated:
        with open('s_animals_sce.txt') as expected:
            assert generated.read() == expected.read()


