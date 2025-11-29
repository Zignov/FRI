import unittest

class Kolesar:
    def __init__(self, vrstica, stolpec, zemljevid):
        self.vrstica = vrstica
        self.stolpec = stolpec
        self.zemljevid = zemljevid
        self.trdozivost = 1
        self.kilometrina = 0
        self.polja = {(self.vrstica, self.stolpec)}
        self.pot_cela = []
        
    def lokacija(self):
        #print(f"vrstica: {self.vrstica}, stolpec: {self.stolpec}")
        return (self.vrstica, self.stolpec)
        

    def premik(self, smer):
        if self.trdozivost >= 1:
            if smer == ">":
                #print("Desno")
                nova_pozicija = (self.vrstica, self.stolpec+1)
                if nova_pozicija not in self.zemljevid:
                    self.stolpec += 1
                    self.kilometrina += 1
                    self.polja.add(self.lokacija())
                    self.pot_cela.append(smer)
                else:
                    self.trdozivost -= 1
                    
            if smer == "<":
                #print("Levo")
                nova_pozicija = (self.vrstica, self.stolpec-1)
                if nova_pozicija not in self.zemljevid:
                    self.stolpec -= 1
                    self.kilometrina += 1
                    self.polja.add(self.lokacija())
                    self.pot_cela.append(smer)
                else:
                    self.trdozivost -= 1                    
            if smer == "v":
                #print("Dol")
                nova_pozicija = (self.vrstica+1, self.stolpec)
                if nova_pozicija not in self.zemljevid:
                    self.vrstica += 1
                    self.kilometrina += 1
                    self.polja.add(self.lokacija())
                    self.pot_cela.append(smer)
                else:
                    self.trdozivost -= 1                    
            if smer == "^":
                #print("Gor")
                nova_pozicija = (self.vrstica-1, self.stolpec)
                if nova_pozicija not in self.zemljevid:
                    self.vrstica -= 1
                    self.kilometrina += 1
                    self.polja.add(self.lokacija())
                    self.pot_cela.append(smer)
                else:
                    self.trdozivost -= 1                    
                    
    def prevozi(self, pot):
        #print(zip(pot))
        for dolzina, ukaz in zip(pot[::2], pot[1::2]):
            #print(dolzina, ukaz)
            for x in range(int(dolzina)):
                self.premik(ukaz)
                

    def razdalja(self):
        return(self.kilometrina)
    
    def obiskana_polja(self):
        return self.polja
    
    def pot(self):
        rezultat = ""
        if self.pot_cela:
            trenutno = self.pot_cela[0]
        else:
            return(rezultat)
        stevec = 0
        
        for ukaz in self.pot_cela:
            if (ukaz in trenutno) and stevec < 9:
                stevec+=1
                
            else:
                rezultat += f"{stevec}{trenutno}"
                trenutno = ukaz
                stevec = 1
                
        rezultat += f"{stevec}{trenutno}"
        return(rezultat)
    
    
    

    

        
        
            
            
            





class Test(unittest.TestCase):
    def setUp(self):
        self.zemljevid =  {(2, 4), (2, 11), (2, 12), (2, 13),
                           (4, 2), (4, 10),
                           (5, 2), (5, 8),
                           (6, 7),
                           (7, 1),
                           (8, 4), (8, 5), (8, 6),
                           (9, 2),
                           (10, 6), (10, 11),
                           (11, 3), (11, 10),
                           (12, 4), (12, 11),
                           (13, 7), (13, 12)}

