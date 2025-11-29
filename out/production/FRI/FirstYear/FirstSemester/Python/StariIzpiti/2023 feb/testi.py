from collections import defaultdict

def prehodi(ovire):
    zacasno = []
    rez = []
    for y, x0, x1 in ovire:

        
        if (y, x0-1) in zacasno:
            rez.append((y, x0-1))
        if (y, x1+1) in zacasno:
            rez.append((y, x1+1))
        
        zacasno.append((y,x0-1))
        zacasno.append((y,x1+1))
        
    return set(rez)

def nadlezna_ovira(ovire, y, x, pot):
    prevozeno = defaultdict(int)
    for smer in pot:
        if smer == "^":
            y-=1
        elif smer == "v":
            y+=1
        elif smer == ">":
            x+=1
        elif smer == "<":
            x-=1
            
        for y_, x0_, x1_ in ovire:
            if y_ == y and x0_<= x <= x1_:
                prevozeno[(y_, x0_, x1_)] += 1

    if prevozeno:
        rez = max(prevozeno, key=prevozeno.get)
        return rez
    else:
        return None
    
    
def odstrani(ovire, stolpci):
    for stolpec in stolpci:
        for y, x0, x1 in ovire:
            if x0 <= stolpec <= x1:
                ovire.remove((y, x0, x1))


class Kolesar:
    
    def __init__(self, ovire, y, x):
        self.ovire = ovire
        self.y = y
        self.x = x
        self.stevec = 0
        
    def premik(self, smer):
        if smer == "^":
            self.y-=1
        elif smer == "v":
            self.y+=1
        elif smer == ">":
            self.x+=1
        elif smer == "<":
            self.x-=1
            
        for y, x0, x1 in self.ovire:
            if x0 <= self.x <= x1 and self.y == y:
                self.ovire.remove((y, x0, x1))
                self.stevec += 1
                
    def lokacija(self):
        return((self.y, self.x))
    
    def uspesnost(self):
        return self.stevec




import unittest
import random

ovire = [(1, 1, 1), (1, 3, 3),
         (2, 1, 4), (2, 6, 7), (2, 11, 12),
         (3, 9, 9),
         (5, 3, 5), (5, 7, 10),
         (7, 4, 5), (7, 11, 11), (7, 13, 14),
         (9, 1, 1), (9, 3, 4), (9, 8, 10),
         (10, 6, 7), (10, 12, 12), (10, 14, 14),
         (11, 9, 9),
         (12, 1, 1), (12, 3, 4), (12, 10, 12),
         (14, 1, 3), (14, 8, 10)
         ]

kopija_ovir = ovire.copy()

