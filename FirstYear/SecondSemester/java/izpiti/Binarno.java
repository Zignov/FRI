package izpiti;

import java.io.File;
import java.util.Scanner;

public class Binarno {

    public static void prevod(){


        try {

            File v = new File("viri/medved.bin");
            Scanner sc = new Scanner(v);
            StringBuilder raw = new StringBuilder();

            while (sc.hasNextLine()){
                raw.append(sc.nextLine());
            }

            String[] split = String.valueOf(raw).split(" ");


            StringBuilder rez = new StringBuilder("year  month  day  hour  minute  latitude  longitude");

            for (int i = 0; i < split.length; i++) {
                rez.append(Integer.parseInt(split[i], 2));
                if (i % 7 == 0) {
                    rez.append("\n");
                }
            }


            System.out.println(rez);

        }
        catch (Exception e){

        }
    }

    public static void main(String[] args){
        prevod();
    }



}
