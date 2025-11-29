zemljevid = [(4, 7, 1), (1, 3, 2), (10, 14, 2), (4, 7, 4), (10, 14, 4), (4, 7, 6), 
(1, 3, 7), (6, 7, 7), (11, 15, 7)]

zemljevid2 = [(4, 7, 1), (1, 3, 2), (10, 14, 2), (4, 7, 4), (10, 14, 4), (4, 7, 6), 
(1, 3, 7), (6, 7, 7), (11, 15, 7), (12, 13, 8), (4, 6, 48), (3,7,4), (7,9,874)]


def nabava(stari, novi):
    seznam = set(novi)
    rezultat = {}
    
    for x in novi:
        for y in stari:
            print(f"x: {x}, y: {y}")
            if x == y:
                seznam.remove(y)
                
    print(seznam)
    
    
    for x0, x1, y in seznam:
        if (x1-x0) not in rezultat:
            rezultat[x1-x0] = 1
        else:
            rezultat[x1-x0] += 1
    
    print(rezultat)
    return(rezultat)

#nabava(zemljevid, zemljevid2)


def rekonstrukcija(kocke):
    slovar = {}
    rezultat = []
    for y, x in kocke:
        if y not in slovar:
            slovar[y] = {x}
        else:
            slovar[y].add(x)
            
    for y in slovar:
        rezultat.append((min(slovar[y]), max(slovar[y]), y))
            
    print(sorted(rezultat))
    
#rekonstrukcija([(2, 3), (1, 1), (2, 2), (2, 4), (1, 2), (3, 4)])
    
    
def dekodiraj_vrstico(vrstica):
    y = 1
    stevec = 1
    ovira = ()
    rezultat = []
    for x in vrstica:
        if x == "<":
            x0 = stevec
            
        if x == ">":
            x1 = stevec
            if (x1 - x0 != 1):
                ovira = (x0, x1)
                rezultat.append(ovira)
        
        stevec += 1
        
    #print(rezultat)
    
    return rezultat

#dekodiraj_vrstico("..<-->...<---->..<>..<..>")


def preberi(ime_datoteke):
    y = 1
    dat = open(ime_datoteke, mode="r", encoding="utf-8")
    rez = []
    
    for vrstica in open(ime_datoteke, mode="r", encoding="utf-8"):
        ovira = dekodiraj_vrstico(vrstica)
        if ovira:
            for koordinata in ovira:
                rez.append((*koordinata, y))
        y += 1
         
    print(rez)
    return rez
        
#preberi("test.txt")



'''slovar = {".": "dh", "d": "ab", "h": 
"tef", "a": "cr", "b": "uv", "t": "xy", "f": "qm", "c": "w", "r": "i", "u": "o", "v": "p", "x": "s", 
"y": "", "q": "g", "m": "n", "w": "j", "o": "l", "s": "z", "g": "B", "n": "A", "l": "T"}

def vrhovi(skladovnica, ovira, visina):
    stevec = 0

    if ovira in skladovnica:
        stevec += 1
        print(skladovnica[ovira])
        ovira = skladovnica[ovira]
        rezultat = vrhovi(slovar, skladovnica[ovira], visina)
    
    else:
        if stevec >= visina:
            print(stevec)
            return(rezultat)
        

print(vrhovi(slovar, "a", 3))'''



class Ovire:
    def __init__(self, x0, x1, y):
        self.x0 = x0
        self.x1 = x1
        self.y = y
        
    def strel(self, x, y):
        for x1, _, y1 in zemljevid:
            if (x,y) == (x1,y1):
                return True
            else:
                return False
            
    def zadetkov(self)
    
            
            
        
    
    