class Test06(Test):
    def test_Kolesar_premik_lokacija(self):
        zemljevid = self.zemljevid.copy()
        ana = Kolesar(11, 11, zemljevid)
        berta = Kolesar(5, 7, zemljevid)

        self.assertEqual((11, 11), ana.lokacija())
        ana.premik(">")
        self.assertEqual((11, 12), ana.lokacija())
        ana.premik("^")
        self.assertEqual((10, 12), ana.lokacija())
        ana.premik("^")
        self.assertEqual((9, 12), ana.lokacija())
        ana.premik("<")
        self.assertEqual((9, 11), ana.lokacija())
        ana.premik("<")
        self.assertEqual((9, 10), ana.lokacija())
        ana.premik("v")
        self.assertEqual((10, 10), ana.lokacija())
        ana.premik(">")  # Obleži
        self.assertEqual((10, 10), ana.lokacija())
        ana.premik("<")  # še vedno leži
        self.assertEqual((10, 10), ana.lokacija())

        self.assertEqual((5, 7), berta.lokacija())
        berta.premik("^")
        self.assertEqual((4, 7), berta.lokacija())

    def test_Kolesar_prevozi(self):
        ana = Kolesar(4, 6, self.zemljevid.copy())
        ana.prevozi("2^3>")
        self.assertEqual((2, 9), ana.lokacija())
        ana.prevozi("7v6<1^1<5>4v")
        self.assertEqual((8, 3), ana.lokacija())


