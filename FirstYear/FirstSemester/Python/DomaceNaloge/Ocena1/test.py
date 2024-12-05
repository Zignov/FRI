

import unittest
import ast
from xml.dom import minidom

povezave = [
    (11, 10, 13, 10),

    (2, 12, 8, 12),
    (6, 11, 6, 13),

    (0, 16, 10, 16),
    (3, 18, 3, 13),
    (7, 14, 3, 14),
    (9, 17, 9, 14),
    (13, 15, 8, 15),
    (12, 14, 12, 17),
    (13, 16, 21, 16),
    (14, 18, 14, 15),
    (13, 15, 13, 16),
    (16, 16, 16, 10),
    (16, 10, 21, 10),
    (14, 18, 10, 18),
    (11, 13, 11, 20),
    (15, 13, 22, 13),
    (17, 15, 17, 17),
    (18, 17, 18, 14),
    (19, 19, 22, 19),
    (20, 15, 20, 17),
    (21, 10, 21, 19),
]

def pravilna(povezava):
    if (povezava[0] == povezava[2]):
        if(povezava[1] != povezava[3]):
            return True
    elif (povezava[1] == povezava[3]):
        if(povezava[0] != povezava[2]):
            return True
    else: return False
    
def pravilne(povezave):
    rez = True
    for x in povezave:
        if pravilna(x) != True:
            rez = False
    return rez

def urejena(povezava):
    
    if (povezava[0], povezava[1]) <= (povezava[2], povezava[3]):
        return(povezava[0], povezava[1], povezava[2], povezava[3])
    else:
        return (povezava[2], povezava[3], povezava[0], povezava[1])
    
def na_povezavi(x, y, povezava):
    povezava = urejena(povezava)
    if (povezava[0]<=x<=povezava[2]) and (povezava[1]<=y<=povezava[3]):
        return True
    return False

def povezave_tocke(x, y, povezave):
    rez = set()
    for povezava in povezave:
        if na_povezavi(x, y, urejena(povezava)):
            rez.add(urejena(povezava))
    return rez

from collections import Counter            

def secisce(povezava1, povezava2):
    x1, y1, x2, y2 = urejena(povezava1)
    x3, y3, x4, y4 = urejena(povezava2)
    
    if x1 == x2 and y3 == y4:
        if x3<=x1<=x4 and y1<=y3<=y2:
            return(x1, y3)

    elif y1 == y2 and x3 == x4:
        if y3<=y1<=y4 and x1<=x3<=x2:
            return(x3, y1)
    
    return None
    
def krizisca(povezave):
    resitev = {}
    for x in povezave:
        for y in povezave:
            if x!=y:
                add = secisce((x), (y))
                if add:
                    resitev[tuple(sorted((urejena(x),urejena(y))))] = add
                
    return resitev

from itertools import pairwise

def mozna_pot(pot, mreza):
    '''rez = True
    #print(list(pairwise(pot)))

    for x,y in pairwise(pot):
        #print((urejena(x),urejena(y)))
        #print(((urejena(x),urejena(y))) not in mreza or ((urejena(y),urejena(x))) not in mreza)
        if ((urejena(x),urejena(y))) not in mreza and ((urejena(y), urejena(x)) not in mreza):
            rez = False
    return rez'''

    return all((urejena(x), urejena(y)) in mreza or (urejena(y), urejena(x)) in mreza for x,y in pairwise(pot))


def razdalja(pot, mreza): 
    razdalja_skupna = 0
    presecisce_prejsnje = None
    for x in range(len(pot)-1):
        povezava1 = urejena(pot[x])
        povezava2 = urejena(pot[x + 1])
        if (povezava1, povezava2) in mreza or (povezava2, povezava1) in mreza:
            presecisce = secisce(povezava1, povezava2)
            if presecisce:
                if presecisce_prejsnje:
                    x1, y1 = presecisce
                    x2, y2 = presecisce_prejsnje
                    razdalja_skupna += abs(x1- x2) + abs(y1 - y2)
                presecisce_prejsnje = presecisce
    return razdalja_skupna



