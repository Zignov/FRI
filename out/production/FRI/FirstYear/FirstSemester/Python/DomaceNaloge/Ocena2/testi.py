

import unittest
import warnings


def preberi_zapis(zapis):
    cas = int(zapis.split()[0][1:-1])
    stevilka = int(zapis.split()[2][:-1])
    akcija = ""
    kdo = None
    rezultat = None
    
    if "prejem" in zapis:
        akcija = "prejem"
        
    elif "odgovori" in zapis:
        akcija = "odgovori"
        kdo = ((zapis.split(":")[1]).split()[0]).strip()
        rezultat = zapis.split(":")[2].strip()

    elif "prepusti" in zapis:
        akcija = "prepusti"
        kdo = ((zapis.split(":")[1]).split()[0]).strip()
        rezultat = zapis.split(":")[2].strip()

    #print("Test:", (zapis.split(":")[1]).split()[0])
    return(cas, stevilka, akcija, kdo, rezultat)


def preberi_dnevnik(ime_datoteke):
    dnevnik = []
    datoteka = open(ime_datoteke, "r", encoding="utf-8")
    for vrstica in datoteka:
        dnevnik.append(preberi_zapis(vrstica))
        
    return dnevnik


def strni(dnevnik):
    rezultat = {}

    for zapis in dnevnik:
        cas, stevilka, akcija, kdo, rezultat_zapisa = zapis
        if stevilka not in rezultat:
            rezultat[stevilka] = [] 
            
        rezultat[stevilka].append((cas, akcija, kdo, rezultat_zapisa))

    max_pobuda = max(rezultat.keys(), default=0)
    rezultat_list = [None] * (max_pobuda + 1)
    
    for stevilka, akcije in rezultat.items():
        rezultat_list[stevilka] = akcije
        
    return rezultat_list


def casi(dnevnik):
    rezultat = {}

    for zapis in dnevnik:
        cas, stevilka, akcija, kdo, rezultat_zapisa = zapis
        if stevilka not in rezultat:
            rezultat[stevilka] = [] 
        
        rezultat[stevilka].append(cas)
        
    for stevilka, cas in rezultat.items():
        rezultat[stevilka] = max(cas) - min(cas)
        
    return rezultat


def hitro(dnevnik, meja):
    sum = 0
    for cas in casi(dnevnik).values():
        if cas <= meja:
            sum += 1
    return sum


def najtezji_primer(dnevnik):
    #print(casi(dnevnik))
    trenutna = 0
    rezultat = 0
    for stvar in casi(dnevnik).items():
        if stvar[1] > trenutna:
            trenutna = stvar[1]
            rezultat = stvar[0]
    return rezultat


def podrejeni(dnevnik):
    rezultat = {}
    for _, _, akcija, kdo, rezultat_zapisa in dnevnik:
        if akcija == "prepusti":
            if kdo not in rezultat:
                rezultat[kdo] = set()
            rezultat[kdo].add(rezultat_zapisa)
    return rezultat

