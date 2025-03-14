import unittest
import random
import warnings
import os



def skupne_povezave(pot1, pot2):
    prva = []
    resitev = []
    stevec = 0
    for x in zip(pot1, pot1[1:]):
        
        print (x)
        prva.append(x)
        
    for x in zip(pot2[:len(pot1)], pot2[1:len(pot1)]):
        if x == prva[stevec]:
            resitev.append(x)
        stevec += 1
            
            
    print(pot1, pot2)
    print(resitev)
    return len(resitev)


'''def skupne_povezave(pot1, pot2):
    resitev = []
    prva = list(zip(pot1, pot2[1:]))
    druga = list(zip(pot2, pot2[1:]))
    stevec = 0
    
    print(druga)
    for y in range(len(druga)):
        if prva[y] == (druga[y]):
            resitev.append(druga[y])
        stevec += 1
            
    print(pot1, pot2)
    print(resitev)
    return len(resitev)'''
    
def najzahtevnejse(zemljevid):
    seznam = {}
    resitev = 0
    rez = ""
    for (kljuc1, kljuc2), vescine in zemljevid.items():
        print(kljuc1,kljuc2, "  ", vescine)
        
        #for stvar in vescine:
        if kljuc1 in seznam:
            print(seznam)
            print(vescine)
            seznam[kljuc1].extend(vescine)
        else:
            seznam[kljuc1] = list(vescine)
            
        #for stvar in vescine:
        if kljuc2 in seznam:
            seznam[kljuc2].extend(vescine)
        else:
            seznam[kljuc2] = list(vescine)
            
        #print(zemljevid)
    print(seznam)
        
    for kljuc, stvar in seznam.items():
        print(stvar)
        edinstvene = set(stvar)
        if stvar:
            if len(edinstvene) > resitev:
                rez = kljuc
                resitev = len(edinstvene) 
                
    return rez



def preberi_zemljevid_povezav(ime_datoteke):
    slovar = {}
    t = open(ime_datoteke, mode = "r", encoding= "UTF-8")
    #print(t)

    
    for vrstica in t:
        print(vrstica)
        stvari, kljuci = vrstica.split(":")
        #print(stvari, ")))))", kljuci)
        
        for kljuc in kljuci.strip().split(", "):
            #print(kljuc)
            
            if kljuc in slovar:
                slovar[kljuc].append(stvari)
            else:
                slovar[kljuc] = [stvari]
                
    print(slovar)
    return slovar











A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R, S, T, U, V = "ABCDEFGHIJKLMNOPRSTUV"

proto_zemljevid = {
    (A, B): "gravel trava",
    (A, V): "pešci lonci",
    (B, C): "bolt lonci",
    (B, V): "",
    (C, R): "stopnice pešci lonci",
    (D, F): "stopnice pešci",
    (D, R): "pešci",
    (E, I): "trava lonci",
    (F, G): "trava črepinje",
    (G, H): "črepinje pešci",
    (G, I): "avtocesta",
    (H, J): "robnik bolt",
    (I, M): "avtocesta",
    (I, P): "gravel",
    (I, R): "stopnice robnik",
    (J, K): "",
    (J, L): "gravel bolt",
    (K, M): "stopnice bolt",
    (L, M): "robnik pešci",
    (M, N): "rodeo",
    (N, P): "gravel",
    (O, P): "gravel",
    (P, S): "",
    (R, U): "trava pešci",
    (R, V): "pešci lonci",
    (S, T): "robnik trava",
    (T, U): "gravel trava",
    (U, V): "robnik lonci trava"
}

zemljevid = {k: set(v.split()) for k, v in proto_zemljevid.items()} | {k[::-1]: set(v.split()) for k, v in
                                                                       proto_zemljevid.items()}