class TestOneLineMixin:
    functions = {
        elm.name: elm
        for elm in ast.parse(open(__file__, "r", encoding="utf-8").read()).body
        if isinstance(elm, ast.FunctionDef)}

    def assert_is_one_line(self, func):
        body = self.functions[func.__code__.co_name].body
        self.assertEqual(len(body), 1, "\nFunkcija ni dolga le eno vrstico")
        self.assertIsInstance(body[0], ast.Return, "\nFunkcija naj bi vsebovala le return")

    def test_nedovoljene_funkcije(self):
        dovoljene_funkcije = {
            "pravilna", "pravilne", "urejena", "na_povezavi",
            "povezave_tocke", "secisce", "krizisca", "mozna_pot",
            "razdalja", "svg", "povezane", "dostopne", "pot"}
        for func in self.functions:
            self.assertIn(func, dovoljene_funkcije, f"\nFunkcija {func} ni dovoljena.")


class Test06(unittest.TestCase):
    def test_01_pravilna(self):
        self.assertTrue(pravilna((10, 20, 10, 22)))
        self.assertTrue(pravilna((10, 22, 10, 20)))
        self.assertTrue(pravilna((13, 5, 18, 5)))
        self.assertTrue(pravilna((18, 5, 13, 5)))

        # Ni OK: spremenita se obe koordinati
        self.assertFalse(pravilna((10, 18, 12, 4)))
        self.assertFalse(pravilna((18, 10, 4, 12)))
        self.assertFalse(pravilna((10, 20, 10, 20)))

        # Ni OK: ne spremeni se nobena koordinata
        self.assertFalse(pravilna((10, 12, 10, 12)))

    def test_02_pravilne(self):
        self.assertTrue(pravilne(povezave))
        self.assertTrue(pravilne([(1, 5, 1, 8)]))
        self.assertTrue(pravilne([(1, 5, 2, 5)]))

        self.assertFalse(pravilne(povezave + [(10, 10, 10, 10)]))
        self.assertFalse(pravilne([(10, 10, 10, 10)] + povezave))
        self.assertFalse(pravilne(povezave + [(10, 18, 12, 4)]))
        self.assertFalse(pravilne([(10, 18, 12, 4)] + povezave))

    def test_03_urejena(self):
        self.assertEqual((10, 20, 10, 22), urejena((10, 20, 10, 22)))
        self.assertEqual((10, 20, 10, 22), urejena((10, 22, 10, 20)))
        self.assertEqual((13, 5, 18, 5), urejena((13, 5, 18, 5)))
        self.assertEqual((13, 5, 18, 5), urejena((18, 5, 13, 5)))

    def test_04_na_povezavi(self):
        self.assertTrue(na_povezavi(10, 20, (10, 20, 10, 22)))
        self.assertTrue(na_povezavi(10, 21, (10, 20, 10, 22)))
        self.assertTrue(na_povezavi(10, 22, (10, 20, 10, 22)))
        self.assertTrue(na_povezavi(10, 20, (10, 22, 10, 20)))
        self.assertTrue(na_povezavi(10, 21, (10, 22, 10, 20)))
        self.assertTrue(na_povezavi(10, 22, (10, 22, 10, 20)))
        self.assertFalse(na_povezavi(10, 23, (10, 22, 10, 20)))
        self.assertFalse(na_povezavi(10, 19, (10, 22, 10, 20)))
        self.assertFalse(na_povezavi(10, 23, (10, 20, 10, 22)))
        self.assertFalse(na_povezavi(10, 19, (10, 20, 10, 22)))
        self.assertFalse(na_povezavi(9, 21, (10, 20, 10, 22)))
        self.assertFalse(na_povezavi(9, 21, (10, 22, 10, 20)))
        self.assertFalse(na_povezavi(11, 21, (10, 20, 10, 22)))
        self.assertFalse(na_povezavi(11, 21, (10, 22, 10, 20)))

        self.assertTrue(na_povezavi( 20, 10, (20, 10, 22, 10)))
        self.assertTrue(na_povezavi( 21, 10, (20, 10, 22, 10)))
        self.assertTrue(na_povezavi( 22, 10, (20, 10, 22, 10)))
        self.assertTrue(na_povezavi( 20, 10, (22, 10, 20, 10)))
        self.assertTrue(na_povezavi( 21, 10, (22, 10, 20, 10)))
        self.assertTrue(na_povezavi( 22, 10, (22, 10, 20, 10)))
        self.assertFalse(na_povezavi(23, 10, (22, 10, 20, 10)))
        self.assertFalse(na_povezavi(19, 10, (22, 10, 20, 10)))
        self.assertFalse(na_povezavi(23, 10, (20, 10, 22, 10)))
        self.assertFalse(na_povezavi(19, 10, (20, 10, 22, 10)))
        self.assertFalse(na_povezavi(21,  9, (20, 10, 22, 10)))
        self.assertFalse(na_povezavi(21,  9, (22, 10, 20, 10)))
        self.assertFalse(na_povezavi(21, 11, (20, 10, 22, 10)))
        self.assertFalse(na_povezavi(21, 11, (22, 10, 20, 10)))

    def test_05_povezave_tocke(self):
        self.assertEqual({(3, 13, 3, 18)}, povezave_tocke(3, 15, povezave))
        self.assertEqual({(3, 13, 3, 18)}, povezave_tocke(3, 18, povezave))
        self.assertEqual({(3, 13, 3, 18)}, povezave_tocke(3, 13, povezave))

        self.assertEqual({(11, 13, 11, 20)}, povezave_tocke(11, 17, povezave))
        self.assertEqual({(11, 13, 11, 20)}, povezave_tocke(11, 13, povezave))
        self.assertEqual({(11, 13, 11, 20)}, povezave_tocke(11, 20, povezave))

        self.assertEqual({(6, 11, 6, 13), (2, 12, 8, 12)},
                         povezave_tocke(6, 12, povezave))
        self.assertEqual({(3, 14, 7, 14), (3, 13, 3, 18)},
                         povezave_tocke(3, 14, povezave))
        self.assertEqual({(13, 16, 21, 16), (13, 15, 13, 16)},
                         povezave_tocke(13, 16, povezave))

        self.assertEqual(set(), povezave_tocke(13, 17, povezave))

    def test_06_secisce(self):
        # Sekanje
        self.assertEqual((10, 22), secisce((10, 20, 10, 25), (8, 22, 18, 22)))
        self.assertEqual((10, 22), secisce((10, 25, 10, 22), (8, 22, 18, 22)))
        self.assertEqual((10, 22), secisce((10, 25, 10, 22), (18, 22, 8, 22)))
        self.assertEqual((10, 22), secisce((10, 20, 10, 25), (18, 22, 8, 22)))

        self.assertEqual((10, 22), secisce((8, 22, 18, 22), (10, 20, 10, 25)))
        self.assertEqual((10, 22), secisce((8, 22, 18, 22), (10, 25, 10, 22)))
        self.assertEqual((10, 22), secisce((18, 22, 8, 22), (10, 25, 10, 22)))
        self.assertEqual((10, 22), secisce((18, 22, 8, 22), (10, 20, 10, 25)))

        # Dotikanje
        self.assertEqual((10, 22), secisce((10, 20, 10, 25), (10, 22, 18, 22)))
        self.assertEqual((10, 22), secisce((10, 25, 10, 20), (10, 22, 18, 22)))
        self.assertEqual((10, 22), secisce((10, 25, 10, 20), (18, 22, 10, 22)))
        self.assertEqual((10, 22), secisce((10, 20, 10, 25), (18, 22, 10, 22)))

        # Dotikanje v točki
        self.assertEqual((10, 20), secisce((10, 20, 10, 25), (10, 20, 8, 20)))
        self.assertEqual((10, 20), secisce((10, 25, 10, 20), (10, 20, 8, 20)))
        self.assertEqual((10, 20), secisce((10, 25, 10, 20), (8, 20, 10, 20)))
        self.assertEqual((10, 20), secisce((10, 20, 10, 25), (8, 20, 10, 20)))

        # Sekanje
        self.assertEqual((22, 10), secisce((20, 10, 25, 10), (22,  8, 22, 18)))
        self.assertEqual((22, 10), secisce((25, 10, 22, 10), (22,  8, 22, 18)))
        self.assertEqual((22, 10), secisce((25, 10, 22, 10), (22, 18, 22,  8)))
        self.assertEqual((22, 10), secisce((20, 10, 25, 10), (22, 18, 22,  8)))
        self.assertEqual((22, 10), secisce((22,  8, 22, 18), (20, 10, 25, 10)))
        self.assertEqual((22, 10), secisce((22,  8, 22, 18), (25, 10, 22, 10)))
        self.assertEqual((22, 10), secisce((22, 18, 22,  8), (25, 10, 22, 10)))
        self.assertEqual((22, 10), secisce((22, 18, 22,  8), (20, 10, 25, 10)))

        # Dotikanje
        self.assertEqual((22, 10), secisce((20, 10, 25, 10), (22, 10, 22, 18)))
        self.assertEqual((22, 10), secisce((25, 10, 20, 10), (22, 10, 22, 18)))
        self.assertEqual((22, 10), secisce((25, 10, 20, 10), (22, 18, 22, 10)))
        self.assertEqual((22, 10), secisce((20, 10, 25, 10), (22, 18, 22, 10)))

        # Dotikanje v točki
        self.assertEqual((20, 10), secisce((20, 10, 25, 10), (20, 10, 20,  8)))
        self.assertEqual((20, 10), secisce((25, 10, 20, 10), (20, 10, 20,  8)))
        self.assertEqual((20, 10), secisce((25, 10, 20, 10), (20,  8, 20, 10)))
        self.assertEqual((20, 10), secisce((20, 10, 25, 10), (20,  8, 20, 10)))

        # Ni sekanja: vzporedni
        self.assertIsNone(secisce((10, 20, 10, 25), (8, 20, 8, 25)))
        self.assertIsNone(secisce((8, 20, 8, 25), (10, 20, 10, 25)))
        self.assertIsNone(secisce((8, 20, 18, 20), (1, 25, 0, 25)))

        # Ni sekanja: različni
        self.assertIsNone(secisce((10, 20, 10, 25), (12, 22, 15, 22)))

        krizisca = Test07.prava_krizisca
        for p1 in povezave:
            for p2 in povezave:
                if p1 != p2:
                    up1, up2 = urejena(p1), urejena(p2)
                    if (up1, up2) in krizisca:
                        self.assertEqual(krizisca[up1, up2], secisce(p1, p2),
                                         f"Napaka v klicu secisce({p1}, {p2})")
                    elif (up2, up1) in krizisca:
                        self.assertEqual(krizisca[up2, up1], secisce(p1, p2),
                                         f"Napaka v klicu secisce({p1}, {p2})")
                    else:
                        self.assertIsNone(secisce(p1, p2), f"Napaka v klicu secisce({p1}, {p2})")