class Test(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def assertDictAlmostEqual(self, a, b):
        self.assertEqual(set(a), set(b))
        for k in a:
            self.assertAlmostEqual(a[k], b[k])


class Test06(Test):
    def test_01_preberi_zapis(self):
        self.assertEqual(
            (720, 126, "prejem", None, None),
            preberi_zapis("[720] Pobuda 126: prejem")
        )
        self.assertEqual(
            (725, 86, "odgovori", "Ema", "Ureditev bomo reševali celostno."),
            preberi_zapis("[725] Pobuda 86: Ema odgovori: Ureditev bomo reševali celostno.")
        )
        self.assertEqual(
            (727, 114, "prepusti", "Zofka", "Johanca"),
            preberi_zapis("[727] Pobuda 114: Zofka prepusti: Johanca")
        )
        self.assertEqual(
            (66, 1, "odgovori", "Cilka", "Problem bomo preučili in ukrepali skladno s pristojnostmi."),
            preberi_zapis("[66] Pobuda 1: Cilka odgovori: Problem bomo preučili in ukrepali skladno s pristojnostmi.")
        )

    def test_02_preberi_dnevnik(self):
        dnevnik = preberi_dnevnik("odgovori.txt")
        self.assertEqual(6262, len(dnevnik))
        self.assertEqual(set(range(1, 2024)), {d[1] for d in dnevnik})
        self.assertEqual((10, 1, 'prejem', None, None), dnevnik[0])
        self.assertEqual((12243, 2004, 'odgovori', 'Urša',
                          'Problem bomo preučili in ukrepali skladno s pristojnostmi.') ,
                         dnevnik[6261])
        self.assertEqual((117, 17, 'prepusti', 'Zofka', 'Johanca'), dnevnik[42])

        dnevnik = preberi_dnevnik("odgovori-manjsi.txt")
        self.assertEqual(31, len(dnevnik))
        self.assertEqual(set(range(1, 10)), {d[1] for d in dnevnik})
        self.assertEqual((1059, 1, 'prejem', None, None), dnevnik[0])
        self.assertEqual((9355, 6, 'odgovori', 'Fanči', 'Hvala za komentar.'), dnevnik[20])

    def test_03_strni(self):
        dnevnik = preberi_dnevnik("odgovori-manjsi.txt")
        self.assertEqual([None,
                         [(1059, 'prejem', None, None),
                          (1099, 'prepusti', 'Zofka', 'Johanca'),
                          (1141, 'odgovori', 'Johanca',
                           'Problem bomo preučili in ukrepali skladno s pristojnostmi.')],
                         [(3032, 'prejem', None, None),
                          (3092, 'prepusti', 'Tina', 'Urša'),
                          (3138, 'odgovori', 'Urša', 'Predlagana sprememba ni v načrtu.')],
                         [(5191, 'prejem', None, None),
                          (5278, 'prepusti', 'Angelca', 'Berta'),
                          (5381, 'odgovori', 'Berta', 'Predlagana sprememba ni v načrtu.')],
                         [(8329, 'prejem', None, None),
                          (8407, 'prepusti', 'Cilka', 'Micka'),
                          (8479, 'prepusti', 'Micka', 'Petra'),
                          (8569, 'odgovori', 'Petra',
                           'Problem bomo preučili in ukrepali skladno s pristojnostmi.')]
                        ],
                         strni(dnevnik)[:5])

        dnevnik = preberi_dnevnik("odgovori.txt")
        pobude = strni(dnevnik)
        self.assertEqual(2024, len(pobude))
        self.assertIsNone(pobude[0])
        self.assertEqual(
            [(657, 'prejem', None, None),
             (742, 'odgovori', 'Klara',
              'Problem bomo preučili in ukrepali skladno s pristojnostmi.')],
             pobude[117]
        )
        self.assertEqual(
            [(554, 'prejem', None, None),
             (638, 'prepusti', 'Angelca', 'Fanči'),
             (718, 'odgovori', 'Fanči', 'Hvala za komentar.')],
            pobude[101]
        )
        self.assertEqual(
            [(11867, 'prejem', None, None),
             (11940, 'prepusti', 'Cilka', 'Helga'),
             (11998, 'prepusti', 'Helga', 'Nina'),
             (12076, 'odgovori', 'Nina', 'Ureditev bomo reševali celostno.')],
            pobude[2000]
        )

    def test_04_casi(self):
        dnevnik = preberi_dnevnik("odgovori-manjsi.txt")
        self.assertEqual(
            {1: 82, 2: 106, 3: 190, 4: 240, 5: 235, 6: 186, 7: 205, 8: 46, 9: 155},
            casi(dnevnik)
        )

class TestD(Test):
    @classmethod
    def setUpClass(cls):
        cls.manjsi = preberi_dnevnik("odgovori-manjsi.txt")
        cls.dnevnik = preberi_dnevnik("odgovori.txt")

class Test07(TestD):
    def test_01_hitro(self):
        self.assertEqual(1, hitro(self.manjsi, 50))
        self.assertEqual(2, hitro(self.manjsi, 100))
        self.assertEqual(6, hitro(self.manjsi, 200))
        self.assertEqual(9, hitro(self.manjsi, 1000))

        self.assertEqual(0, hitro(self.dnevnik, 10))
        self.assertEqual(3, hitro(self.dnevnik, 40))
        self.assertEqual(305, hitro(self.dnevnik, 80))

    def test_02_najtezji_primer(self):
        self.assertEqual(4, najtezji_primer(self.manjsi))
        self.assertEqual(501, najtezji_primer(self.dnevnik))

    def test_03_podrejeni(self):
        self.assertEqual(
            {'Angelca': {'Fanči', 'Berta'},
             'Cilka': {'Klara', 'Micka'},
             'Johanca': {'Fanči'},
             'Klara': {'Nina', 'Micka'},
             'Micka': {'Nina', 'Petra'},
             'Tina': {'Urša'},
             'Zofka': {'Angelca', 'Johanca'}},
            podrejeni(self.manjsi)
        )

        self.assertEqual(
            {'Angelca': {'Cilka', 'Dani', 'Berta', 'Fanči'},
             'Cilka': {'Klara', 'Micka', 'Helga'},
             'Dani': {'Iva', 'Jana', 'Tina'},
             'Helga': {'Nina', 'Petra', 'Olga'},
             'Johanca': {'Fanči', 'Ema', 'Helga'},
             'Klara': {'Nina', 'Jana', 'Micka'},
             'Micka': {'Nina', 'Petra', 'Olga'},
             'Tina': {'Urša'},
             'Zofka': {'Johanca', 'Angelca'}},
            podrejeni(self.dnevnik)
        )

class Test08(TestD):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def test_01_razmerje(self):
        self.assertEqual({'Angelca': 0.0,
            'Berta': 1.0,
            'Cilka': 0.0,
            'Fanči': 1.0,
            'Helga': 1.0,
            'Johanca': 0.5,
            'Klara': 0.0,
            'Micka': 0.0,
            'Nina': 1.0,
            'Petra': 1.0,
            'Tina': 0.0,
            'Urša': 1.0,
            'Zofka': 0.0}, razmerje(self.manjsi))

        self.assertDictEqual({
            'Angelca': 0.4013986013986014,
            'Berta': 1.0,
            'Cilka': 0.20448877805486285,
            'Dani': 0.36507936507936506,
            'Ema': 1.0,
            'Fanči': 1.0,
            'Helga': 0.3319672131147541,
            'Iva': 1.0,
            'Jana': 1.0,
            'Johanca': 0.41203703703703703,
            'Klara': 0.4110169491525424,
            'Micka': 0.3644067796610169,
            'Nina': 1.0,
            'Olga': 1.0,
            'Petra': 1.0,
            'Tina': 0.2,
            'Urša': 1.0,
            'Zofka': 0.0}, razmerje(self.dnevnik))

    def test_02_natancnost(self):
        self.assertDictAlmostEqual({
           'Angelca': 81.5,
           'Berta': 103.0,
           'Cilka': 89.0,
           'Fanči': 83.5,
           'Helga': 46.0,
           'Johanca': 46.0,
           'Klara': 57.0,
           'Micka': 82.5,
           'Nina': 41.5,
           'Petra': 90.0,
           'Tina': 60.0,
           'Urša': 46.0,
           'Zofka': 46.0}, natancnost(self.manjsi))

    def test_03_kvaliteta(self):
        self.assertEqual([
            'Berta',
            'Petra',
            'Cilka',
            'Fanči',
            'Micka',
            'Angelca',
            'Tina',
            'Klara',
            'Helga',
            'Johanca',
            'Urša',
            'Zofka',
            'Nina'],
        kvaliteta(self.manjsi))

        dnevnik = preberi_dnevnik("odgovori.txt")
        self.assertEqual([
            'Olga',
            'Fanči',
            'Ema',
            'Urša',
            'Nina',
            'Dani',
            'Iva',
            'Johanca',
            'Angelca',
            'Berta',
            'Zofka',
            'Jana',
            'Klara',
            'Helga',
            'Tina',
            'Cilka',
            'Petra',
            'Micka'],
            kvaliteta(self.dnevnik))

class Test09(TestD):
    def setUp(self):
        super().setUp()
        self.rodbina = {
            "Adam": {"Matjaž", "Cilka", "Daniel"},
            "Daniel": {"Elizabeta", "Hans"},
            "Elizabeta": {"Ludvik", "Jurij", "Barbara"},
            "Herman": {"Margareta"},
            "Hans": {"Herman", "Erik"},
            "Jožef": {"Alenka", "Aleksander", "Petra"},
            "Jurij": {"Franc", "Jožef"},
            "Matjaž": {"Viljem"},
            "Viljem": {"Tadeja"}
        }

    def test_01_neustvarjalni(self):
        self.assertEqual(
            {'Berta': 'Predlagana sprememba ni v načrtu.',
             'Helga': 'Predlagana sprememba ni v načrtu.',
             'Johanca': 'Problem bomo preučili in ukrepali skladno s pristojnostmi.',
             'Petra': 'Problem bomo preučili in ukrepali skladno s pristojnostmi.',
             'Urša': 'Predlagana sprememba ni v načrtu.'},
            neustvarjalni(self.manjsi))

        self.assertEqual(
            {'Johanca': 'Ureditev bomo reševali celostno.',
             'Olga': 'Hvala za komentar.',
             'Tina': 'Ureditev bomo reševali celostno.',
             'Urša': 'Problem bomo preučili in ukrepali skladno s pristojnostmi.'},
            neustvarjalni(self.dnevnik))

    def test_02_pot_med(self):
        self.assertEqual(
            ["Adam", "Daniel", "Hans", "Erik"],
            pot_med(self.rodbina, "Adam", "Erik"))
        self.assertEqual(
            ["Adam", "Daniel", "Hans", "Herman"],
            pot_med(self.rodbina, "Adam", "Herman"))
        self.assertEqual(
            ['Adam', 'Daniel', 'Elizabeta', 'Jurij', 'Jožef', 'Aleksander'],
            pot_med(self.rodbina, "Adam", "Aleksander"))
        self.assertEqual(
            ['Elizabeta', 'Jurij', 'Jožef', 'Aleksander'],
            pot_med(self.rodbina, "Elizabeta", "Aleksander"))
        self.assertEqual(
            ['Elizabeta'],
            pot_med(self.rodbina, "Elizabeta", "Elizabeta"))
        self.assertIsNone(pot_med(self.rodbina, "Elizabeta", "Adam"))
        self.assertIsNone(pot_med(self.rodbina, "Elizabeta", "Hans"))
        self.assertIsNone(pot_med(self.rodbina, "Elizabeta", "Herman"))

        hierarhija = podrejeni(self.dnevnik)
        self.assertEqual(
            ['Angelca', 'Dani', 'Tina'],
            pot_med(hierarhija, "Angelca", "Tina"))
        self.assertIn(
            pot_med(hierarhija, "Angelca", "Jana"),
            (['Angelca', 'Dani', 'Jana'], ['Angelca', 'Cilka', 'Klara', 'Jana']))
        self.assertIn(
            pot_med(hierarhija, "Zofka", "Jana"),
            (['Zofka', 'Angelca', 'Dani', 'Jana'], ['Zofka', 'Angelca', 'Cilka', 'Klara', 'Jana']
            ))
        self.assertIsNone(pot_med(hierarhija, "Angelca", "Zofka"))

    def test_03_nivoji(self):
        self.assertEqual(
            {'Elizabeta': 0,
             'Barbara': 1,
             'Jurij': 1,
             'Ludvik': 1,
             'Franc': 2,
             'Jožef': 2,
             'Aleksander': 3,
             'Alenka': 3,
             'Petra': 3},
            nivoji(self.rodbina, "Elizabeta")
        )

        self.assertEqual(
            {'Adam': 0,
             'Aleksander': 5,
             'Alenka': 5,
             'Barbara': 3,
             'Cilka': 1,
             'Daniel': 1,
             'Elizabeta': 2,
             'Erik': 3,
             'Franc': 4,
             'Hans': 2,
             'Herman': 3,
             'Jožef': 4,
             'Jurij': 3,
             'Ludvik': 3,
             'Margareta': 4,
             'Matjaž': 1,
             'Petra': 5,
             'Tadeja': 3,
             'Viljem': 2},
            nivoji(self.rodbina, "Adam")
        )

        self.assertEqual(
            {"Aleksander": 0},
            nivoji(self.rodbina, "Aleksander")
        )

        a, b, c, d, e = "abcde"
        hierarhija = {
            d: {e},
            a: {b, c},
            b: {c, d, e},
        }
        self.assertEqual(
            {'a': 0, 'b': 1, 'c': 1, 'd': 2, 'e': 2},
            nivoji(hierarhija, a))
        hierarhija = {
            a: {b, c},
            b: {c, d, e},
            d: {e},
        }
        self.assertEqual(
            {'a': 0, 'b': 1, 'c': 1, 'd': 2, 'e': 2},
            nivoji(hierarhija, a))
        hierarhija = {
            a: {b, c},
            b: {c, d},
            d: {e}
        }
        self.assertEqual(
            {'a': 0, 'b': 1, 'c': 1, 'd': 2, 'e': 3},
            nivoji(hierarhija, a))


        hierarhija = podrejeni(self.manjsi)
        self.assertEqual(
            {'Angelca': 0, 'Berta': 1, 'Fanči': 1},
            nivoji(hierarhija, "Angelca")
        )

        hierarhija = podrejeni(self.dnevnik)
        self.assertEqual(
            {'Angelca': 1,
             'Berta': 2,
             'Cilka': 2,
             'Dani': 2,
             'Ema': 2,
             'Fanči': 2,
             'Helga': 2,
             'Iva': 3,
             'Jana': 3,
             'Johanca': 1,
             'Klara': 3,
             'Micka': 3,
             'Nina': 3,
             'Olga': 3,
             'Petra': 3,
             'Tina': 3,
             'Urša': 4,
             'Zofka': 0},
            nivoji(hierarhija, "Zofka")
        )

class Test10(unittest.TestCase):
    def test_01_odpiranje_datoteke(self):
        with warnings.catch_warnings(category=ResourceWarning, record=True) as warns:
            preberi_dnevnik("odgovori-manjsi.txt")
        self.assertEqual([], warns,
                         "Funkcija preberi_dnevnik ni pravilno odprla datoteke.")

    def test_02_poimenovane_terke(self):
        dnevnik = preberi_dnevnik("odgovori-manjsi.txt")
        tretji = dnevnik[3]
        self.assertIsInstance(tretji, Zapis)
        self.assertIsInstance(tretji, tuple)
        self.assertEqual(2, tretji.stevilka)
        self.assertEqual(3032, tretji.cas)
        self.assertEqual("prejem", tretji.akcija)
        self.assertIsNone(tretji.kdo)
        self.assertIsNone(tretji.rezultat)

        zapis = Zapis(42, 17, "prepusti", "Zofka", "Johanca")
        self.assertEqual(42, zapis.cas)
        self.assertEqual(17, zapis.stevilka)
        self.assertEqual("prepusti", zapis.akcija)
        self.assertEqual("Zofka", zapis.kdo)
        self.assertEqual("Johanca", zapis.rezultat)
        self.assertEqual((42, 17, "prepusti", "Zofka", "Johanca"), zapis)

        zapis = Zapis(13, 1234, "prejen")
        self.assertEqual(13, zapis.cas)
        self.assertEqual(1234, zapis.stevilka)
        self.assertEqual("prejen", zapis.akcija)
        self.assertIsNone(zapis.kdo)
        self.assertIsNone(zapis.rezultat)

    def test_03_dekorator(self):
        @s_casi
        def f(x):
            self.assertEqual(
                {1: 82, 2: 106, 3: 190, 4: 240, 5: 235, 6: 186, 7: 205, 8: 46, 9: 155},
                x)

        f(preberi_dnevnik("odgovori-manjsi.txt"))

    def test_04_tipi(self):
        from typing import Union

        def assertHierarchy(hierarhija):
            self.assertIs(hierarhija.__origin__, dict)
            kljuc, vrednost = hierarhija.__args__
            self.assertEqual(str, kljuc)
            self.assertIs(vrednost.__origin__, set)
            self.assertEqual((str,), vrednost.__args__)

        with self.subTest("Tipi v funkciji 'hitro'"):
            zapisi, meja = hitro.__code__.co_varnames[:2]
            self.assertEqual(
                {zapisi: list[Zapis], meja: int, 'return': int},
                hitro.__annotations__)

        with self.subTest("Tipi v funkciji 'podrejeni'"):
            tipi = podrejeni.__annotations__.copy()
            assertHierarchy(tipi.pop('return'))
            self.assertEqual(list[Zapis], tipi.popitem()[1])

        with self.subTest("Tipi v funkciji 'pot_med'"):
            hierarhija, oseba1, oseba2 = pot_med.__code__.co_varnames[:3]
            tipi = pot_med.__annotations__
            assertHierarchy(tipi[hierarhija])
            self.assertEqual(tipi[oseba1], str)
            self.assertEqual(tipi[oseba2], str)
            rezultat = tipi['return']
            self.assertIs(rezultat.__origin__, Union)
            self.assertEqual(2, len(rezultat.__args__))
            self.assertIn(type(None), rezultat.__args__)
            ne_none = rezultat.__args__[1 - rezultat.__args__.index(type(None))]
            self.assertIs(ne_none.__origin__, list)
            self.assertEqual((str, ), ne_none.__args__)

        with self.subTest("Tipi v funkciji 'nivoji'"):
            hierarhija, oseba = nivoji.__code__.co_varnames[:2]
            tipi = nivoji.__annotations__
            assertHierarchy(tipi[hierarhija])
            self.assertEqual(tipi[oseba], str)
            rezultat = tipi['return']
            self.assertIs(rezultat.__origin__, dict)
            self.assertEqual((str, int), rezultat.__args__)


if __name__ == "__main__":
    unittest.main()
