package izpiti;

import java.awt.image.AreaAveragingScaleFilter;
import java.util.ArrayList;
import java.util.Arrays;

public class Ponavljanje {

    public static String popraviBesedilo(String besedilo){


        StringBuilder sb = new StringBuilder();
        //System.out.println(besedilo.length());

        for(int i = 0; i<besedilo.length()-1; i++){

                //System.out.printf("i = %s, j = %s -> %b \n", besedilo.charAt(i), besedilo.charAt(i+1), besedilo.charAt(i) == besedilo.charAt(i+1));

                if(besedilo.charAt(i) == besedilo.charAt(i+1)){
                    continue;
                }
                else{
                    sb.append(besedilo.charAt(i));
                }


        }

        if (besedilo.charAt(besedilo.length() - 2) != besedilo.charAt(besedilo.length() - 1)) {
            sb.append(besedilo.charAt(besedilo.length() - 1));
        }



        String[] rez = String.valueOf(sb).split(" ");
        ArrayList<String> list = new ArrayList<>(Arrays.asList(rez));
        ArrayList<Integer> poz = new ArrayList<>();


        for(int i = 0; i<rez.length-1; i++){
            if(rez[i].equalsIgnoreCase(rez[i+1])){
                poz.add(i);
            }
        }

        for(int i = poz.size()-1; i>=0; i--){
            //System.out.println(poz.get(i));
            //System.out.println(list.get(poz.get(i)));
            list.remove((int) poz.get(i));
        }

        StringBuilder fin = new StringBuilder();

        //System.out.println(list);

        for(int i = 0; i<list.size(); i++){
            fin.append(list.get(i));
            fin.append(" ");
        }



        //System.out.println(poz);

        return String.valueOf(fin);

    }




    public static void main(String[] args){
        System.out.println(popraviBesedilo("Proggrammiranje mi mmii mii je jjje všeččč všeč"));

    }


}
