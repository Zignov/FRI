package DomaceNaloge;

import java.io.File;
import java.util.Scanner;

public class DN07 {




    public Planet[] preberi (String vir) {
        Scanner sc = null;
        Planet[] seznam = new Planet[8];
        int stevec = 0;
        try {
            sc = new Scanner(new File(vir));
            while (sc.hasNextLine()) {
                String vrsica = sc.nextLine();
                String ime = vrsica.split(":")[0];
                int radij = Integer.parseInt(vrsica.split(":")[1]);

                seznam[stevec] = new Planet(ime, radij);
                stevec++;
            }

            sc.close();
            return seznam;
        }
        catch (Exception e) {
            return null;
        }
    }


    public void sestevek(String[] imena, Planet[] seznam, String ime){
        double sestevek = 0;
        for(int i = 0; i<seznam.length; i++){
            for(int j = 0; j< imena.length; j++){
                if(seznam[i].getIme().equalsIgnoreCase(imena[j])){
                    //System.out.print(seznam[i].getIme() + " ");
                    //System.out.println(seznam[i].getRadij());
                    sestevek += seznam[i].povrsina();
                }
            }
        }
        if(sestevek != 0){
            System.out.printf("Povrsina planetov \"%s\" je %.0f milijonov km2",ime, sestevek/1000000);
        }
    }


    public static void main (String[]args){
        DN07 dn = new DN07();
        Planet[] seznam = dn.preberi(args[0]);

        dn.sestevek(args[1].split("\\+"), seznam, args[1]);
    }
}

class Planet{
    private String ime;

    public int getRadij() {
        return radij;
    }

    public String getIme() {
        return ime;
    }

    private int radij;

    public Planet(String ime, int radij) {
        this.ime = ime;
        this.radij = radij;
    }


    public double povrsina(){
        return (4 * Math.PI * radij * radij);
    }
}
