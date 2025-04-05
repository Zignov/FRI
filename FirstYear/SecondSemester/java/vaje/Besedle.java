package vaje;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.Scanner;

public class Besedle {

    // Konstante barv
    static final int BELA = 0;
    static final int CRNA = 1;
    static final int RUMENA = 2;
    static final int ZELENA = 3;

    // ANSI ukazi (za barvni izpis)
    static final String ANSI_RESET = "\u001B[0m";
    static final String ANSI_GREEN_BG = "\u001b[42m";
    static final String ANSI_YELLOW_BG = "\u001b[43m";
    static final String ANSI_WHITE_BG = "\u001b[47;1m";
    static final String ANSI_BLACK_BG = "\u001b[40m";
    static final String ANSI_WHITE = "\u001b[37m";
    static final String ANSI_BLACK = "\u001b[30m";

    static final String abeceda = "ABCČDEFGHIJKLMNOPRSŠTUVZŽ"; // Veljavne črke
    static final int MAX_POSKUSOV = 6; // Število poskusov

    static String[] seznamBesed; // Seznam vseh možnih besed
    static String iskanaBeseda; // Iskana beseda trenutne igre
    static int[] barveAbecede; // Barve črk pri izpisu abecede

    static Scanner sc = new Scanner(System.in);

    // Izpiše znak v izbrani barvi
    static void izpisiZBarvo(char znak, int barva) {
        String slog;
        if (barva == ZELENA) {
            slog = ANSI_BLACK + ANSI_GREEN_BG;
        } else if (barva == RUMENA) {
            slog = ANSI_BLACK + ANSI_YELLOW_BG;
        } else if (barva == BELA) {
            slog = ANSI_BLACK + ANSI_WHITE_BG;
        } else {
            slog = ANSI_WHITE + ANSI_BLACK_BG;
        }
        System.out.print(slog + " " + znak + " " + ANSI_RESET);
    }

    // Prebere seznam besed iz datoteke
    static void preberiBesede(String datoteka) throws FileNotFoundException {
        Scanner reader1 = new Scanner(new File(datoteka));
        //System.out.println(reader1.nextLine());



        int steviloBesed = Integer.parseInt(reader1.nextLine());
        seznamBesed = new String[steviloBesed];
        //System.out.println(reader1.nextLine());

        for(int i = 0; i<steviloBesed && reader1.hasNextLine(); i++){
            String vrstica = reader1.nextLine().toUpperCase();
            //System.out.println(vrstica);
            seznamBesed[i] = vrstica;
        }

        //System.out.print(seznamBesed[5]);
        reader1.close();
    }

    // Pripravi vse za novo igro
    static void novaIgra() {
        Random rng = new Random();
        iskanaBeseda = seznamBesed[rng.nextInt(seznamBesed.length)];

        barveAbecede = new int[abeceda.length()];

        for (int i = 0; i<abeceda.length(); i++){
            barveAbecede[i] = 0;
        }

        //System.out.println(iskanaBeseda);
    }

    // Izpiše abecedo
    static void izpisiAbecedo() {
        for(int i = 0; i<abeceda.length(); i++){
            izpisiZBarvo(abeceda.charAt(i), barveAbecede[i]);
        }
        System.out.println();
    }

    // Ali je beseda veljavna?
    static boolean veljavnaBeseda(String beseda) {
        boolean odgovor = true;

        for(int i = 0; i<beseda.length(); i++){
            if(abeceda.contains(String.valueOf(beseda.charAt(i)))){
                odgovor = true;
            }
            else{
                odgovor = false;
                break;
            }
        }
        if(beseda.length() != 5){
            return false;
        }
        return odgovor;
    }

    // Določi barve črk v ugibani besedi
    static int[] pobarvajBesedo(String ugibanaBeseda) {
        int[] tabela = new int[ugibanaBeseda.length()];

        for(int i = 0; i<tabela.length; i++){
            tabela[i] = 0;
        }

        for (int i = 0; i<ugibanaBeseda.length(); i++){
            if(ugibanaBeseda.charAt(i) == iskanaBeseda.charAt(i)){
                tabela[i] = 3;
            }
            else if(iskanaBeseda.contains(String.valueOf(ugibanaBeseda.charAt(i)))){
                tabela[i] = 2;
            }
            else{
                tabela[i] = 1;
            }
        }

        for(int i = 0; i<ugibanaBeseda.length(); i++){
            int index = abeceda.indexOf(ugibanaBeseda.charAt(i));
            //System.out.println(index);

            barveAbecede[index] = tabela[i];

        }
        /*for(int i = 0; i<tabela.length; i++){
            System.out.print(tabela[i]);
        }*/

        return tabela;

        //return new int[0];
    }

    // Izpiši besedo
    static void izpisiBesedo(String ugibanaBeseda, int[] barve) {
        for (int i = 0; i<ugibanaBeseda.length(); i++){
            izpisiZBarvo(ugibanaBeseda.charAt(i), barve[i]);
        }
        System.out.println();
    }


    // Izvede eno igro
    static void igra() {
        novaIgra();

        //System.out.print(iskanaBeseda);

        int poskus = 1;
        boolean uganil = false;
        while (poskus <= MAX_POSKUSOV) {
            izpisiAbecedo();
            System.out.printf("Poskus %d/%d: ", poskus, MAX_POSKUSOV);
            String ugibanaBeseda = sc.nextLine().toUpperCase();

            //System.out.println(veljavnaBeseda(ugibanaBeseda));
            // Preveri veljavnost
            if (!veljavnaBeseda(ugibanaBeseda))
                continue;

            // Pobarvaj crke v besedi (namigi)
            int[] barve = pobarvajBesedo(ugibanaBeseda);

            // Izpiši pobarvano besedo
            izpisiBesedo(ugibanaBeseda, barve);

            if (ugibanaBeseda.equals(iskanaBeseda)) {
                uganil = true;
                break;
            }
            poskus++;
        }

        if (uganil) {
            System.out.printf("Bravo! Besedo si uganil/a v %d poskusih.\n", poskus);
        } else {
            System.out.printf("Žal ti ni uspelo. Pravilna beseda: %s\n", iskanaBeseda);
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        preberiBesede("FirstYear/SecondSemester/Java/Vaje/viri/besede.txt");

        while (true) {
            igra();
            System.out.print("Nova igra? (d/n): ");
            String odg = sc.nextLine();
            if (odg.toLowerCase().charAt(0) != 'd') {
                break;
            }
        }
    }
}