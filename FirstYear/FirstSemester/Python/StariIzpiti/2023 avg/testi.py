
import random
import unittest


def nestrinjanja(ovire1, ovire2):
    rez = []
    print(ovire1, '\n', ovire2)
    for x in ovire1:
        if x not in ovire2:
            rez.append(x)
            
    for x in ovire2:
        if x not in ovire1 and x not in rez:
            rez.append(x)

    print(rez)
    return set(rez)

def proste_ovire(ovire):
    print(ovire)
    rez = set(ovire)
    for x0, x1, y in ovire:
        for x0_, x1_, y_ in ovire:
            if y == y_ and (x0_ <= x0 <= x1_ or x0_ <= x1 <= x1_):
                if (x0, x1, y) in rez and (x0 != x0_ or x1 != x1_):
                    rez.remove((x0, x1, y))
    return list(rez)
        


def dolzina_ovir(ime_datoteke):
    a = open(ime_datoteke, mode="r", encoding="utf-8")
    rez = 0
    for line in a:
        if line != "\n":
            print(line)
            zacetek, konec = line.split(" ")[0].split("-")
            rez += (int(konec) - int(zacetek) + 1)
            
            print(zacetek, "sdfs", konec)
    return rez

def zdruzi_ovire(ovire):
    nove_ovire = ovire
    
    for x0, x1, y in ovire:
        for x0_, x1_, y_ in ovire:
            if x1+1 == x0_ and y == y_:
                nove_ovire.remove((x0, x1, y))
                nove_ovire.remove((x0_, x1_, y_))
                
                print(f"removed: {(x0, x1, y)} and {(x0_, x1_, y_)}")
                
                nove_ovire.append((x0, x1_, y))
                print(f"added: {(x0, x1_, y)}")
                zdruzi_ovire(nove_ovire)
      
    return (nove_ovire)


class Kolesarska:
    
    def __init__(self):
        self.zemljevid = []

    def dodaj_oviro(self, x0, x1, y):
        self.zemljevid.append((x0, x1, y))
        
    def stevilo_ovir(self):
        return (len(self.zemljevid))
    
    def prosto(self, x, y):
        print(self.zemljevid)
        rez = True
        
        for x0, x1, y_ in self.zemljevid:
            if y == y_ and x0<= x <= x1:
                rez = False
            else:
                rez = True
                
        print(rez)
        return rez
    
class InteligentnaKolesarska(Kolesarska):
    def __init__(self):
        super().__init__()
        super().stevilo_ovir
        
    def prosto(self, x, y):
        is_free = super().prosto(x, y)
        if is_free:
            self.dodaj_oviro(x, x, y)
        return is_free
        
        



ovire = [(1, 3, 6), (2, 4, 3),
         (3, 4, 9), (6, 9, 5), (9, 10, 2), (9, 10, 8),
         (4, 6, 7),
         ]


class Test(unittest.TestCase):
    def test_01_nestrinjanja(self):
        dodatne = [(3, 5, 1), (1, 2, 3)]
        ovire2 = ovire[1:-2] + dodatne
        self.assertEqual(set(ovire[:1] + ovire[-2:] + dodatne), nestrinjanja(ovire, ovire2))

    def test_02_proste_ovire(self):
        ovire = [(1, 3, 6), (2, 4, 3),
                 (3, 4, 9), (6, 9, 5), (9, 10, 2), (9, 10, 8),
                 (4, 6, 7),
                 (1, 2, 10), (5, 8, 10),
                 (5, 8, 13), (5, 8, 13),

                 (3, 5, 6),
                 (4, 6, 5), (8, 10, 5),
                 (1, 2, 3), (3, 3, 3), (4, 7, 3), (6, 8, 3)
                 ]
        for _ in range(5):
            random.shuffle(ovire)
            self.assertEqual(
                {(3, 4, 9), (9, 10, 2), (9, 10, 8), (4, 6, 7), (1, 2, 10), (5, 8, 10)},
                set(proste_ovire(ovire)))

    def test_03_dolzina_ovir(self):
        with open("ovire.txt", "wt", encoding="utf8") as f:
            f.write("".join(f"{x0}-{x1} {y}\n" for x0, x1, y in ovire))
        self.assertEqual(19, dolzina_ovir("ovire.txt"))

    def test_04_zdruzi_ovire(self):
        ovire = [(1, 3, 2), (4, 6, 2),
                 (4, 8, 5), (11, 13, 5),
                 (1, 3, 6),
                 (3, 5, 8), (6, 6, 8), (7, 10, 8)]
        self.assertEqual([(1, 6, 2), (4, 8, 5), (11, 13, 5), (1, 3, 6), (3, 10, 8)], zdruzi_ovire(ovire))

        ovire = [(1, 3, 2), (4, 6, 2),
                 (4, 8, 5), (11, 13, 5),
                 (1, 3, 6),
                 (3, 5, 8), (6, 6, 8), (7, 10, 8),
                 (3, 5, 10)]
        self.assertEqual([(1, 6, 2), (4, 8, 5), (11, 13, 5), (1, 3, 6), (3, 10, 8), (3, 5, 10)], zdruzi_ovire(ovire))

    def test_05_kolesarska(self):
        k = Kolesarska()

        self.assertEqual(0, k.stevilo_ovir())
        self.assertTrue(k.prosto(4, 8))
        self.assertTrue(k.prosto(4, 8))

        k.dodaj_oviro(3, 5, 7)
        self.assertEqual(1, k.stevilo_ovir())
        self.assertTrue(k.prosto(4, 8))
        self.assertTrue(k.prosto(4, 8))

        k.dodaj_oviro(1, 2, 8)
        self.assertEqual(2, k.stevilo_ovir())
        self.assertTrue(k.prosto(4, 8))
        self.assertTrue(k.prosto(4, 8))

        k.dodaj_oviro(3, 5, 8)
        self.assertEqual(3, k.stevilo_ovir())
        self.assertFalse(k.prosto(4, 8))

        # Test, da inteligentna kolesarska ne definira drugih metod kot `prosto`
        dodatne = [f"`{k}`" for k in InteligentnaKolesarska.__dict__
                   if not (k[:2] == "__" or k == "prosto")]
        self.assertTrue(
            not dodatne,
            f"Razred InteligentnaKolesarska naj definira samo metodo `prosto`,\n"
            f"ne pa tudi {','.join(dodatne)}")

        # Test, da se ovire dodajajo
        k2 = InteligentnaKolesarska()
        self.assertEqual(0, k2.stevilo_ovir())
        self.assertTrue(k2.prosto(4, 8))
        self.assertEqual(1, k2.stevilo_ovir())
        self.assertFalse(k2.prosto(4, 8))

        # Test, da inteligentna kolesarska sicer deluje kot normalna
        k = InteligentnaKolesarska()

        self.assertEqual(0, k.stevilo_ovir())

        k.dodaj_oviro(3, 5, 7)
        self.assertEqual(1, k.stevilo_ovir())
        self.assertTrue(k.prosto(4, 8))
        self.assertEqual(2, k.stevilo_ovir())


if __name__ == "__main__":
    unittest.main()
