# Svojo rešitev pišite sem.
# Najboljše je, da pustite teste v datoteki z rašitvijo, da ne bi ponesreči pobrisali preveč.

def unzip(s, sirina):
    prejsni_znak = ""
    vrstica = ""
    rezultat = []
    for znak in s:
        if znak == "<" or znak == ">" or znak == "v" or znak == "^":
            if sirina == len(vrstica):
                rezultat.append(vrstica)
                vrstica = ""
            prejsni_znak = znak
            vrstica += znak
        else:
            #print(f"znak: {znak}")
            for ponovitev in range(int(znak)):
                if sirina == len(vrstica):
                    rezultat.append(vrstica)
                    vrstica = ""
                
                vrstica += prejsni_znak
    
    rezultat.append(vrstica)
    print(rezultat)
    return rezultat


def pred_ciklom(zemljevid, x ,y):
    while pomozna(zemljevid, (x,y)) == None:
        print("asokdfjalsdfjal")
        if zemljevid[y][x] == ">":
            x+=1
            print(x, y)
        elif zemljevid[y][x] == "<":
            x-=1
            print(x, y)
        elif zemljevid[y][x] == "^":
            y-=1
            print(x, y)
        elif zemljevid[y][x] == "v":
            y+=1
            print(x, y)

rezultat = []
rezultat2 = set()  
    
def pomozna(zemljevid, polje):

    
    rezultat.append(polje)
    rezultat2.add(polje)
    
    print(rezultat, rezultat2)
    
    if list(rezultat2) != rezultat:
        return rezultat2


    
    
            








import unittest

sneg = """
>>v>>v
vvv^<<
>>>>v^
^^<>>v
>^<<<<""".strip().splitlines()

pred_ciklom(sneg, 0, 0)