class Test07(Test):
    def test_Kolesar_razdalja_pot_obiskano(self):
        zemljevid = self.zemljevid.copy()
        ana = Kolesar(11, 11, zemljevid)
        berta = Kolesar(5, 7, zemljevid)

        self.assertEqual((11, 11), ana.lokacija())
        self.assertEqual(0, ana.razdalja())
        self.assertEqual({(11, 11)}, ana.obiskana_polja())
        self.assertEqual("", ana.pot())

        ana.premik(">")
        self.assertEqual((11, 12), ana.lokacija())
        self.assertEqual(1, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12)}, ana.obiskana_polja())
        self.assertEqual("1>", ana.pot())

        ana.premik("^")
        self.assertEqual((10, 12), ana.lokacija())
        self.assertEqual(2, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12)}, ana.obiskana_polja())
        self.assertEqual("1>1^", ana.pot())

        ana.premik("^")
        self.assertEqual((9, 12), ana.lokacija())
        self.assertEqual(3, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12), (9, 12)}, ana.obiskana_polja())
        self.assertEqual("1>2^", ana.pot())

        ana.premik("<")
        self.assertEqual((9, 11), ana.lokacija())
        self.assertEqual(4, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12), (9, 12), (9, 11)}, ana.obiskana_polja())
        self.assertEqual("1>2^1<", ana.pot())

        ana.premik("<")
        self.assertEqual((9, 10), ana.lokacija())
        self.assertEqual(5, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12), (9, 12), (9, 11), (9, 10)}, ana.obiskana_polja())
        self.assertEqual("1>2^2<", ana.pot())

        ana.premik("v")
        self.assertEqual((10, 10), ana.lokacija())
        self.assertEqual(6, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12), (9, 12), (9, 11), (9, 10), (10, 10)}, ana.obiskana_polja())
        self.assertEqual("1>2^2<1v", ana.pot())

        ana.premik(">")  # Obleži
        self.assertEqual((10, 10), ana.lokacija())
        self.assertEqual(6, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12), (9, 12), (9, 11), (9, 10), (10, 10)}, ana.obiskana_polja())
        self.assertEqual("1>2^2<1v", ana.pot())

        ana.premik("<")  # še vedno leži
        self.assertEqual((10, 10), ana.lokacija())
        self.assertEqual(6, ana.razdalja())
        self.assertEqual({(11, 11), (11, 12), (10, 12), (9, 12), (9, 11), (9, 10), (10, 10)}, ana.obiskana_polja())
        self.assertEqual("1>2^2<1v", ana.pot())

        self.assertEqual((5, 7), berta.lokacija())
        self.assertEqual(0, berta.razdalja())
        self.assertEqual({(5, 7)}, berta.obiskana_polja())
        self.assertEqual("", berta.pot())

        berta.premik("^")
        self.assertEqual((4, 7), berta.lokacija())
        self.assertEqual(1, berta.razdalja())
        self.assertEqual({(5, 7), (4, 7)}, berta.obiskana_polja())
        self.assertEqual("1^", berta.pot())

    def test_Kolesar_prevozi(self):
        ana = Kolesar(4, 6, self.zemljevid.copy())
        ana.prevozi("2^1>")
        self.assertEqual((2, 7), ana.lokacija())
        self.assertEqual(3, ana.razdalja())
        self.assertEqual({(4, 6), (3, 6), (2, 6), (2, 7)}, ana.obiskana_polja())
        self.assertEqual("2^1>", ana.pot())

        ana.prevozi("2>7v6<1^1<5>4v")
        self.assertEqual((8, 3), ana.lokacija())
        self.assertEqual(21, ana.razdalja())
        self.assertEqual({(4, 9), (4, 6), (9, 5), (8, 3), (8, 9), (9, 8), (2, 8),
                          (3, 9), (3, 6), (5, 9), (8, 2), (9, 7), (9, 4), (2, 7),
                          (7, 9), (9, 3), (9, 9), (9, 6), (2, 9), (2, 6), (6, 9)},
                         ana.obiskana_polja())
        self.assertEqual("2^3>7v6<1^1<1>", ana.pot())

        cilka = Kolesar(2, 1, self.zemljevid.copy())
        cilka.prevozi("1^5>")
        self.assertEqual((1, 6), cilka.lokacija())
        self.assertEqual(6, cilka.razdalja())
        self.assertEqual({(2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)},
                            cilka.obiskana_polja())
        self.assertEqual("1^5>", cilka.pot())

        cilka.prevozi("7>")
        self.assertEqual((1, 13), cilka.lokacija())
        self.assertEqual(13, cilka.razdalja())
        self.assertEqual({(2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
                          (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13)},
                         cilka.obiskana_polja())
        self.assertEqual("1^9>3>", cilka.pot())


class Test08(Test):
    def test_0_dedovanje(self):
        for metoda in ("prevozi", "lokacija", "razdalja", "pot", "obiskana_polja"):
            for clsname in ("Kolesar", "Trdozivec", "Duh", "Eksplozivec"):
                cls = globals().get(clsname)
                if cls is None:
                    continue
                self.assertIs(getattr(Kolesar, metoda), getattr(cls, metoda),
                              f"Demšar ne vidi potrebe, da bi imela Kolesar in {clsname} vsak svojo metodo {metoda}")

    def test_Duh(self):
        ana = Duh(10, 2, self.zemljevid.copy())
        ana.premik("^")
        self.assertEqual((8, 2), ana.lokacija())
        self.assertEqual(2, ana.razdalja())
        self.assertEqual({(10, 2), (9, 2), (8, 2)}, ana.obiskana_polja())
        self.assertEqual("2^", ana.pot())

        ana.prevozi("4>")
        self.assertEqual((8, 9), ana.lokacija())
        self.assertEqual(9, ana.razdalja())
        self.assertEqual({(10, 2), (9, 2), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9)},
                            ana.obiskana_polja())
        self.assertEqual("2^7>", ana.pot())

    def test_Trdozivec(self):
        zemljevid = self.zemljevid.copy()
        ana = Trdozivec(7, 5, zemljevid, 2)
        ana.prevozi("1v")  #  Preživi trk
        self.assertEqual((7, 5), ana.lokacija())
        self.assertEqual(0, ana.razdalja())
        self.assertEqual({(7, 5)}, ana.obiskana_polja())
        self.assertEqual("", ana.pot())

        ana.premik(">")  #  ... in se še vedno premika
        self.assertEqual((7, 6), ana.lokacija())
        self.assertEqual(1, ana.razdalja())
        self.assertEqual({(7, 5), (7, 6)}, ana.obiskana_polja())
        self.assertEqual("1>", ana.pot())

        ana.prevozi("1v")  #  Obleži
        self.assertEqual((7, 6), ana.lokacija())
        self.assertEqual(1, ana.razdalja())
        self.assertEqual({(7, 5), (7, 6)}, ana.obiskana_polja())
        self.assertEqual("1>", ana.pot())

        ana.premik(">")  #  ... in se še vedno premika
        self.assertEqual((7, 6), ana.lokacija())
        self.assertEqual(1, ana.razdalja())
        self.assertEqual({(7, 5), (7, 6)}, ana.obiskana_polja())
        self.assertEqual("1>", ana.pot())

        berta = Trdozivec(7, 5, zemljevid, 5)
        berta.prevozi("2v")  # izgubi dve življenji
        self.assertEqual((7, 5), berta.lokacija())
        self.assertEqual(0, berta.razdalja())
        berta.prevozi("1^3>1^")  # izgubi še dve življenji
        self.assertEqual((5, 6), berta.lokacija())
        berta.prevozi("2>1^")  # obleži, ignorira zadnji premik
        self.assertEqual((5, 7), berta.lokacija())

    def test_Eksplozivec(self):
        zemljevid = self.zemljevid.copy()
        ana = Eksplozivec(10, 2, zemljevid)
        berta = Kolesar(10, 2, zemljevid)
        cilka = Kolesar(10, 2, zemljevid)

        cilka.prevozi("2^")  # Cilka ne more gor
        self.assertEqual((10, 2), cilka.lokacija())
        self.assertEqual(0, cilka.razdalja())

        ana.premik("^")  # Ana razstreli oviro, slava Ani!
        self.assertEqual((9, 2), ana.lokacija())
        self.assertEqual(1, ana.razdalja())
        self.assertEqual({(10, 2), (9, 2)}, ana.obiskana_polja())
        self.assertEqual("1^", ana.pot())

        berta.prevozi("2^")  # Berta je preživela, ker je Ana razstrelila oviro
        self.assertEqual((8, 2), berta.lokacija())
        self.assertEqual(2, berta.razdalja())
        self.assertEqual({(10, 2), (9, 2), (8, 2)}, berta.obiskana_polja())
        self.assertEqual("2^", berta.pot())

        cilka.prevozi("2^")  # Cilka pa še kar leži
        self.assertEqual((10, 2), cilka.lokacija())
        self.assertEqual(0, cilka.razdalja())
        self.assertEqual({(10, 2)}, cilka.obiskana_polja())
        self.assertEqual("", cilka.pot())

