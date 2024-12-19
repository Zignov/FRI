

from itertools import pairwise


def hitrejsa(prva, druga, razmerja):
    if druga in razmerja[prva]:
        return True
    elif prva in razmerja[druga]:
        return False
    else:
        return any(hitrejsa(x, druga, razmerja) for x in razmerja[prva])
    
def skalpi(kolesarka, razmerja):
    rezultat = set(razmerja[kolesarka])
    rezultat.add(kolesarka)
    
    for x in razmerja[kolesarka]:
        rezultat |= (skalpi(x, razmerja))
      
    #print("rezultat je:" , rezultat)
    return rezultat    


def izlocanje(kandidatke, razmerja):
    odgovor = set()
    for x in kandidatke:
        premagane = skalpi(x, razmerja)
        je_premagana = False
        
        for premagan in kandidatke:
            if premagan != x and hitrejsa(premagan, x, razmerja):
                je_premagana = True
                break
            
        if not je_premagana:
            odgovor.add(x)
        
    return odgovor

razmerja = {'Ana': {'Vera', 'Cilka'},
            'Berta': {'Greta', 'Klara', 'Iva', 'Cilka'},
            'Cilka': {'Olga'},
            'Črtomira': set(),
            'Dani': {'Liza', 'Ana', 'Fanči', 'Cilka', 'Micka', 'Greta'},
            'Ema': set(),
            'Fanči': {'Liza', 'Poldka', 'Cilka'},
            'Greta': set(),
            'Helga': set(),
            'Iva': {'Ema', 'Helga'},
            'Jana': {'Liza', 'Dani', 'Berta', 'Micka', 'Tina', 'Greta'},
            'Klara': {'Helga', 'Nina'},
            'Liza': {'Vera', 'Olga', 'Rezka'},
            'Micka': {'Liza', 'Saša', 'Urša'},
            'Nina': {'Olga', 'Poldka'},
            'Olga': {'Poldka'},
            'Poldka': set(),
            'Rezka': {'Saša'},
            'Saša': set(),
            'Špela': {'Žana'},
            'Tina': set(),
            'Urša': {'Vera'},
            'Vera': set(),
            'Zoja': {'Žana', 'Tina'},
            'Žana': set()}

razmerja2 = {x: {y} for x, y in pairwise(sorted(razmerja))}
razmerja2.update({"Žana": set(), "Trelawney": set()})

import unittest


class Test01Obvezna(unittest.TestCase):
    def test_01_hitrejsa(self):
        self.assertTrue(hitrejsa("Jana", "Berta", razmerja))
        self.assertFalse(hitrejsa("Berta", "Jana", razmerja))
        self.assertTrue(hitrejsa("Berta", "Poldka", razmerja))
        self.assertFalse(hitrejsa("Poldka", "Berta", razmerja))
        self.assertFalse(hitrejsa("Saša", "Berta", razmerja))
        self.assertFalse(hitrejsa("Berta", "Saša", razmerja))
        self.assertFalse(hitrejsa("Špela", "Tina", razmerja))
        self.assertFalse(hitrejsa("Jana", "Črtomira", razmerja))
        self.assertFalse(hitrejsa("Črtomira", "Jana", razmerja))

        # Testi na drugačnem grafu
        self.assertTrue(hitrejsa("Ana", "Žana", razmerja2))
        self.assertFalse(hitrejsa("Žana", "Ana", razmerja2))
        self.assertFalse(hitrejsa("Ana", "Trelawney", razmerja2))
        self.assertFalse(hitrejsa("Ana", "Trelawney", razmerja2))

    def test_02_skalpi(self):
        self.assertEqual(
            {"Berta", "Cilka", "Olga", "Poldka", "Iva", "Klara", "Helga", "Ema", "Nina", "Greta"},
            skalpi("Berta", razmerja))
        self.assertEqual(
            {"Cilka", "Olga", "Poldka"},
            skalpi("Cilka", razmerja))
        self.assertEqual(
            {"Olga", "Poldka"},
            skalpi("Olga", razmerja))
        self.assertEqual(
            {"Greta"},
            skalpi("Greta", razmerja))
        self.assertEqual(
            {"Iva", "Helga", "Ema"},
            skalpi("Iva", razmerja))

        # Testi na drugačnem grafu
        self.assertEqual(
            {"Žana"}, skalpi("Žana", razmerja2))
        self.assertEqual(
            {'Liza', 'Micka', 'Nina', 'Olga', 'Poldka', 'Rezka', 'Saša',
             'Tina', 'Urša', 'Vera', 'Zoja', 'Črtomira', 'Špela', 'Žana'},
            skalpi("Liza", razmerja2))

    def test_03_izlocanje(self):
        self.assertEqual(
            {"Žana", "Dani", "Iva"},
            izlocanje({"Žana", "Dani", "Ema", "Iva", "Fanči", "Vera"}, razmerja)
        )
        self.assertEqual(
            {"Žana", "Jana"},
            izlocanje({"Žana", "Jana", "Dani", "Ema", "Iva", "Fanči", "Vera"}, razmerja)
        )
        self.assertEqual(
            {"Jana"},
            izlocanje({"Jana", "Dani", "Ema", "Iva", "Fanči", "Vera"}, razmerja)
        )

        # Testi na drugačnem grafu
        self.assertEqual(
            {"Fanči"},
            izlocanje({"Greta", "Jana", "Vera", "Fanči"}, razmerja2)
        )


class Test02Dodatna(unittest.TestCase):
    def test_01_dokazov(self):
        self.assertEqual(1, dokazov("Jana", "Berta", razmerja))
        self.assertEqual(0, dokazov("Berta", "Jana", razmerja))
        self.assertEqual(4, dokazov("Jana", "Cilka", razmerja))
        self.assertEqual(1, dokazov("Jana", "Nina", razmerja))
        self.assertEqual(5, dokazov("Jana", "Liza", razmerja))
        self.assertEqual(10, dokazov("Jana", "Olga", razmerja))
        self.assertEqual(12, dokazov("Jana", "Poldka", razmerja))
        self.assertEqual(1, dokazov("Špela", "Žana", razmerja))

        self.assertEqual(1, dokazov("Ana", "Žana", razmerja2))
        self.assertEqual(0, dokazov("Žana", "Ana", razmerja2))


if __name__ == "__main__":
    unittest.main()