class Test07(unittest.TestCase):
    prava_krizisca = {
         ((0, 16, 10, 16), (3, 13, 3, 18)): (3, 16),
         ((0, 16, 10, 16), (9, 14, 9, 17)): (9, 16),
         ((2, 12, 8, 12), (6, 11, 6, 13)): (6, 12),
         ((3, 13, 3, 18), (3, 14, 7, 14)): (3, 14),
         ((8, 15, 13, 15), (9, 14, 9, 17)): (9, 15),
         ((8, 15, 13, 15), (11, 13, 11, 20)): (11, 15),
         ((8, 15, 13, 15), (12, 14, 12, 17)): (12, 15),
         ((8, 15, 13, 15), (13, 15, 13, 16)): (13, 15),
         ((10, 18, 14, 18), (11, 13, 11, 20)): (11, 18),
         ((10, 18, 14, 18), (14, 15, 14, 18)): (14, 18),
         ((13, 15, 13, 16), (13, 16, 21, 16)): (13, 16),
         ((13, 16, 21, 16), (14, 15, 14, 18)): (14, 16),
         ((13, 16, 21, 16), (16, 10, 16, 16)): (16, 16),
         ((13, 16, 21, 16), (17, 15, 17, 17)): (17, 16),
         ((13, 16, 21, 16), (18, 14, 18, 17)): (18, 16),
         ((13, 16, 21, 16), (20, 15, 20, 17)): (20, 16),
         ((13, 16, 21, 16), (21, 10, 21, 19)): (21, 16),
         ((15, 13, 22, 13), (16, 10, 16, 16)): (16, 13),
         ((15, 13, 22, 13), (21, 10, 21, 19)): (21, 13),
         ((16, 10, 16, 16), (16, 10, 21, 10)): (16, 10),
         ((16, 10, 21, 10), (21, 10, 21, 19)): (21, 10),
         ((19, 19, 22, 19), (21, 10, 21, 19)): (21, 19)}

    def test_01_krizisca(self):
        self.assertEqual(self.prava_krizisca, krizisca(povezave))
        self.assertEqual(
            {((0, 16, 10, 16), (3, 13, 3, 18)): (3, 16),
             ((0, 16, 10, 16), (9, 14, 9, 17)): (9, 16),
             ((2, 12, 8, 12), (6, 11, 6, 13)): (6, 12),
             ((3, 13, 3, 18), (3, 14, 7, 14)): (3, 14),
             ((8, 15, 13, 15), (9, 14, 9, 17)): (9, 15)},
            krizisca(povezave[:8]))

    def test_02_mozna_pot(self):
        self.assertTrue(mozna_pot(
            [(14, 18, 10, 18),
             (14, 18, 14, 15),
             (13, 16, 21, 16),
             (13, 16, 13, 15),
             (8, 15, 13, 15),
             (9, 14, 9, 17),
             (10, 16, 0, 16),
             (9, 14, 9, 17),
             (8, 15, 13, 15),
             (13, 16, 13, 15)], self.prava_krizisca))

        self.assertFalse(mozna_pot(
            [(14, 18, 10, 18),
             (14, 18, 14, 15),
             (13, 16, 13, 15),
             (8, 15, 13, 15),
             (9, 14, 9, 17),
             (10, 16, 0, 16),
             (9, 14, 9, 17),
             (8, 15, 13, 15),
             (13, 16, 13, 15)], self.prava_krizisca))

        self.assertFalse(mozna_pot(
            [(14, 18, 10, 18),
             (14, 18, 14, 15),
             (13, 16, 21, 16),
             (13, 16, 13, 15),
             (8, 15, 14, 15),
             (9, 14, 9, 17),
             (10, 16, 0, 16),
             (9, 14, 9, 17),
             (8, 15, 13, 15),
             (13, 16, 13, 15)], self.prava_krizisca))

    def test_03_razdalja(self):
        self.assertEqual(
            14,
            razdalja([(14, 18, 10, 18),
             (14, 18, 14, 15),
             (13, 16, 21, 16),
             (13, 16, 13, 15),
             (8, 15, 13, 15),
             (9, 14, 9, 17),
             (10, 16, 0, 16),
             (9, 14, 9, 17),
             (8, 15, 13, 15),
             (13, 16, 13, 15)], self.prava_krizisca)
        )