class Test(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def test_1_skupne_povezave(self):
        self.assertEqual(1, skupne_povezave("ABCDEF",
                                            "GHCDFI"))
        self.assertEqual(1, skupne_povezave("ABCDEFJKLM",
                                            "GHCDFI"))
        self.assertEqual(1, skupne_povezave("ABCDEF",
                                            "GHCDFIJKLM"))
        self.assertEqual(2, skupne_povezave("ABCDEFG",
                                            "GHCDIFG"))
        self.assertEqual(2, skupne_povezave("ABCDEFG",
                                            "GHCDIFGH"))
        self.assertEqual(2, skupne_povezave("ABCDEFGH",
                                            "GHCDIFG"))
        self.assertEqual(3, skupne_povezave("ABCDEFGH",
                                            "GHCDEMGH"))
        self.assertEqual(0, skupne_povezave("ABCDEFGH",
                                            "HABCDEFG"))
        self.assertEqual(0, skupne_povezave("ABCDEFGH",
                                            ""))
        self.assertEqual(0, skupne_povezave("ABCDABCD",
                                            "BCDABCDE"))
        self.assertEqual(3, skupne_povezave("ABCDABCD",
                                            "BCDEABCD"))
        self.assertEqual(7, skupne_povezave("ABCDABCD",
                                            "ABCDABCD"))

    def test_2_najzahtevnejse(self):
        self.assertIn(najzahtevnejse(zemljevid), "IM")
        self.assertEqual("A", najzahtevnejse({(A, B): {"gravel"},
                                              (A, C): {"trava"},
                                              (B, C): set(),
                                              (B, D): set(),
                                              (B, E): set()
                                              }))

    def test_3_preberi_zemljevid_povezav(self):
        vx = f"vescina{random.randint(0, 1000)}"
        kx = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(5))
        fname = f"zemljevid{random.randint(1000, 9999)}.txt"
        try:
            with open(fname, "wt") as f:
                f.write(f"""A-B: grava, travel, pesek
A-C: pesek
B-C: grava, crepinje, avtocesta
A-E: crepinje, pesci
A-F:
D-{kx}: {vx}
""")

            self.assertEqual({"grava": {(A, B), (B, C)},
                              "travel": {(A, B)},
                              "avtocesta": {(B, C)},
                              "pesek": {(A, B), (A, C)},
                              "crepinje": {(B, C), (A, E)},
                              "pesci": {(A, E)},
                              vx: {(D, kx)}
                              }, preberi_zemljevid_povezav(fname))
        finally:
            os.remove(fname)

    def test_4_stevilo_poti(self):
        self.assertEqual(1, stevilo_poti("A", "B", zemljevid))
        self.assertEqual(3, stevilo_poti("G", "N", zemljevid))
        self.assertEqual(4, stevilo_poti("A", "V", zemljevid))
        self.assertEqual(4, stevilo_poti("A", "V", zemljevid))

        self.assertEqual(2, stevilo_poti("R", "V", zemljevid))
        self.assertEqual(6, stevilo_poti("F", "V", zemljevid))
        self.assertEqual(8, stevilo_poti("D", "V", zemljevid))

    def test_5_kolesar(self):
        ana = Kolesar("A", zemljevid, {"gravel", "trava", "pešci", "lonci", "bolt"})

        self.assertEqual("A", ana.lokacija())
        ana.premik("B")
        self.assertEqual("B", ana.lokacija())
        ana.premik("A")
        self.assertEqual("A", ana.lokacija())
        ana.premik("V")
        self.assertEqual("V", ana.lokacija())
        ana.premik("R")
        self.assertEqual("R", ana.lokacija())
        ana.premik("C")  # pade po stopnicah!
        self.assertIsNone(ana.lokacija())
        ana.premik("B")  # leži pod stopnicami
        self.assertIsNone(ana.lokacija())
        ana.premik("A")  # še vedno leži pod stopnicami. In se ne premakne več.
        self.assertIsNone(ana.lokacija())

        berta = Kolesar("B", zemljevid,
                        {'avtocesta', 'gravel', 'lonci', 'pešci', 'robnik', 'rodeo', 'stopnice', 'trava', 'bolt'})

        self.assertEqual("B", berta.lokacija())
        berta.premik("A")
        self.assertEqual("A", berta.lokacija())
        berta.premik("V")
        self.assertEqual("V", berta.lokacija())
        berta.premik("R")
        self.assertEqual("R", berta.lokacija())
        berta.premik("C")
        self.assertEqual("C", berta.lokacija())
        berta.premik("B")
        self.assertEqual("B", berta.lokacija())
        berta.premik("A")
        self.assertEqual("A", berta.lokacija())
        berta.premik("C")  # iz A v C ni poti!
        self.assertIsNone(berta.lokacija())
        berta.premik("B")  # in še vedno leži pod cesto
        self.assertIsNone(berta.lokacija())

        # Ne zna nič in nima kaj voziti po Ljubljani
        polde = Kolesar("P", zemljevid, set())
        self.assertEqual("P", polde.lokacija())
        polde.premik("S")
        self.assertEqual("S", polde.lokacija())
        polde.premik("P")
        self.assertEqual("P", polde.lokacija())
        polde.premik("I")
        self.assertIsNone(polde.lokacija())
        polde.premik("P")
        self.assertIsNone(polde.lokacija())


if __name__ == "__main__":
    unittest.main()

