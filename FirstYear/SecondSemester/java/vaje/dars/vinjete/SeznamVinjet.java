package vaje.dars.vinjete;

import java.io.File;
import java.util.Scanner;

public class SeznamVinjet {

    private Vinjeta[] prodaneVinjete;

    public int dolzina;


    public boolean preberiPodatke(String vir){
        Scanner sc = null;
        try{
            //System.out.println(vir);
            sc = new Scanner(new File(vir));
            dolzina = Integer.parseInt(sc.nextLine());
            //System.out.println(dolzina);
            prodaneVinjete = new Vinjeta[dolzina];
            int stevec = 0;

            while (sc.hasNextLine()){
                if(stevec > dolzina){
                    return false;
                }
                String[] podatki = sc.nextLine().split(";");
                prodaneVinjete[stevec] = new Vinjeta((podatki[0]), (podatki[1]), (podatki[2]), (podatki[3]));
                stevec++;
            }
            sc.close();
            return true;
        }
        catch (Exception e){
            return false;
        }


    }

    public void izpisiVinjete(){
        for(int i = 0; i<dolzina; i++){
            System.out.println(prodaneVinjete[i].toString());
        }
    }


    public boolean preveriVinjeto(String registerska){
        for(int i = 0; i < dolzina; i++){
            String reg = prodaneVinjete[i].getRegisterska();
            if (reg.equals(registerska)){
                return true;
            }
        }
        return false;
    }

    public void izpisiVinjete(String tip) {
        int stevec = 0;
        for (int i = 0; i < dolzina; i++) {
            String vrsta = prodaneVinjete[i].getVrsta();
            if (vrsta.equals(tip)) {
                System.out.println(prodaneVinjete[i].toString());
                stevec++;
            }
        }
        if(stevec > 0) {
            System.out.printf("Stevilo vinjet tipa %s je: %d", tip, stevec);
        }
        else {
            System.out.print("Ni vinjet");
        }
    }


    public void izpisiLetneVeljavnosti() {
        for (int i = 0; i < dolzina; i++) {
            String vrsta = prodaneVinjete[i].getVrsta();
            String datum = prodaneVinjete[i].getDatum();
            if (vrsta.equals("letna")) {
                String reg = prodaneVinjete[i].toString();

                int novDatum = Integer.parseInt(datum.substring(6,10)) + 1;

                System.out.printf("%s: veljavna do %s%d", prodaneVinjete[i].getRegisterska(), datum.substring(0,6), novDatum);
                System.out.println();
            }
        }
    }

}
