package vaje.vaje9.kodirniki;

public class XORAlgoritem extends Kodirnik{

    public XORAlgoritem(String geslo) {
        this.geslo = geslo;
    }

    String geslo;
    int index = 0;


    @Override
    int zakodiraj(int vrednost) {
         int rez = (vrednost) ^ geslo.charAt(index % (geslo.length()));
         index++;
         return rez;
    }

    @Override
    int odkodiraj(int vrednost) {
        return (zakodiraj(vrednost));
    }

    @Override
    public void ponsatavi() {
        index = 0;
    }
}
