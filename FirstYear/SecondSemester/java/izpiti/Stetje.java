package izpiti;

import java.io.*;
import java.util.Collection;
import java.util.Collections;
import java.util.Map;
import java.util.TreeMap;

public class Stetje {


    public static void preberiInIzpisi(String vhod) {

        TreeMap<String, Integer> rez = new TreeMap<>();

        try {
            FileInputStream fio = new FileInputStream(new File(vhod));
            InputStreamReader ior = new InputStreamReader(fio);


            while(ior.ready()){
                char ch = ((char)ior.read());
                if(Character.isAlphabetic(ch)) {
                    String crka = String.valueOf(ch).toUpperCase();
                    if (!crka.equals("\n")) {

                        if (rez.containsKey(crka)) {
                            rez.put(crka, rez.get(crka) + 1);
                        } else {
                            rez.put(crka, 1);
                        }
                    }
                }
            }


            rez.entrySet().stream().sorted(Map.Entry.<String, Integer>comparingByValue().reversed()).limit(5).forEach(e -> System.out.println(e.getKey() + ":"+e.getValue()));
            //System.out.println(rez);
            ior.close();

        }
        catch (Exception e){

        }
    }


    public static void main(String[] args){
        preberiInIzpisi("viri/abc.txt");
    }
}