class Test(unittest.TestCase):
    def test_01_unzip(self):
        #self.assertEqual(["<^<<vvvv"], unzip("<^<<vvvv", 8))
        self.assertEqual(["<^<<", "vvvv"], unzip("<^<<vvvv", 4))
        self.assertEqual(["<^<<", "vvvv"], unzip("<^<<v3", 4))
        self.assertEqual(sneg, unzip(">1v>1v3^<1>3v^2<>>v>^<3", 6))

        self.assertEqual([">" * 4] * 3, unzip(">56", 4))

    def test_02_pred_ciklom(self):
        self.assertEqual(4, pred_ciklom(sneg, 0, 0))
        self.assertEqual(3, pred_ciklom(sneg, 1, 0))
        self.assertEqual(2, pred_ciklom(sneg, 2, 0))
        self.assertEqual(1, pred_ciklom(sneg, 2, 1))
        self.assertEqual(0, pred_ciklom(sneg, 2, 2))

        self.assertEqual(1, pred_ciklom(sneg, 1, 1))
        self.assertEqual(0, pred_ciklom(sneg, 1, 2))
        self.assertEqual(0, pred_ciklom(sneg, 2, 2))
        self.assertEqual(0, pred_ciklom(sneg, 3, 2))

        self.assertEqual(1, pred_ciklom(sneg, 0, 2))
        self.assertEqual(2, pred_ciklom(sneg, 0, 3))

        self.assertEqual(1, pred_ciklom(sneg, 0, 4))

        self.assertEqual(0, pred_ciklom(sneg, 3, 0))
        self.assertEqual(1, pred_ciklom(sneg, 5, 2))

        self.assertEqual(4, pred_ciklom([">>>>><"], 0, 0))

    def test_03_polja_do(self):
        self.assertEqual({(0, 0)},
                         polja_do(sneg, 0, 0))
        self.assertEqual({(0, 1), (0, 2), (0, 3)},
                         polja_do(sneg, 0, 2))
        self.assertEqual({(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (2, 1), (4, 3), (5, 4), (0, 2), (2, 2), (1, 0), (3, 2), (1, 3), (4, 4), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (4, 2), (2, 3), (3, 3), (5, 3)},
                         polja_do(sneg, 1, 2))
        self.assertEqual({(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (2, 1), (4, 3), (5, 4), (0, 2), (2, 2), (1, 0), (3, 2), (1, 3), (4, 4), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (4, 2), (2, 3), (3, 3), (5, 3)},
                         polja_do(sneg, 1, 3))

    def test_04_polja_do_rek(self):
        self.assertEqual({(0, 0)},
                         polja_do_rek(sneg, 0, 0, set()))
        self.assertEqual({(0, 1), (0, 2), (0, 3)},
                         polja_do_rek(sneg, 0, 2, set()))
        self.assertEqual({(0, 1), (0, 2)},
                         polja_do_rek(sneg, 0, 2, {(0, 3)}))
        self.assertEqual({(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (2, 1), (4, 3), (5, 4), (0, 2), (2, 2), (1, 0), (3, 2), (1, 3), (4, 4), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (4, 2), (2, 3), (3, 3), (5, 3)},
                         polja_do_rek(sneg, 1, 2, set()))
        self.assertEqual({(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (2, 1), (4, 3), (5, 4), (0, 2), (2, 2), (1, 0), (3, 2), (1, 3), (4, 4), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (4, 2), (2, 3), (3, 3), (5, 3)},
                         polja_do_rek(sneg, 1, 3, set()))

    def test_05_plug(self):
        zemljevid = sneg.copy()
        plug1 = Plug(zemljevid, 0, 0)
        plug2 = Plug(zemljevid, 2, 0)
        plug3 = Plug(zemljevid, 1, 4)

        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(0, plug3.ociscenih())

        plug2.premik("<")
        self.assertEqual((1, 0), plug2.lokacija())
        self.assertEqual(1, plug2.ociscenih())

        plug2.premik("v")
        self.assertEqual((1, 1), plug2.lokacija())
        self.assertEqual(2, plug2.ociscenih()) # očistil je polje (1, 1)

        plug2.premik("v")
        self.assertEqual((1, 2), plug2.lokacija())
        self.assertEqual(3, plug2.ociscenih())

        plug1.premik("v")
        self.assertEqual((0, 1), plug1.lokacija())
        self.assertEqual(1, plug1.ociscenih())

        plug1.premik(">")
        self.assertEqual((1, 1), plug1.lokacija())
        self.assertEqual(2, plug1.ociscenih())  # očistil je polje (0, 1)

        plug1.premik(">")
        self.assertEqual((2, 1), plug1.lokacija())
        self.assertEqual(2, plug1.ociscenih())  # ni očistil polja (1, 1), ker ga je pred njim že plug2

        plug1.premik(">")
        self.assertEqual((3, 1), plug1.lokacija())
        self.assertEqual(3, plug1.ociscenih())  # očistil je polje (2, 1)

        plug3.premik("<")
        self.assertEqual((0, 4), plug3.lokacija())
        self.assertEqual(1, plug3.ociscenih())  # očistil je polje (1, 4)

        plug3.premik(">")
        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())  # očistil je polje (0, 4)

        plug3.premik("<")
        self.assertEqual((0, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())  # (1, 4) je bilo že čisto

        plug3.premik(">")
        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())  # (0, 4) tudi

        plug3.premik("v")  # zapelje ven: ignoriramo naslednje tri ukaze
        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())  # (0, 4) tudi

        plug3.premik("^")  # ignoriramo
        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())

        plug3.premik("^")  # ignoriramo
        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())

        plug2.premik("v")
        self.assertEqual((1, 3), plug2.lokacija())  # plug 2 očisti (1, 2)
        self.assertEqual(4, plug2.ociscenih())

        plug2.premik("v")
        self.assertEqual((1, 4), plug2.lokacija())  # plug 2 očisti (1, 3)
        self.assertEqual(5, plug2.ociscenih())

        plug2.premik(">")
        self.assertEqual((2, 4), plug2.lokacija())  # ne očisti (1, 4), ker ga je že plug 3
        self.assertEqual(5, plug2.ociscenih())

        plug3.premik("^")  # ignoriramo
        self.assertEqual((1, 4), plug3.lokacija())
        self.assertEqual(2, plug3.ociscenih())

        plug3.premik("^")  # ne ignoriramo ...
        self.assertEqual((1, 3), plug3.lokacija())  # vendar ne očisti (1, 4), ker ga je že prej
        self.assertEqual(2, plug3.ociscenih())

        plug3.premik("<")  # ne ignoriramo ...
        self.assertEqual((0, 3), plug3.lokacija())  # vendar ne očisti (1, 3), ker ga je že plug 2
        self.assertEqual(2, plug3.ociscenih())

        plug3.premik(">")
        self.assertEqual((1, 3), plug3.lokacija())
        self.assertEqual(3, plug3.ociscenih())  # očisti (0, 3)


if __name__ == "__main__":
    unittest.main()
