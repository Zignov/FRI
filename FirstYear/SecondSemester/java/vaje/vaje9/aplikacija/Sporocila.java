package vaje.vaje9.aplikacija;

import vaje.vaje9.kodirniki.CezarjevAlgoritem;
import vaje.vaje9.kodirniki.Kodiranje;
import vaje.vaje9.kodirniki.Kodirnik;
import vaje.vaje9.kodirniki.XORAlgoritem;

public class Sporocila {


    public static void main (String [] args){
        Kodirnik cezar = new CezarjevAlgoritem(4);
        Kodiranje testCez = new Kodiranje(cezar);

        String zakodirano = testCez.zakodiranjeBesedila("test");
        System.out.print("Kodirano: ");
        System.out.println(zakodirano);
        System.out.print("Odkodirano: ");
        System.out.println(testCez.odkodiranjeBesedila(zakodirano));

        System.out.println();

        Kodirnik xor = new XORAlgoritem("test");
        Kodiranje testXOR = new Kodiranje(xor);

        String zakodirano2 = testXOR.zakodiranjeBesedila("test");
        System.out.print("Kodirano: ");
        System.out.println(zakodirano2);
        System.out.print("Odkoriano: ");
        System.out.println(testXOR.odkodiranjeBesedila(zakodirano2));
    }
}