class Test(unittest.TestCase):
    def test_01_prehodi(self):
        self.assertEqual(
            {(1, 2), (2, 5), (5, 6), (7, 12), (9, 2), (10, 13), (12, 2)},
            prehodi(ovire))
        self.assertEqual(ovire, kopija_ovir, "ne spreminjaj podanega seznama ovir!")

        ovire2 = ovire.copy()
        random.shuffle(ovire2)
        self.assertEqual(
            {(1, 2), (2, 5), (5, 6), (7, 12), (9, 2), (10, 13), (12, 2)},
            prehodi(ovire2))
        ovire_k2 = ovire2.copy()
        self.assertEqual(ovire2, ovire_k2, "ne spreminjaj podanega seznama ovir!")

    def test_02_nadlezna_ovira(self):
        # prva točka ni na oviri. če jih je več, lahko vrne katerokoli
        self.assertEqual((7, 4, 5), nadlezna_ovira(ovire, 10, 4, "^^^^^^>vvv<<vvv<^<^^"))
        self.assertEqual((9, 3, 4), nadlezna_ovira(ovire, 6, 4, "vvv<"))
        self.assertEqual((5, 3, 5), nadlezna_ovira(ovire, 6, 4, "^"))
        self.assertIsNone(nadlezna_ovira(ovire, 6, 4, ">>^^"))
        self.assertEqual(ovire, kopija_ovir, "ne spreminjaj podanega seznama ovir!")

    def test_03_sprosti(self):
        # vrstni red mora biti ohranjen!
        global ovire

        self.assertIsNone(odstrani(ovire, [4]), "Funkcija naj ne vrača ničesar.")
        self.assertEqual(
            [(1, 1, 1), (1, 3, 3),
             (2, 6, 7), (2, 11, 12),
             (3, 9, 9),
             (5, 7, 10),
             (7, 11, 11), (7, 13, 14),
             (9, 1, 1), (9, 8, 10),
             (10, 6, 7), (10, 12, 12), (10, 14, 14),
             (11, 9, 9),
             (12, 1, 1), (12, 10, 12),
             (14, 1, 3), (14, 8, 10)
             ],
            sorted(ovire)
        )
        indeksi = list(map(kopija_ovir.index, ovire))
        self.assertEqual(sorted(indeksi), indeksi, "Vrstni red ovir se ne sme spremeniti!")
        ovire = kopija_ovir.copy()

        self.assertIsNone(odstrani(ovire, [4, 7, 11]))
        self.assertEqual(
            [(1, 1, 1), (1, 3, 3),
             (3, 9, 9),
             (7, 13, 14),
             (9, 1, 1), (9, 8, 10),
             (10, 12, 12), (10, 14, 14),
             (11, 9, 9),
             (12, 1, 1),
             (14, 1, 3), (14, 8, 10)
             ],
            sorted(ovire)
        )
        indeksi = list(map(kopija_ovir.index, ovire))
        self.assertEqual(sorted(indeksi), indeksi, "Vrstni red ovir se ne sme spremeniti!")
        ovire = kopija_ovir.copy()

        self.assertIsNone(odstrani(ovire, [4, 5]), "Funkcija naj ne vrača ničesar.")
        self.assertEqual(
            [(1, 1, 1), (1, 3, 3),
             (2, 6, 7), (2, 11, 12),
             (3, 9, 9),
             (5, 7, 10),
             (7, 11, 11), (7, 13, 14),
             (9, 1, 1), (9, 8, 10),
             (10, 6, 7), (10, 12, 12), (10, 14, 14),
             (11, 9, 9),
             (12, 1, 1), (12, 10, 12),
             (14, 1, 3), (14, 8, 10)
             ],
            sorted(ovire)
        )
        indeksi = list(map(kopija_ovir.index, ovire))
        self.assertEqual(sorted(indeksi), indeksi, "Vrstni red ovir se ne sme spremeniti!")
        ovire = kopija_ovir.copy()

        self.assertIsNone(odstrani(ovire, [15]), "Funkcija naj ne vrača ničesar.")
        self.assertEqual(ovire, kopija_ovir)
        indeksi = list(map(kopija_ovir.index, ovire))
        self.assertEqual(sorted(indeksi), indeksi, "Vrstni red ovir se ne sme spremeniti!")

        self.assertIsNone(odstrani(ovire, []), "Funkcija naj ne vrača ničesar.")
        self.assertEqual(ovire, kopija_ovir)
        indeksi = list(map(kopija_ovir.index, ovire))
        self.assertEqual(sorted(indeksi), indeksi, "Vrstni red ovir se ne sme spremeniti!")

    def test_04_najdaljsi_skok(self):
        self.assertEqual(0, najdaljsi_skok(ovire, (1, 3, 3)))
        self.assertEqual(0, najdaljsi_skok(ovire, (2, 1, 4)))
        self.assertEqual(0, najdaljsi_skok(ovire, (2, 1, 4)))
        self.assertEqual(2, najdaljsi_skok(ovire, (3, 9, 9)))
        self.assertEqual(1, najdaljsi_skok(ovire, (2, 6, 7)))
        self.assertEqual(2, najdaljsi_skok(ovire, (5, 7, 10)))
        self.assertEqual(3, najdaljsi_skok(ovire, (9, 8, 10)))
        self.assertEqual(3, najdaljsi_skok(ovire, (14, 8, 10)))
        self.assertEqual(6, najdaljsi_skok(ovire, (7, 13, 14)))
        self.assertEqual(6, najdaljsi_skok(ovire, (10, 14, 14)))
        self.assertEqual(7, najdaljsi_skok(ovire, (10, 12, 12)))
        self.assertEqual(3, najdaljsi_skok(ovire, (12, 10, 12)))

    def test_05_anarhist(self):
        k = Kolesar(ovire.copy(), 10, 4)

        self.assertEqual((10, 4), k.lokacija())
        self.assertEqual(0, k.uspesnost())

        k.premik("^")
        self.assertEqual((9, 4), k.lokacija())
        self.assertEqual(1, k.uspesnost())
        self.assertEqual(ovire, kopija_ovir, "kolesar sme spreminjati podani seznam ovir, ne pa vsebine (globalne) spremenljivke `ovire`")

        k.premik("^")
        self.assertEqual((8, 4), k.lokacija())
        self.assertEqual(1, k.uspesnost())

        k.premik("^")
        self.assertEqual((7, 4), k.lokacija())
        self.assertEqual(2, k.uspesnost())

        k.premik("^")
        self.assertEqual((6, 4), k.lokacija())
        self.assertEqual(2, k.uspesnost())

        k.premik("^")
        self.assertEqual((5, 4), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("^")
        self.assertEqual((4, 4), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik(">")
        self.assertEqual((4, 5), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("v")
        self.assertEqual((5, 5), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("v")
        self.assertEqual((6, 5), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("v")
        self.assertEqual((7, 5), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("<")
        self.assertEqual((7, 4), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("<")
        self.assertEqual((7, 3), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("v")
        self.assertEqual((8, 3), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("v")
        self.assertEqual((9, 3), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("v")
        self.assertEqual((10, 3), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("<")
        self.assertEqual((10, 2), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("^")
        self.assertEqual((9, 2), k.lokacija())
        self.assertEqual(3, k.uspesnost())

        k.premik("<")
        self.assertEqual((9, 1), k.lokacija())
        self.assertEqual(4, k.uspesnost())

        k.premik("^")
        self.assertEqual((8, 1), k.lokacija())
        self.assertEqual(4, k.uspesnost())

        k.premik("^")
        self.assertEqual((7, 1), k.lokacija())
        self.assertEqual(4, k.uspesnost())

if __name__ == "__main__":
    unittest.main()
