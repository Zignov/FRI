import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;

public class DN03 {
    public static void main (String[] args){

        if(args.length == 3) {
            try {
                String datoteka = args[0];
                int n = Integer.parseInt(args[1]);
                int seed = Integer.parseInt(args[2]);
                Scanner sc = new Scanner(new File(datoteka));
                Random random = new Random(seed);

                Scanner reader = new Scanner(new File(datoteka));
                int stevec = Integer.parseInt(reader.nextLine());
                String[] besede = new String[stevec];


                for (int i = 0; i < stevec; i++) {
                    besede[i] = reader.nextLine();
                }
                reader.close();
                //System.out.println(besede[3]);

                for(int i = 0; i<n; i++){
                    int nakljucna = random.nextInt(stevec);
                    System.out.print(besede[nakljucna].charAt(random.nextInt(besede[nakljucna].length())));
                }


            } catch (FileNotFoundException e) {
                System.out.println("error");
                e.printStackTrace();
            }
        }
        else{
            System.out.println("error");
        }
    }
}
