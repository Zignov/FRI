//package izpiti;
//
//import java.io.File;
//import java.util.ArrayList;
//import java.util.Collection;
//import java.util.HashMap;
//import java.util.Scanner;
//
//public class naloga11 {
//
//    public static String stetje(String v){
//        try{
//            File vhod = new File(v);
//            Scanner sc = new Scanner (vhod);
//
//            ArrayList<String> besede = new ArrayList<>();
//            HashMap<String, Integer> stevec = new HashMap<>();
//
//            while (sc.hasNextLine()){
//                String[] zac = sc.nextLine().split("/0");
//                for(int i = 0; i<zac.length; i++){
//                    besede.add(zac[i]);
//                }
//            }
//
//
//            for(int i = 0; i<besede.size(); i++){
//                if(stevec.containsKey(besede.get(i))){
//                    stevec.put(besede.get(i), stevec.get(besede.get(i)) + 1);
//                }
//                else{
//                    stevec.put(besede.get(i), 1);
//                }
//            }
//
//
//            System.out.println(stevec.values());
//        }
//        catch(Exception e){
//
//        }
//    }
//
//    public static void main(String []args){
//
//    }
//
//
//}
