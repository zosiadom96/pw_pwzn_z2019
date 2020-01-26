"""
Na (1 pkt.):
Napisz program do sprawdzenia poprawności skompresowanego wyjścia poprzedniej
funkcji.
Funkcja MUSI w swej implementacji korzystać z wyrażeń regularnych.
Funkcja na wejściu przyjmuje nazwę pliku do sprawdzenia, na wyjściu zwraca
dwuelementową tuplę zawierającą liczbę poprawnych wierszy:
- na indeksie 0 płeć F
- na indeksie 1 płeć M
"""
import re
import csv


def check_animal_list(file_path):
    patternMALE = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_[M]_\d+\.\d{3}e[+-]\d+$'
    patternFEMALE = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_[F]_\d+\.\d{3}e[+-]\d+$'
    result = [0, 0]
    with open(file_path) as file:
        next(file, None)
        for row in file:
            if bool(re.match(patternFEMALE, row)):
                result[0] += 1
            elif bool(re.match(patternMALE, row)):
                result[1] += 1
    return tuple(result)


if __name__ == '__main__':
    assert check_animal_list('s_animals_sce.txt') == (2, 2)
    assert check_animal_list('animals_sc_corrupted.txt') == (5, 0)
