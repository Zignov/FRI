
def po_urah(a):
    rez = []
    stevec = 0
    ura = 0
    for stevilka in a:
        if stevec == 60:
            #print("uraaaa:", ura)
            rez.append(ura)
            #print(rez)
            ura = 0
            stevec = 0
        
        ura += stevilka
        stevec += 1
    rez.append(ura)
    
    #print(rez)
    return rez

def naj_ura(a):
    seznam = po_urah(a)
    stevec = 0
    rezultat = 0
    max = seznam[0]
    for x in seznam:
        #print(max)
        #print(stevec)
        if x>max:
            max = x
            rezultat = stevec
        stevec += 1
    return rezultat

def brez_prehodov(a):
    stevec = 0
    for x in a:
        print (x)
        if x == 0:
            stevec += 1
            
    return stevec


def obdobje_brez(a):
    stevec = 0
    stetje = False
    zacetek = 0
    konec = 0
    obdobje = 0
    max_obdobje = 0
    rez = (0,0)
    for x in a:
        #print(f'{zacetek, konec, obdobje, max_obdobje, stetje} znak = {x}')
        if x==0:
            if stetje == False:
                zacetek = stevec
                stetje = True
                obdobje = 1
            else:
                obdobje += 1
                
        else:
            if stetje == True:
                konec = stevec-1
                stetje = False

                if obdobje > max_obdobje:
                    max_obdobje = obdobje
                    rez = (zacetek, konec)
                    
        stevec += 1
        
        if obdobje > max_obdobje:
            rez = (zacetek, stevec-1)
                    
    return rez


def obremenitve(imena, porocila):
    stevilo = len(imena)
    stevec = 1
    odgovor = {}
    rez = 0
    rezultat = 0
    
    for x in porocila:
        if stevec not in odgovor:
            odgovor[stevec] = x
        else:
            odgovor[stevec] += x
            
        if stevec<stevilo:
            stevec += 1
        else:
            stevec = 1
            
        print(odgovor)
        
    for x in odgovor:
        if rez < odgovor[x]:
            rez = odgovor[x]
            rezultat = x
            
    return(imena[rezultat-1])
        
            