class Test09A(Test08):
    def setUp(self):
        super().setUp()
        self.zemljevid = Ovire(self.zemljevid)

    def test_Ovira(self):
        ovire = Ovire({(1, 1), (2, 4)})
        ovire.discard((1, 1))
        self.assertTrue((1, 1) in ovire)
        ovire.discard((2, 4))
        self.assertTrue((2, 4) in ovire)
        ovire.discard((1, 1))
        self.assertTrue((1, 1) in ovire)
        ovire.discard((1, 1))
        self.assertFalse((1, 1) in ovire)
        self.assertTrue((2, 4) in ovire)
        ovire.discard((1, 1))
        self.assertFalse((1, 1) in ovire)

    def test_Eksplozivec(self):
        zemljevid = self.zemljevid
        ana = Eksplozivec(10, 2, zemljevid)
        berta = Kolesar(10, 2, zemljevid)
        cilka = Kolesar(10, 2, zemljevid)
        dani = Kolesar(9, 1, zemljevid)

        cilka.prevozi("2^")  # Cilka ne more gor
        self.assertEqual((10, 2), cilka.lokacija())
        self.assertEqual(0, cilka.razdalja())

        ana.premik("^")  # Ana načne oviro, vendar je ne dokonča
        self.assertEqual((10, 2), ana.lokacija())
        self.assertEqual(0, ana.razdalja())

        berta.prevozi("1^")  # Berta ne more gor in obleži
        self.assertEqual((10, 2), berta.lokacija())
        self.assertEqual(0, berta.razdalja())

        ana.prevozi("4^")  # Ana nažge oviro še štirikrat: prvič se ne zgodi nič, nato se trikrat premakne
        self.assertEqual((7, 2), ana.lokacija())
        self.assertEqual(3, ana.razdalja())

        dani.prevozi("2>")  # Dani ima prosto pot
        self.assertEqual((9, 3), dani.lokacija())
        self.assertEqual(2, dani.razdalja())

        cilka.prevozi("2^")  # Cilka pa še kar leži
        self.assertEqual((10, 2), cilka.lokacija())
        self.assertEqual(0, cilka.razdalja())


if __name__ == '__main__':
    unittest.main()
