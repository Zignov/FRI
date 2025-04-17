package vaje.dars.aplikacija;

import vaje.dars.vinjete.SeznamVinjet;

public class Kontrola {


    public static void main(String[]args){
        //SeznamVinjet.preberiPodatke("vir/vinjete.txt");
        SeznamVinjet sv = new SeznamVinjet();
        if(!sv.preberiPodatke("FirstYear/SecondSemester/Java/vaje/dars/vir/vinjete.txt")){
            System.exit(0);
        }

        //sv.izpisiVinjete();
        //System.out.print(sv.preveriVinjeto("MSGG69"));
        //sv.izpisiVinjete("letna");
        sv.izpisiLetneVeljavnosti();

    }
}
