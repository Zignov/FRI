//package izpiti;
//
//import java.util.HashMap;
//import java.util.Scanner;
//import java.util.TreeMap;
//import java.io.File;
//
//public class Medalje {
//
//    public class Drzava{
//        String kratica;
//        String mesto;
//        int prebivalstvo;
//
//
//        public Drzava(String kratica, String mesto, int prebivalstvo) {
//            this.kratica = kratica;
//            this.mesto = mesto;
//            this.prebivalstvo = prebivalstvo;
//        }
//
//        public String getKratica() {
//            return kratica;
//        }
//
//        public void setKratica(String kratica) {
//            this.kratica = kratica;
//        }
//
//        public String getMesto() {
//            return mesto;
//        }
//
//        public void setMesto(String mesto) {
//            this.mesto = mesto;
//        }
//
//        public int getPrebivalstvo() {
//            return prebivalstvo;
//        }
//
//        public void setPrebivalstvo(int prebivalstvo) {
//            this.prebivalstvo = prebivalstvo;
//        }
//    }
//
//    public static TreeMap<String, String> preberiDrzave(String imeDatoteke, String imeDat){
//
//        TreeMap<String, String> rez = new TreeMap<>();
//
//        try{
//            Scanner sc = new Scanner(new File(imeDatoteke));
//
//            while (sc.hasNextLine()){
//
//                String zac = sc.nextLine();
//
//                rez.put(zac.split(":")[0], zac);
//            }
//
//            sc.close();
//
//            Scanner sc2 = new Scanner(new File(imeDat));
//
//            while(sc2.hasNextLine()){
//
//            }
//        }
//        catch (Exception e){
//
//        }
//
//
//
//
//    }
//
//
//
//
//}