class Test08(unittest.TestCase, TestOneLineMixin):
    def test(self):
        self.assert_is_one_line(pravilna)
        self.assert_is_one_line(pravilne)
        self.assert_is_one_line(urejena)
        self.assert_is_one_line(povezave_tocke)

class Test09(unittest.TestCase, TestOneLineMixin):
    def test(self):
        self.assert_is_one_line(krizisca)
        self.assert_is_one_line(mozna_pot)
        self.assert_is_one_line(razdalja)

    def test_01_svg(self):
        for pov in [povezave[:8], povezave]:
            urejene = set(map(urejena, pov))

            svg(pov, "test.svg")
            dom = minidom.parse("test.svg")
            el_svg = dom.getElementsByTagName("svg")[0]

            viewport = el_svg.getAttribute("viewBox")
            mix, miy, wi, he = map(int, viewport.split())
            self.assertLessEqual(mix, min(x for x, _, _, _ in pov))
            self.assertLessEqual(miy, min(y for _, y, _, _ in pov))
            self.assertGreaterEqual(mix + wi, max(x for _, _, x, _ in pov))
            self.assertGreaterEqual(miy + he, max(y for _, _, _, y in pov))

            self.assertEqual(
                sorted(urejene),
                sorted({urejena(tuple(int(line.getAttribute(a)) for a in "x1 y1 x2 y2".split()))
                  for line in el_svg.getElementsByTagName("line")}))
            self.assertEqual(
                {p[:2] for p in pov} | {p[2:] for p in pov},
                { tuple(int(line.getAttribute(a)) for a in "cx cy".split())
                  for line in el_svg.getElementsByTagName("circle")})


