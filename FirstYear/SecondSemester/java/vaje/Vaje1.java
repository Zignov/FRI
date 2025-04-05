package vaje;

public class Vaje1 {
    public static void pravokonikStevilVrstice(int sirina, int visina){
        for (int i = 1; i<=visina; i++){
            for (int j = 0; j<sirina; j++){
                System.out.print(i%10);
            }
            System.out.println();
        }
    }

    public static void pravokotnikStevilStolpci(int sirina, int visina){
        for (int i = 0; i<visina; i++){
            for (int j = 1; j<= sirina; j++){
                System.out.print(j%10);
            }
            System.out.println();
        }
    }

    public static void pravokotnik(int odmik, int sirina, int visina){
        for (int i = 0; i<visina; i++){
            for (int j = 0; j<odmik; j++){
                System.out.print(" ");
            }
            for (int j = 0; j< sirina; j++){
                System.out.print("x");
            }
            System.out.println();
        }
    }

    public static void trikotnikStevilVrstice(int visina){
        for (int i = 1; i<=visina; i++){
            for (int j = 0; j<i; j++){
                System.out.print(i%10);
            }
            System.out.println();
        }
    }

    public static void trikotnikStevilStolpci(int visina){
        for (int i = 1; i<=visina; i++){
            for (int j = 1; j<=i; j++){
                System.out.print(j%10);
            }
            System.out.println();
        }
    }

    public static void trikotnikStevilVrsticeObrnjen(int visina){
        for (int i = visina; i>0; i--){
            for (int j = i; j>0; j--){
                System.out.print(i%10);
            }
            System.out.println();
        }
    }

    public static void trikotnikStevilStolpciObrnjen(int visina){
        for (int i = visina; i>0; i--){
            for (int j = i; j>0; j--){
                System.out.print(j%10);
            }
            System.out.println();
        }
    }

    public static void trikotnikStevil(int visina){
        for (int i = 1; i<=visina; i++){
            for(int j = 0; j<(visina - i); j++){
                System.out.print(" ");
            }
            for(int j = 1; j<(i*2); j++){
                System.out.print(j%10);
            }
            System.out.println();
        }
    }

    public static void trikotnik(int odmik, int visina){
        for (int i = 1; i<= visina; i++){
            for(int j = 0; j<(visina - i)+odmik; j++){
                System.out.print(" ");
            }

            for (int j = 1; j<=(i*2-1); j++){
                System.out.print("*");
            }
            System.out.println();
        }
    }

    public static void trikotnikObrnjen(int odmik, int visina){
        for (int i = visina; i>0; i--){
            for(int j = 0; j<(visina - i)+odmik; j++){
                System.out.print(" ");
            }

            for (int j = 1; j<=(i*2-1); j++){
                System.out.print("*");
            }
            System.out.println();
        }
    }

    public static void romb(int odmik, int velikost) {
        trikotnik(odmik, velikost);
        trikotnikObrnjen(odmik+1, velikost-1);
    }

    public static void smreka(int v){
        int stevec = 0;
        int debelina;
        if (v%2 == 0){
            debelina = v+1;
        }
        else{
            debelina = v;
        }

        for (int i = 1; i<=v; i++){
            trikotnik(v*2-2*i, 2*i);
            stevec++;

        }
        //System.out.print(stevec*2*2-1);
        for(int j = 0; j< v*2; j++) {
            for (int i = 0; i < ((4 * stevec - 1) - v) / 2; i++) {
                System.out.print(" ");
            }
            for (int i = 0; i < debelina; i++) {
                System.out.print("X");
            }
            System.out.println();
        }
    }









    public static void main(String[] args){
        //pravokonikStevilVrstice(7,3);
        //pravokotnikStevilStolpci(15,3);
        //pravokotnik(5,7,3);
        //trikotnikStevilVrstice(3);
        //trikotnikStevilStolpci(5);
        //trikotnikStevilVrsticeObrnjen(3);
        //trikotnikStevilStolpciObrnjen(3);
        //trikotnikStevil(5);
        //trikotnik(5,5);
        //trikotnikObrnjen(5, 5);
        //romb(2,5);
        smreka(4);
    }
}
