package naloga5;

import java.io.File;
import java.util.Scanner;

public class DN05 {

    static int sirina;
    static int visina;

    public static int[][] preberiZacetnoPostavitev(String imeDatoteke){
        Scanner sc = null;

        try {
            sc = new Scanner(new File(imeDatoteke));
            //System.out.println(sc.nextLine());

            if (!sc.hasNextLine()){
                System.out.println("Napaka: Manjka podatek o dimenzijah igralne povrsine.");
                return null;
            }

            String velikost = sc.nextLine().trim();

            if (!velikost.matches("\\d+x\\d+")){
                System.out.println("Napaka: Nepravilen podatek o dimenzijah igralne povrsine.");
                return null;
            }

            sirina = Integer.parseInt(velikost.split("x")[0]);
            visina = Integer.parseInt(velikost.split("x")[1]);

            if (sirina<0 || visina<0){
                System.out.println("Napaka: Dimenzija mora biti pozitivna.");
                return null;
            }

            if(!sc.hasNextLine()){
                System.out.println("Napaka: Manjka podatek o stevilu ladij.");
                return null;
            }
            //System.out.println(visina);
            int stLadij = Integer.parseInt(sc.nextLine());
            //System.out.println(stLadij);

            if (stLadij<0){
                System.out.println("Napaka: Stevilo ladij ne sme biti negativno.");
                return null;
            }

            int [][] postavitev = new int[stLadij][5];

            for (int i=0; i<stLadij; i++){
                if(!sc.hasNextLine()){
                    System.out.println("Napaka: Podatek o stevilu ladij se ne ujema s stevilom vnosov.");
                    return null;
                }

                String[] ladja = sc.nextLine().split(" ");
                if (ladja.length != 5){
                    System.out.println("Napaka: Nepravilen podatek o postavitvi ladje.");
                    return null;
                }

                switch (ladja[4]){
                    case("S"):
                        ladja[4] = "0";
                        break;
                    case("J"):
                        ladja[4] = "1";
                        break;
                    case("V"):
                        ladja[4] = "2";
                        break;
                    case("Z"):
                        ladja[4] = "3";
                        break;

                    default:
                        System.out.println("Napaka: Nepravilen podatek o postavitvi ladje.");
                        return null;
                }

                for (int j = 0; j<5; j++){
                    try {
                        postavitev[i][j] = Integer.parseInt(ladja[j]);
                    }
                    catch (Exception e){
                        System.out.println("Napaka: Nepravilen podatek o postavitvi ladje.");
                        return null;
                    }
                }
            }

            return postavitev;

        }
        catch (Exception e){
            System.out.println("Napaka: datoteka ne obstaja.");
        }
        finally {
            if (sc != null) {
                sc.close();
            }
        }

        return null;
    }


    public static void izpisiPostavitev(int[][] postavitev){
        for(int i = 0; i< postavitev.length; i++){
            System.out.printf("Igralec: %d Dolzina: %d Smer: %d Koordinate premca: (%d,%d)", postavitev[i][0], postavitev[i][3],postavitev[i][4],postavitev[i][1],postavitev[i][2]);
            System.out.println();
        }
    }


    public static int[][] izdeljaIgralnoPovrsino(int[][] postavitev){
        int[][] povrsina = new int[visina][2*sirina];
        int x;
        int y;

        for (int i = 0; i<postavitev.length; i++){      //ladje

            //povrsina[postavitev[i][2]][postavitev[i][0]+postavitev[i][1]] = (i+1)*10+1;
            for(int j = 0; j<postavitev[i][3]; j++){    //dolzina
                try {
                    switch (postavitev[i][4]) {

                        case (0):
                            x = postavitev[i][2] - j - 1;
                            y = postavitev[i][0] * sirina + postavitev[i][1] - 1;
                            if (povrsina[x][y] == 0)
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            else{
                                //TODO odstrani function, k bo dobu j pa su cez celo tabelo pa brisov
                            }
                            break;
                        case (1):
                            x = postavitev[i][2] + j - 1;
                            y = postavitev[i][0] * sirina + postavitev[i][1] - 1;
                            if (povrsina[x][y] == 0) {
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                        case (2):
                            x = postavitev[i][2] - 1;
                            y = postavitev[i][0] * sirina + postavitev[i][1] + j - 1;
                            if (povrsina[x][y] == 0) {
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                        case (3):
                            x = postavitev[i][2] - 1;
                            y = postavitev[i][0] * sirina + postavitev[i][1] - j - 1;
                            if (povrsina[x][y] == 0) {
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                    }
                }
                catch (Exception e){
                    continue;
                }
            }
        }
        for (int i = 0; i < povrsina.length; i++) {
            for (int j = 0; j < povrsina[i].length; j++) {
                System.out.printf("%3d", povrsina[i][j]); // fixed-width columns
            }
            System.out.println();
        }

        return postavitev;
    }

    public static void main (String[] args){

        if (args.length == 2){
            if(args[0].equals("postavitev")){
                int[][] postavitev = preberiZacetnoPostavitev(args[1]);
                izpisiPostavitev(postavitev);
                izdeljaIgralnoPovrsino(postavitev);
            }
        }
    }

}