class Test10(unittest.TestCase):
    def test_01_povezane(self):
        self.assertEqual(
            {(0, 16, 10, 16): {(3, 13, 3, 18),
                               (9, 14, 9, 17)},
             (2, 12, 8, 12): {(6, 11, 6, 13)},
             (3, 13, 3, 18): {(0, 16, 10, 16),
                              (3, 14, 7, 14)},
             (3, 14, 7, 14): {(3, 13, 3, 18)},
             (6, 11, 6, 13): {(2, 12, 8, 12)},
             (8, 15, 13, 15): {(9, 14, 9, 17),
                               (11, 13, 11, 20),
                               (12, 14, 12, 17),
                               (13, 15, 13, 16)},
             (9, 14, 9, 17): {(0, 16, 10, 16),
                              (8, 15, 13, 15)},
             (10, 18, 14, 18): {(14, 15, 14, 18),
                                (11, 13, 11, 20)},
             (11, 13, 11, 20): {(8, 15, 13, 15),
                                (10, 18, 14, 18)},
             (12, 14, 12, 17): {(8, 15, 13, 15)},
             (13, 15, 13, 16): {(8, 15, 13, 15),
                                (13, 16, 21, 16)},
             (13, 16, 21, 16): {(13, 15, 13, 16),
                                (14, 15, 14, 18),
                                (16, 10, 16, 16),
                                (17, 15, 17, 17),
                                (18, 14, 18, 17),
                                (20, 15, 20, 17),
                                (21, 10, 21, 19)},
             (14, 15, 14, 18): {(10, 18, 14, 18),
                                (13, 16, 21, 16)},
             (15, 13, 22, 13): {(16, 10, 16, 16),
                                (21, 10, 21, 19)},
             (16, 10, 16, 16): {(13, 16, 21, 16),
                                (15, 13, 22, 13),
                                (16, 10, 21, 10)},
             (16, 10, 21, 10): {(16, 10, 16, 16),
                                (21, 10, 21, 19)},
             (17, 15, 17, 17): {(13, 16, 21, 16)},
             (18, 14, 18, 17): {(13, 16, 21, 16)},
             (19, 19, 22, 19): {(21, 10, 21, 19)},
             (20, 15, 20, 17): {(13, 16, 21, 16)},
             (21, 10, 21, 19): {(13, 16, 21, 16),
                                (15, 13, 22, 13),
                                (16, 10, 21, 10),
                                (19, 19, 22, 19)}},
            povezane(Test07.prava_krizisca))

    def test_02_dostopne(self):
        obmocje1 =  {
            (0, 16, 10, 16),
            (3, 13, 3, 18),
            (3, 14, 7, 14),
            (8, 15, 13, 15),
            (9, 14, 9, 17),
            (10, 18, 14, 18),
            (11, 13, 11, 20),
            (12, 14, 12, 17),
            (13, 15, 13, 16),
            (13, 16, 21, 16),
            (14, 15, 14, 18),
            (15, 13, 22, 13),
            (16, 10, 16, 16),
            (16, 10, 21, 10),
            (17, 15, 17, 17),
            (18, 14, 18, 17),
            (19, 19, 22, 19),
            (20, 15, 20, 17),
            (21, 10, 21, 19)}

        obmocje2 = {(6, 11, 6, 13), (2, 12, 8, 12)}
        obmocje3 = {(11, 10, 13, 10)}

        self.assertEqual(obmocje1, dostopne((0, 16, 10, 16), Test07.prava_krizisca))
        self.assertEqual(obmocje1, dostopne((20, 15, 20, 17), Test07.prava_krizisca))
        self.assertEqual(obmocje1, dostopne((20, 17, 20, 15), Test07.prava_krizisca))

        self.assertEqual(obmocje2, dostopne((2, 12, 8, 12), Test07.prava_krizisca))
        self.assertEqual(obmocje2, dostopne((8, 12, 2, 12), Test07.prava_krizisca))
        self.assertEqual(obmocje2, dostopne((6, 13, 6, 11), Test07.prava_krizisca))
        self.assertEqual(obmocje2, dostopne((6, 11, 6, 13), Test07.prava_krizisca))

        self.assertEqual(obmocje3, dostopne((11, 10, 13, 10), Test07.prava_krizisca))
        self.assertEqual(obmocje3, dostopne((13, 10, 11, 10), Test07.prava_krizisca))

    def test_03_pot(self):
        for sx, sy, ex, ey in [(11, 19, 17, 10),
                               (17, 10, 11, 19),
                               (1, 16, 22, 13)]:
            najdena = pot(sx, sy, ex, ey, Test07.prava_krizisca)
            rez = '\n'.join(map(str, najdena))
            napaka = f"Napaka pri iskanju poti od ({sx}, {sy}) do ({ex}, {ey}):\n{rez}"
            self.assertTrue(mozna_pot(najdena, Test07.prava_krizisca), napaka)
            self.assertTrue(na_povezavi(sx, sy, najdena[0]), napaka)
            self.assertTrue(na_povezavi(ex, ey, najdena[-1]), napaka)

        # Ni poti - območji sta nepovezani
        self.assertIsNone(pot(11, 19, 13, 10, Test07.prava_krizisca))

        # Na prvi točki ni povezave
        self.assertIsNone(pot(8, 18, 8, 16, Test07.prava_krizisca))
        # Na drugi točki ni povezave
        self.assertIsNone(pot(8, 16, 8, 18, Test07.prava_krizisca))


if __name__ == "__main__":
    unittest.main()
