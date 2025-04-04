package Vaje.vaje4.zbirke;

public class Seznam {


    private static int stStvari;
    private static String[] seznam;


    /** ustvari seznam
     * @param dolzina seznama
     * @return true ce se seznam uspeno ustvari in false, ce ze obstaja
     */

    public static boolean narediSeznam(int n){
        try{
            seznam = new String[n];
            return true;
        }
        catch(Exception e) {
            System.out.print("seznam ze obstaja");
            return false;
        }
    }

    /**
     * Doda element na zadnje (prazno) mesto v seznamu
     * @param element
     * @return true ob uspehu false of napaki
     */
    public static boolean dodajNaKonecSeznama(String element){
        if ((seznam == null) || (seznam.length == stStvari)){
            return false;
        }
        seznam[stStvari] = element;
        stStvari++;
        return true;

    }

    /**
     * Metoda izpise vse elemente v seznamu
     */
    public static void izpisiSeznam(){
        if (seznam == null){
            System.out.print("NAPAKA: Seznam ne obstaja.");
        }
        else if(stStvari<1){
            System.out.print("Seznam je prazen (nima elementov).");
        }
        else {

            System.out.println("Na seznamu so naslednji elementi:");
            for (int i = 1; i <= stStvari; i++) {
                System.out.println(i + ". " + seznam[i - 1]);
            }
        }
    }

    /**
     * Metoda odstrani element iz seznama na podanem mestu, vse ostale elemente zamakne
     * @param mesto
     * @return null ob napaki, odstranjen element ob uspehu
     */
    public static String odstraniIzSeznama(int mesto){
        if (seznam == null){
            return null;
        }
        mesto--;

        if (seznam[mesto] == null){
            return null;
        }

        String odvec = seznam[mesto];
        for (int i = mesto; i<stStvari; i++){
            if (i!=stStvari-1){
                seznam[i] = seznam[i+1];
            }
        }
        stStvari--;
        return odvec;
    }

    /**
     * Metoda doda element v seznam na podanem mestu
     * @param element
     * @param mesto
     * @return false ob napaki, true ob uspehu
     */
    public static boolean dodajVSeznam(String element, int mesto) {
        if (seznam == null || mesto < 1 || stStvari == seznam.length) {
            return false;
        }

        int index = mesto - 1;

        if (index > seznam.length) {
            dodajNaKonecSeznama(element);
        } else {
            seznam[index] = element;
        }
        return true;
    }

    /**
     * Vrnes dolzino seznama
     * @return -1 ce seznam ne obstaja, drugace dolzino seznama
     */

    public static int dolzinaSeznama(){
        if(seznam == null){
            return -1;
        }
        return stStvari;

    }

    /**
     * Unici seznam in vse elemente v njem
     * @return vrne false ce seznam ne obstaja, true ob unicenju
     */
    public static boolean uniciSeznam(){
        if (seznam == null){
            return false;
        }

        for (int i = 0; i<seznam.length; i++){
            seznam[i] = null;
        }

        seznam = null;
        return true;
    }



}
