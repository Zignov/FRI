package vaje.vaje10;

import java.io.File;
import java.util.*;

public class Dolgovi {

    List<Prijatelj> prijatelji = new ArrayList<>();
    File pri = new File("viri/Prijatelji.txt");
    File dol = new File("viri/Dolgovi.txt");

    public void preberiPrijatelje(File datoteka){
        try{
            Scanner sc = new Scanner(datoteka);
            while (sc.hasNextLine()){
                String vrstica = sc.nextLine();
                //System.out.println(vrstica);
                Prijatelj prijatelj = new Prijatelj(vrstica);
                prijatelji.add(prijatelj);

            }
            sc.close();
        }
        catch (Exception e){
            System.out.println("Napaka pri branju datoteke: " + e.getMessage());
        }
    }

    public void izpisi(){
        for (int i = 0; i < prijatelji.size(); i++) {
            System.out.println(prijatelji.get(i).toString() + " je dolznen/a: ");


            if(prijatelji.get(i).getDolgovi() != null){
                for (var vnos : prijatelji.get(i).getDolgovi().entrySet()) {
                    Prijatelj upnik = vnos.getKey();
                    double znesek = vnos.getValue();
                    System.out.println(" ---> " + upnik.toString() + ": " + znesek + " EUR");
                }
            }
        }
    }

    public Prijatelj najdiPrijatelja(String ime){
        for (int i = 0; i< prijatelji.size(); i++){
            if (prijatelji.get(i).ime.equals(ime)){
                return prijatelji.get(i);
            }
        }
        return null;
    }


    public void preberiDolgove (File datoteka){
        try{
            Scanner sc = new Scanner(datoteka);
            while (sc.hasNextLine()){
                String vrstica = sc.nextLine();
                String[] deli = vrstica.split(";");

                if(deli.length != 3){
                    continue;
                }
                String imeDolznik = deli[0];
                String imeUpnik = deli[1];
                double znesek = Double.parseDouble(deli[2]);

                if (znesek < 0){
                    String zacasno = imeDolznik;
                    imeDolznik = imeUpnik;
                    imeUpnik = zacasno;
                    znesek = -znesek;
                }

                Prijatelj dolznik = najdiPrijatelja(imeDolznik);
                Prijatelj upnik = najdiPrijatelja(imeUpnik);

                if (dolznik != null && upnik != null) {
                    dolznik.dodajDolg(upnik, znesek);
                }

            }
            sc.close();
        }
        catch (Exception e){}
    }


    public Set<Prijatelj> vrniBrezDolgov(){
        Set<Prijatelj> brezDolgov = new TreeSet<>();
        for (int i = 0; i < prijatelji.size(); i++) {
            if (prijatelji.get(i).getDolgovi().isEmpty()){
                brezDolgov.add(prijatelji.get(i));
            }
        }
        return brezDolgov;
    }

    public void izpisBrez(Set<Prijatelj> brez){
        for(var free : brez){
            System.out.println(free.toString());
        }
    }
}
