package vaje.igra;

import java.util.ArrayList;
import java.util.Random;

public class Logika {

    private static int[][] polja;
    private static int tocke;
    private static boolean konec = true;

    static Random rnd = new Random();

    public static void zacniNovoIgro(int velikost){
        tocke = 0;
        polja = new int[velikost][velikost];
        konec = false;
        int novoStevilo;

        for(int i =0; i<2; i++){
            DodajSt(polja);
        }
    }

    public static int[][] DodajSt (int[][] povrsina){
        ArrayList<Integer> prazno = new ArrayList<Integer>();
        int stevec = 0;
        int novoStevilo;
        for(int i = 0; i<povrsina.length; i++){
            for(int j = 0; j<povrsina[i].length; j++){
                if(povrsina[i][j] == 0){
                    prazno.add(stevec);
                }
                stevec++;
            }
        }

        int izbrana = rnd.nextInt(prazno.size());
        int poljnjenoPolje = prazno.get(izbrana);
        if(rnd.nextDouble(0,1)>=0.9){
            novoStevilo = 4;
        }
        else {
            novoStevilo = 2;
        }
        povrsina[poljnjenoPolje/polja.length][poljnjenoPolje%polja.length] = novoStevilo;
        prazno.remove(izbrana);
        return povrsina;
    }

    public static int vrniPloscico(int i, int j){
        try{
            return polja[i][j];
        }
        catch (Exception e) {
            System.out.println("out of bounds");
            return 0;
        }
    }

    public static void koncajIgro(){
        if(konec){
            System.exit(0);
        }
        else {
            konec = true;
        }
    }


    public static int vrniTocke(){
        return 0;
    }

    public static boolean jeZmagal(){
        return false;
    }

    public static boolean jeKonec(){
        /*for (int i = 0; i<polja.length-1; i++){
            for(int j=0; j<polja[i].length-1; j++){
                if(polja[i][j] != 0 && polja[i][j] != polja [i][j+1] || polja[i][j] != polja [i+1][j]){
                    konec = true;
                }
            }
        }
        return konec;*/
        return konec;
    }

    public static void naslednjaPoteza(int smer){
        int[][] trenutna = polja;

        switch (smer){
            case(0):
                premikLevo(polja);
                break;
            case(1):
                rotiraj();
                rotiraj();
                premikLevo(polja);
                rotiraj();
                rotiraj();
                break;
            case(2):
                rotiraj();
                rotiraj();
                rotiraj();
                premikLevo(polja);
                rotiraj();
                break;
            case(3):
                rotiraj();
                premikLevo(polja);
                rotiraj();
                rotiraj();
                rotiraj();
        }


        DodajSt(polja);     //todo: ce spammas isto smer se zmer doda...
    }



    public static int[][] premikLevo(int[][] polje){
        boolean premik = false;

        for (int i = 0; i<polje.length; i++){
            for (int j=1; j<polje[i].length; j++){
                if (polje[i][j] != 0){
                    if(polje[i][j-1] == 0){
                        polje[i][j-1] = polje[i][j];
                        polje[i][j] = 0;
                        premik = true;
                    }

                }
            }
        }

        if(premik){
            return premikLevo(polje);
        }

        for (int i = 0; i<polje.length; i++){
            for(int j = 0; j<polje[i].length-1; j++){
                if(polje[i][j] == polje[i][j+1] && polje[i][j] != 0){
                    polje[i][j] *= 2;
                    polje[i][j+1] = 0;
                    premik = true;

                }


            }
        }

        return polje;
    }


    /**
     * Zarotira igralno polje (tabela polja) za 90 stopinj
     * v smeri urinega kazalca (v desno).
     * Rezultat metode je zarotirana tabela <code>polja</code>.
     */
    private static void rotiraj() {
        // najprej transponiramo tabelo - zamenjamo stolpce in vrstice
        for (int i = 0; i < polja.length; i++) {
            for (int j = i + 1; j < polja.length; j++) {
                int tmp = polja[i][j];
                polja[i][j] = polja[j][i];
                polja[j][i] = tmp;
            }
        }
        // če rotiramo v desno (v smeri urinega kazalca), obrnemo še vrstni red stolpcev
        for (int i = 0; i < polja.length; i++) {
            for (int j = 0; j < polja.length / 2; j++) {
                int tmp = polja[i][j];
                polja[i][j] = polja[i][polja.length - 1 - j];
                polja[i][polja.length - 1 - j] = tmp;
            }
        }
    }


}
