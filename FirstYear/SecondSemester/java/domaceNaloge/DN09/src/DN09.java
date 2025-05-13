import java.io.File;
import java.util.Scanner;

public class DN09 {


    public Postaja[] postaje;
    public Linija[] linije;
    public Avtobus[] avtobusi;


    public void izpisi(){
        for(int i = 0; i<linije.length; i++){
            System.out.println(linije[i].toString());
        }
    }


    public static void main(String[] args) {
        File Datoteka;
        try {
            Datoteka = new File(args[0]);
        }
        catch (Exception e){
            System.out.println(args[0]);
            System.out.println("Napaka pri odpiranju");
            System.exit(1);
            return;
        }
        Scanner sc = null;

        try {
            sc = new Scanner(Datoteka);
            DN09 dn09 = new DN09();

            String[] prva = sc.nextLine().split(",");
            int[] stevila = new int[prva.length];

            for(int i = 0; i < prva.length; i++){
                stevila[i] = Integer.parseInt(prva[i]);
            }

            dn09.postaje = new Postaja[stevila[0]];
            dn09.linije = new Linija[stevila[1]];
            dn09.avtobusi = new Avtobus[stevila[2]];

            sc.nextLine();
            for(int i = 0; i<stevila[0]; i++){
                String vrstica = sc.nextLine();

                String[] podatki = vrstica.split(",");
                int id = Integer.parseInt(podatki[0]);
                String ime = podatki[1];
                int x = Integer.parseInt(podatki[2]);
                int y = Integer.parseInt(podatki[3]);
                String stringLinje = podatki[4];
                String[] avtobusi = new String[0];
                int cakajoci = Integer.parseInt(podatki[6]);

                if (!podatki[5].isEmpty()) {
                    avtobusi = podatki[5].split(";");
                    for (int j = 0; j < avtobusi.length; j++) {
                        int idAvtobusa = Integer.parseInt(avtobusi[j].split("\\(")[0]);
                        int stPotnikov = Integer.parseInt(avtobusi[j].split("\\(")[1].replace(")", ""));
                        Avtobus avtobus = new Avtobus(idAvtobusa, stPotnikov);
                        avtobus.setTrenutnaPostaja(new Postaja(id, ime, x, y, cakajoci));
                        dn09.avtobusi[j] = avtobus;
                    }
                }




                dn09.postaje[i] = new Postaja(id, ime, x, y, cakajoci);
            }

            sc.nextLine();

            for(int i = 0; i<stevila[1]; i++){
                String vrstica = sc.nextLine();

                String[] podatki = vrstica.split(",");
                int id = Integer.parseInt(podatki[0]);
                String barva = podatki[1];
                String[] avtobusi = podatki[2].split(";");
                String[] postaje = podatki[3].split("\\|");

                dn09.linije[i] = new Linija(id);
                dn09.linije[i].setBarva(barva);

                for (int j=0; j< avtobusi.length; j++){
                    for (int k=0; k<dn09.avtobusi.length; k++){
                        if (dn09.avtobusi[k] != null && dn09.avtobusi[k].getID() == Integer.parseInt(avtobusi[j])){
                            dn09.linije[i].dodajAvtobus(dn09.avtobusi[k]);
                        }
                    }
                }

                for (int j=0; j< postaje.length; j++){
                    for (int k=0; k<dn09.postaje.length; k++){
                        if (dn09.postaje[k] != null && dn09.postaje[k].getID() == Integer.parseInt(postaje[j])){
                            dn09.linije[i].dodajPostajo(dn09.postaje[k]);
                        }
                    }
                }

            }

            dn09.izpisi();

        }
        catch (Exception e){
            System.out.println(args[0] + " " + e.getMessage());
            System.out.println("Napaka pri odpiranju");
            System.exit(1);
            return;
        }
        finally {
            sc.close();
        }
    }
}

class Avtobus{
    int ID;
    int steviloPotnikov;
    Postaja trenutnaPostaja;

    public Avtobus(int ID, int steviloPotnikov) {
        this.ID = ID;
        this.steviloPotnikov = steviloPotnikov;
    }

    public int getSteviloPotnikov() {
        return steviloPotnikov;
    }

    public int getID() {
        return ID;
    }

    public Postaja getTrenutnaPostaja() {
        return trenutnaPostaja;
    }

    public void setTrenutnaPostaja(Postaja trenutnaPostaja) {
        this.trenutnaPostaja = trenutnaPostaja;
    }

    public String toString(){
        return String.format("<%d> (%d) - <%s>", getID(), getSteviloPotnikov(), getTrenutnaPostaja());
    }
}


class Postaja {
    int ID;
    String ime;
    int x;
    int y;
    int cakajoci;


    public Postaja(int ID, String ime, int x, int y, int cakajoci) {
        this.ID = ID;
        this.ime = ime;
        this.x = x;
        this.y = y;
        this.cakajoci = cakajoci;
    }

    public int getID() {
        return ID;
    }

    public String getIme() {

        return ime;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getCakajoci() {
        return cakajoci;
    }

    public String toString(){
        return String.format("<%d> <%s> [%d,%d] čakajoči: %d", getID(), getIme(), getX(), getY(), getCakajoci());
    }
}

class Linija{
    int id;
    String barva;
    Postaja[] postajeLinije = new Postaja[10];
    Avtobus[] avtobusiLinije = new Avtobus[5];

    public Linija(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public String getBarva() {
        return barva;
    }

    public Postaja[] getPostajeLinije() {
        return postajeLinije;
    }

    public Avtobus[] getAvtobusiLinije() {
        return avtobusiLinije;
    }

    public void setBarva(String barva) {
        this.barva = barva;
    }

    public boolean dodajPostajo(Postaja postaja){
        for (int i = 0; i < postajeLinije.length; i++) {
            if (postajeLinije[i] == null) {
                postajeLinije[i] = postaja;
                return true;
            }
        }
        return false;
    }

    public boolean dodajAvtobus(Avtobus avtobus){
        for (int i = 0; i < avtobusiLinije.length; i++) {
            if (avtobusiLinije[i] == null) {
                avtobusiLinije[i] = avtobus;
                return true;
            }
        }
        return false;
    }

    public String toString(){
        StringBuilder sb = new StringBuilder();
        sb.append("Linija ").append(getId()).append(" - ");

        String[] lokacije = new String[avtobusiLinije.length];

        for (int i = 0; i < avtobusiLinije.length; i++) {
            if (avtobusiLinije[i] != null && avtobusiLinije[i].getTrenutnaPostaja() != null) {
                lokacije[i] = avtobusiLinije[i].getTrenutnaPostaja().getIme();
            }
        }
        for (int i = 0; i <postajeLinije.length; i++){
            if (postajeLinije[i] != null) {
                String postaja = postajeLinije[i].getIme();
                sb.append(postaja);

                for (int j = 0;j<avtobusiLinije.length; j++){
                    /*if(avtobusiLinije[j] != null){
                        System.out.print("trenutna: ");
                        System.out.println(avtobusiLinije[j].getTrenutnaPostaja().getIme());
                    }
                    System.out.println(postajeLinije[i].getIme());*/

                    if (avtobusiLinije[j] != null && postajeLinije[i] != null && avtobusiLinije[j].getTrenutnaPostaja().getIme().equals(postajeLinije[i].getIme())) {
                        sb.append("(bus)");
                        break;
                    }
                }
                if (i < postajeLinije.length - 1 && postajeLinije[i + 1] != null) {
                    sb.append(" -> ");
                }
            }
        }

        return sb.toString();
    }

}