def zlata_minuta(i, a):
    zlate = []
    stevec = 60
    rez = False
    for x in range(60):
        zlate.append(x)
        
    for x in a[60:]:
        if x != 0:
            if stevec%2 == 0:
                if stevec//2 in zlate:
                    print(f"stevec: {stevec}, stevec//2= {stevec//2}, a = {a[stevec//2]}")
                    zlate.append(stevec)
            else:
                if (stevec//2) in zlate or (stevec+1)//2 in zlate:
                    zlate.append(stevec)
        stevec += 1
        
    #print(zlate)  
    #print (a[210])
    if i in zlate:
        rez = True
    return rez


class Senzor:
    def __init__(self, ident):
        self.ident = ident
        self.poz = 0
        self.neg = 0


    def prehod(self, smer):
        if smer == "+":
            self.poz += 1
        else:
            self.neg += 1
            
    def prehodov(self):
        return ((self.poz, self.neg))
    

class NadzorniSistem:
    def __init__(self, senzorji):
        self.senzorji = senzorji
            
    def prehod(self, id, smer):
        for x in self.senzorji:
            if x.ident == id:
                return(x.prehod(smer))
                    
    def prehodov(self, id):
        for x in self.senzorji:
            if x.ident == id:
                return(x.prehodov())


import unittest

class Test(unittest.TestCase):
    a = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
         2, 0, 0, 2, 0, 0, 2, 2, 2, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0,
         0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 1, 1, 0,
         0, 1, 0, 0, 2, 2, 1, 1, 0, 3, 0, 1, 2, 1, 0, 1, 0, 0, 0, 0, 3, 1, 1, 2, 1, 2, 1, 1, 0, 2, 2, 0, 1, 2, 1, 1,
         1, 0, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 0, 0, 2, 1, 0, 4, 2, 1, 3, 1, 1, 1, 1, 0, 1, 1, 2, 0, 1, 1, 1,
         1, 1, 1, 0, 2, 1, 0, 1, 2, 2, 1, 2, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 2, 1, 2, 0, 2, 2, 4, 2, 3,
         1, 2, 3, 0, 1, 1, 3, 1, 1, 2, 2, 0, 2, 3, 2, 2, 2, 0, 0, 1, 1, 1, 1, 2, 4, 1, 0, 2, 2, 3, 2, 1, 1, 2, 2, 2,
         2, 1, 2, 1, 2, 3, 3, 1, 2, 3, 2, 2, 2, 2, 1, 0, 4, 2, 2, 2, 2, 1, 2, 3, 1, 2, 1, 2, 2, 2, 2, 3, 2, 3, 2, 0,
         3, 0, 3, 0, 1, 1, 2, 3, 3, 0, 3, 4, 2, 3, 1, 3, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 2, 4, 3, 3, 2, 0, 2, 1, 1, 2,
         4, 2, 3, 3, 0, 2, 1, 4, 3, 2, 2, 0, 2, 3, 2, 2, 1, 2, 0, 4, 4, 2, 1, 3, 1, 2, 2, 2, 2, 4, 2, 3, 2, 3, 3, 2,
         3, 4, 2, 1, 4, 2, 3, 5, 3, 2, 3, 5, 3, 4, 1, 2, 5, 3, 5, 4, 4, 2, 3, 3, 5, 3, 4, 3, 3, 3, 3, 4, 4, 4, 4, 4,
         4, 4, 4, 5, 3, 4, 3, 3, 2, 4, 4, 4, 2, 2, 5, 4, 4, 4, 3, 3, 3, 3, 4, 3, 4, 4, 7, 4, 6, 5, 4, 5, 4, 4, 1, 4,
         5, 5, 4, 6, 3, 4, 3, 5, 4, 5, 4, 5, 4, 2, 4, 5, 5, 3, 2, 4, 5, 3, 4, 4, 6, 4, 7, 4, 4, 5, 3, 6, 5, 7, 5, 4,
         5, 7, 5, 5, 5, 5, 4, 7, 5, 6, 5, 3, 4, 7, 7, 5, 6, 4, 5, 4, 7, 5, 4, 7, 7, 6, 7, 4, 5, 8, 5, 8, 6, 7, 6, 3,
         6, 7, 4, 7, 6, 5, 6, 6, 5, 5, 6, 5, 7, 7, 7, 6, 7, 6, 8, 7, 5, 6, 8, 7, 7, 6, 6, 8, 6, 6, 6, 6, 7, 8, 6, 6,
         8, 7, 6, 6, 7, 6, 6, 6, 7, 6, 8, 8, 9, 9, 9, 9, 7, 9, 8, 7, 9, 7, 7, 8, 8, 8, 7, 7, 7, 9, 9, 7, 8, 6, 9, 8,
         7, 8, 8, 7, 8, 8, 9, 8, 7, 7, 8, 7, 7, 7, 8, 9, 9, 7, 6, 6, 9, 7, 6, 8, 9, 8, 8, 8, 9, 7, 9, 6, 7, 8, 9,
         10, 8, 7, 9, 7, 8, 10, 7, 8, 10, 8, 10, 8, 7, 8, 10, 10, 7, 10, 8, 7, 9, 9, 9, 10, 7, 9, 9, 9, 8, 9, 10,
         10, 9, 10, 9, 7, 10, 9, 8, 11, 9, 9, 10, 8, 9, 9, 11, 11, 11, 9, 10, 11, 9, 9, 8, 10, 9, 9, 10, 11, 8, 12,
         10, 10, 10, 8, 9, 9, 10, 10, 9, 9, 9, 12, 10, 8, 9, 10, 11, 9, 10, 10, 10, 9, 8, 9, 9, 12, 9, 9, 8, 8, 8,
         8, 8, 9, 11, 9, 8, 8, 10, 10, 8, 8, 8, 9, 8, 7, 8, 8, 8, 9, 7, 10, 10, 7, 8, 9, 10, 7, 8, 9, 9, 6, 9, 9, 9,
         8, 8, 9, 8, 8, 9, 10, 9, 10, 9, 8, 9, 6, 7, 9, 8, 9, 9, 6, 8, 7, 7, 6, 8, 10, 9, 8, 7, 6, 7, 9, 8, 10, 9,
         6, 8, 8, 7, 9, 8, 10, 7, 6, 7, 10, 9, 8, 7, 8, 8, 7, 9, 9, 8, 9, 8, 6, 7, 7, 8, 8, 8, 8, 9, 9, 7, 9, 6, 8,
         8, 8, 6, 8, 7, 8, 7, 8, 8, 6, 8, 8, 6, 7, 8, 5, 7, 7, 8, 8, 8, 8, 7, 7, 7, 7, 8, 7, 6, 7, 6, 8, 5, 8, 7, 6,
         8, 8, 9, 8, 6, 7, 7, 7, 7, 8, 6, 7, 7, 7, 7, 6, 8, 7, 7, 6, 7, 7, 8, 7, 7, 7, 6, 8, 7, 7, 5, 6, 7, 8, 7, 5,
         5, 6, 6, 8, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 5, 7, 7, 6, 7, 6, 7, 6, 5, 7, 7, 6, 7, 7, 6, 7, 9, 6, 9, 7, 7, 8,
         7, 6, 6, 6, 6, 10, 8, 5, 9, 6, 6, 8, 7, 8, 7, 8, 8, 9, 9, 7, 8, 9, 6, 7, 8, 8, 7, 8, 8, 7, 7, 7, 8, 9, 8,
         7, 8, 8, 8, 7, 8, 8, 8, 9, 8, 8, 8, 10, 12, 7, 8, 10, 9, 7, 7, 7, 8, 10, 7, 8, 9, 8, 8, 7, 6, 8, 8, 9, 9,
         9, 9, 9, 9, 7, 9, 9, 8, 9, 10, 7, 9, 8, 10, 8, 9, 7, 8, 8, 10, 10, 8, 8, 8, 10, 9, 10, 10, 9, 9, 9, 10, 11,
         8, 7, 10, 9, 8, 9, 9, 12, 9, 10, 8, 10, 11, 9, 10, 10, 11, 9, 7, 10, 11, 10, 9, 10, 10, 9, 9, 7, 10, 9, 9,
         10, 9, 9, 8, 10, 8, 11, 8, 6, 8, 9, 8, 8, 10, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 8, 9, 10, 8, 9, 7, 9,
         7, 7, 9, 6, 8, 10, 9, 9, 7, 7, 8, 9, 9, 8, 9, 8, 6, 8, 7, 9, 8, 7, 8, 10, 9, 6, 7, 6, 9, 8, 9, 8, 8, 7, 8,
         8, 8, 8, 7, 7, 7, 8, 6, 9, 7, 6, 5, 8, 7, 8, 7, 8, 8, 8, 5, 8, 8, 7, 5, 8, 7, 8, 7, 7, 7, 5, 6, 7, 7, 7, 7,
         7, 5, 7, 7, 6, 6, 8, 6, 5, 6, 8, 7, 6, 7, 7, 6, 7, 6, 8, 6, 8, 7, 5, 6, 5, 7, 6, 5, 6, 8, 7, 5, 6, 4, 6, 5,
         6, 6, 8, 7, 5, 4, 6, 8, 4, 5, 7, 4, 7, 7, 6, 6, 5, 6, 6, 5, 5, 7, 6, 5, 5, 5, 7, 5, 5, 6, 8, 5, 5, 5, 6, 5,
         5, 6, 4, 5, 6, 6, 5, 2, 6, 5, 4, 4, 3, 5, 7, 6, 6, 5, 4, 5, 5, 7, 4, 3, 7, 5, 4, 6, 4, 5, 5, 4, 4, 6, 5, 4,
         3, 4, 4, 5, 5, 4, 3, 4, 4, 5, 5, 5, 5, 4, 4, 4, 4, 3, 4, 5, 3, 3, 5, 3, 4, 4, 5, 4, 4, 3, 4, 4, 5, 3, 5, 5,
         5, 4, 2, 4, 4, 3, 2, 3, 5, 5, 3, 4, 5, 2, 4, 3, 4, 1, 3, 2, 2, 4, 3, 3, 3, 3, 2, 3, 4, 2, 2, 3, 4, 2, 4, 0,
         3, 3, 3, 1, 2, 2, 3, 3, 2, 1, 2, 3, 3, 2, 2, 2, 1, 1, 1, 2, 2, 2, 3, 1, 1, 0, 2, 0, 1, 1, 3, 1, 0, 0, 0, 2,
         2, 3, 3, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 0, 2, 1, 2, 0, 1, 2, 0, 1, 0, 2, 0, 1, 2, 1, 1, 0,
         0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0]

    po_urah = [20, 34, 66, 82, 114, 125, 204, 272, 364, 453, 522,
               556, 494, 452, 407, 443, 514, 544, 464, 381, 317, 231, 118, 36]

    def test_1_statistika(self):
        self.assertEqual(list(self.po_urah), list(po_urah(self.a)))
        self.assertEqual(11, naj_ura(self.a))
        self.assertEqual(153, brez_prehodov(self.a))

    def test_2_obdobje_brez(self):
        #                                      0  1  2  3  4  5  6  7  8  9  0  1  2
        self.assertEqual((5, 8), obdobje_brez([0, 0, 1, 2, 3, 0, 0, 0, 0, 1, 2, 0, 0]))
        self.assertEqual((0, 2), obdobje_brez([0, 0, 0, 2, 3, 1, 2, 0, 0, 1, 2, 0, 0]))
        self.assertEqual((7, 12), obdobje_brez([0, 0, 0, 2, 3, 1, 2, 0, 0, 0, 0, 0, 0]))
        self.assertEqual((1421, 1436), obdobje_brez(self.a))

    def test_3_obremenitve(self):
        imena = ["Anina ulica", "Bertin trg", "Cilkina cesta", "Ulica Dani Beznikove"]
        porocila = [10, 2, 5, 10, 3, 5, 3, 4, 5, 2, 3, 4, 2, 1, 2, 6, 8, 1, 2, 3]
        self.assertEqual("Anina ulica", obremenitve(imena, porocila))

        porocila = [3, 5, 3, 4, 3, 6, 3, 4]
        self.assertEqual("Bertin trg", obremenitve(imena, porocila))

        imena = ["Anina ulica", "Bertin trg"]
        self.assertEqual("Bertin trg", obremenitve(imena, porocila))

        imena = list("abcdefghi")
        porocila = list(range(len(imena) * 5))
        self.assertEqual("i", obremenitve(imena, porocila))

    def test_4_zlata_minuta(self):
        self.assertTrue(zlata_minuta(42, self.a))
        self.assertFalse(zlata_minuta(420, self.a))
        self.assertTrue(zlata_minuta(421, self.a))
        self.assertTrue(zlata_minuta(1017, self.a))
        self.assertTrue(zlata_minuta(1018, self.a))
        self.assertTrue(zlata_minuta(952, self.a))
        self.assertTrue(zlata_minuta(953, self.a))
        self.assertFalse(zlata_minuta(1000, self.a))

    def test_5a_senzor(self):
        anina = Senzor(42)
        bertin = Senzor(55)

        anina.prehod("+")
        anina.prehod("+")
        anina.prehod("-")
        anina.prehod("+")
        bertin.prehod("+")

        self.assertEqual((3, 1), anina.prehodov())
        self.assertEqual((1, 0), bertin.prehodov())

    def test_5b_nadzorni_sistem(self):
        anina = Senzor(42)
        bertin = Senzor(55)
        cilkina = Senzor(66)

        nadzor = NadzorniSistem([anina, bertin, cilkina])
        nadzor.prehod(42, "+")
        nadzor.prehod(55, "-")
        nadzor.prehod(55, "+")
        nadzor.prehod(42, "+")
        nadzor.prehod(42, "+")
        nadzor.prehod(55, "-")
        anina.prehod("-")

        self.assertEqual((3, 1), nadzor.prehodov(42))
        self.assertEqual((1, 2), nadzor.prehodov(55))
        self.assertEqual((0, 0), nadzor.prehodov(66))

        self.assertEqual((3, 1), anina.prehodov())


if __name__ == "__main__":
    unittest.main()
