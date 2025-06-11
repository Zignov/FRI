package izpiti;

import java.util.Locale;

public class sin {

    public static double factorial(int n) {
        if (n < 0) {
            System.out.println("ne");
        }
        double result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }



    public static void izracunajPriblizek(double x, int d){
        Locale.setDefault(Locale.ENGLISH);


        double napaka = Math.pow(10, -d);

        double priblizek = 0;

        int stevec = 0;

        while(Math.abs(Math.sin(x) - priblizek) >= napaka){

            int eks = stevec*2+1;
            double fac = factorial(eks);


            if(stevec % 2 == 1){
                priblizek -= Math.pow(x, eks)/fac;
            }
            else{
                priblizek += Math.pow(x, eks)/fac;
            }

            stevec++;

            System.out.printf("Stevec: %d, sin: %f, pribl: %f\n", stevec, Math.sin(x), priblizek);
        }


    }



    public static void main(String[]args){
        izracunajPriblizek(1.7,4);


    }


}
