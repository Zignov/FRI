//package izpiti;
//
//import java.io.File;
//import java.util.*;
//
//public class Drzave {
//
//
//
//    public static void branje(String vhod1, String vhod2) {
//        try {
//            Scanner sc = new Scanner(new File(vhod1));
//            Scanner sc2 = new Scanner(new File(vhod2));
//
//            TreeMap<String, ArrayList> skupaj = new TreeMap<>();
//
//            while(sc.hasNextLine()){
//
//                String[] ino = sc.nextLine().split(";");
//                ArrayList<String> in = new ArrayList<>(Arrays.asList(ino));
//
//                skupaj.put(in.get(0), in);
//            }
//            sc.close();
//            while(sc2.hasNextLine()){
//                String[] ino = sc2.nextLine().split(";");
//                ArrayList<String> in = new ArrayList<>(Arrays.asList(ino));
//
//                skupaj.put(in.get(0), skupaj.get(in.get(0)).addAll(in));
//            }
//
//
//        }
//        catch (Exception e){
//
//        }
//
//
//    }
//}
