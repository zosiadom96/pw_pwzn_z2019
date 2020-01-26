
"""
Częśćć 1 (1 pkt): Uzupełnij klasę Vector tak by reprezentowała wielowymiarowy wektor.
Klasa posiada przeładowane operatory równości, dodawania, odejmowania,
mnożenia (przez liczbę i skalarnego), długości
oraz nieedytowalny (własność) wymiar.
Wszystkie operacje sprawdzają wymiar.
Część 2 (1 pkt): Klasa ma statyczną metodę wylicznia wektora z dwóch punktów
oraz metodę fabryki korzystającą z metody statycznej tworzącej nowy wektor
z dwóch punktów.
Wszystkie metody sprawdzają wymiar.
"""
from math import sqrt

class Vector:

    _dim = None  # Wymiar vectora
    def __init__(self, *args):
        self.vec = tuple(args)
        self._dim = len(args)
        #print("aaaaaa kotki 2")

    @property
    def dim(self):
        return self._dim

    @property
    def len(self):
        leng = sum(dimension*dimension for dimension in self.vec)
        leng = sqrt(leng)
        return leng

    @staticmethod
    def calculate_vector(beg, end):
        """
        Calculate vector from given points
        :param beg: Begging point
        :type beg: list, tuple
        :param end: End point
        :type end: list, tuple
        :return: Calculated vector
        :rtype: tuple
        """
        new_vec = tuple(dos-uno for uno, dos in zip(beg, end))
        return new_vec

    @classmethod
    def from_points(cls, beg, end):
        """"""
        """
        Generate vector from given points.
        :param beg: Begging point
        :type beg: list, tuple
        :param end: End point
        :type end: list, tuple
        :return: New vector
        :rtype: tuple
        """
        if len(beg)==len(end):
            brand_new_vec = cls.calculate_vector(beg, end)
            return cls(*brand_new_vec)
        else:
            raise ValueError("Wrong Dimensions!")

    def __len__(self):
        return len(self.vec)

    def __add__(self, other):
        if isinstance(other,self.__class__):
            if other._dim == self._dim:
                result = [o+s for o,s in zip(other.vec,self.vec)]
                return Vector(*result)
            else:
                raise ValueError("Wrong Dimensions!")
        else:
            raise NotImplemented

    def __sub__(self, other):
        if isinstance(other,self.__class__):
            if other._dim == self._dim:
                result = [o-s for o,s in zip(other.vec,self.vec)]
                return Vector(*result)
            else:
                raise ValueError("Wrong Dimensions!")
        else:
            raise NotImplemented

    def __mul__(self, other):
        if isinstance(other,self.__class__):
            if other._dim == self._dim:
                result = sum(o*s for o,s in zip(other.vec,self.vec))
                return result
            else:
                raise ValueError("Wrong Dimensions!")
        if isinstance(other,int):
            result = [other*s for s in self.vec]
            return Vector(*result)
        else:
            raise NotImplemented

    def __eq__(self, other):
        if isinstance(other,self.__class__):
            return other.vec == self.vec
        else:
            raise NotImplemented


if __name__ == '__main__':
    v1 = Vector(1,2,3)
    v2 = Vector(1,2,3)
    assert v1 + v2 == Vector(2,4,6)
    assert v1 - v2 == Vector(0,0,0)
    assert v1 * 2 == Vector(2,4,6)
    assert v1 * v2 == 14
    assert len(Vector(3,4)) == 2
    assert Vector(3,4).dim == 2
    assert Vector(3,4).len == 5.
    assert Vector.calculate_vector([0, 0, 0], [1,2,3]) == (1,2,3)
    assert Vector.from_points([0, 0, 0], [1,2,3]) == Vector(1,2,3)
