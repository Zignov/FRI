

def nal17():
    
    
    seznam = []
    
    while True:
        vhod = input()
        
        if vhod == "DODAJ":
            dodaj = input("Kaj zelis dodati?")
            seznam.append(dodaj)
            
        elif vhod == "IZPISI":
            for item in seznam:
                print(item + " ")
                
        elif vhod == "IZBRISI":
            izbis = input("Kaj zelite izbrisati")
            seznam.pop()