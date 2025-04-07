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

            if (sirina<=0 || visina<=0){
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

                if (Integer.parseInt(ladja[0]) != 0 && Integer.parseInt(ladja[0]) != 1){
                    System.out.println("Napaka: Nepravilen podatek o postavitvi ladje.");
                    return null;
                }

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
        int x = 0;
        int y = 0;

        for (int i = 0; i<postavitev.length; i++){      //ladje

            boolean napaka = false;

            //povrsina[postavitev[i][2]][postavitev[i][0]+postavitev[i][1]] = (i+1)*10+1;
            for(int j = 0; j<postavitev[i][3]; j++){    //dolzina
                try {
                    int igralec = postavitev[i][0];
                    int levaOmejitev = igralec * sirina;
                    int desnaOmejitev = (igralec + 1) * sirina - 1;

                    switch (postavitev[i][4]) {
                        case (1):
                            x = postavitev[i][2] - j;
                            y = postavitev[i][0] * sirina + postavitev[i][1];
                            if (x < 0 || x>= visina || y<levaOmejitev || y>desnaOmejitev || povrsina[x][y] != 0) //todo implement middle checking in if statement with &&
                                napaka = true;
                            else{
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                        case (0):
                            x = postavitev[i][2] + j;
                            y = postavitev[i][0] * sirina + postavitev[i][1];
                            if (x < 0 || x>= visina || y<levaOmejitev || y>desnaOmejitev || povrsina[x][y] != 0) {
                                napaka = true;
                            }
                            else{
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                        case (3):
                            x = postavitev[i][2];
                            y = postavitev[i][0] * sirina + postavitev[i][1] + j;
                            if (x < 0 || x>= visina || y<levaOmejitev || y>desnaOmejitev || povrsina[x][y] != 0) {
                                napaka = true;
                            }
                            else{
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                        case (2):
                            x = postavitev[i][2];
                            y = postavitev[i][0] * sirina + postavitev[i][1] - j;
                            if (x < 0 || x>= visina || y<levaOmejitev || y>desnaOmejitev || povrsina[x][y] != 0) {
                                napaka = true;
                            }
                            else{
                                povrsina[x][y] = (i + 1) * 10 + 1 + j;
                            }
                            break;
                    }


                }
                catch (Exception e){
                    napaka = true;
                    continue;
                }
                if(napaka){
                    //System.out.println("Napaka pri ladji $" + (i+1));
                    break;
                }


            }
            if (napaka){
                odstrani(i+1, povrsina);
            }
        }


        return povrsina;
    }

    public static void odstrani(int oznakaLadje, int[][] povrsina){
        for (int i = 0; i < povrsina.length; i++) {
            for (int j = 0; j < povrsina[i].length; j++) {
                if ((int)Math.floor(povrsina[i][j] / 10) == oznakaLadje){
                    povrsina[i][j] = 0;
                }
            }
        }
    }

    public static void izrisPovrsineDev(int[][] povrsina){
        for (int i = 0; i < povrsina.length; i++) {
            for (int j = 0; j < povrsina[i].length; j++) {
                System.out.printf("%3d", povrsina[i][j]); // fixed-width columns
            }
            System.out.println();
        }
    }


    public static void izrisiIgralnoPovrsino(int[][] igralnaPovrsina) {


        for (int i = 0; i<visina+2; i++){

                for(int j = 0; j<2*sirina+3; j++){
                    if(i == 0 || j == 0 || i ==visina+1 || j == sirina*2 + 2 || j == (sirina*2+2)/2){
                        System.out.print("# ");
                    }

                    else{
                        try{
                            int checkY = i - 1;
                            int checkX = 0;

                            if (j<(2*sirina+3)/2){
                                checkX = j-1;
                            }
                            else if(j>(2*sirina+3)/2){
                                checkX = j-2;
                            }
                            else {
                                continue;
                            }

                            String plovec = "p ";
                            String trup = "t ";
                            if (igralnaPovrsina[checkY][checkX] == 0){
                                System.out.print("  ");
                            }
                            else {
                                if(igralnaPovrsina[checkY][checkX] % 10 == 1){
                                    System.out.print(plovec);
                                }
                                else {
                                    System.out.print(trup);
                                }
                            }

                        }
                        catch (Exception e){
                            continue;
                        }
                    }
                }
                System.out.println();
        }
    }

    public static void main (String[] args){

        if (args.length == 2) {
            String ukaz = args[0];
            String datoteka = args[1];

            int[][] postavitev = preberiZacetnoPostavitev(datoteka);
            if (postavitev == null) {
                return;
            }

            if (ukaz.equals("postavitev")) {
                izpisiPostavitev(postavitev);
            } else if (ukaz.equals("povrsina")) {
                int[][] povrsina = izdeljaIgralnoPovrsino(postavitev);
                izrisiIgralnoPovrsino(povrsina);
            }
        }
        /*int[][] povrsina = izdeljaIgralnoPovrsino(postavitev);
        izrisPovrsineDev(povrsina);
        izrisiIgralnoPovrsino(povrsina);*/
    }

}