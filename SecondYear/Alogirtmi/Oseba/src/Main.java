
import java.util.Random;
import java.util.Scanner;



public class Main {

    public static class Oseba implements Comparable{
        public String ime;
        public String priimek;
        public int letoR;


        Random rng = new Random();

        public static int smer = 1;
        public static int atribut = 0;

        private static final String[] imena = {"Ana", "Boris", "Cene", "Dora", "Eva", "Filip", "Gaja", "Hana",
                "Igor", "Jure", "Klara", "Luka", "Maja", "Nejc", "Ožbej", "Pia"};


        private static final String[] priimki = {"Novak", "Horvat", "Kovač", "Zupan", "Kralj", "Krajnc", "Potočnik", "Vidmar",
                "Mlakar", "Golob", "Turk", "Božič", "Kastelic", "Koren", "Kovačič", "Rozman"};




        public Oseba(String ime, String priimek, int letoR){
            this.ime = ime;
            this.priimek = priimek;
            this.letoR = letoR;
        }

        public Oseba(){
            this.ime = imena[rng.nextInt(imena.length)];
            this.priimek = priimki[rng.nextInt(priimki.length)];
            this.letoR = 1950 + rng.nextInt(75);
        }


        public String izpis(){
            return priimek + ' ' + ime + " (" + letoR + ") ";
        }

        @Override
        public String toString(){
            String rez;

            switch(atribut){
                case 0:
                    rez = priimek;
                    break;
                case 1:
                    rez = ime;
                    break;
                case 2:
                    rez = String.valueOf(letoR);
                    break;
                default:
                    rez = priimek;
                    break;
            }
            return rez;
        }


        @Override
        public int compareTo(Object o){
            Oseba druga = (Oseba) o;

            switch(atribut){
                case 0:
                    return this.priimek.compareTo(druga.priimek);

                case 1:
                    return this.ime.compareTo(druga.ime);

                case 2:
                    return Integer.compare(this.letoR, druga.letoR);

                default:
                    return this.priimek.compareTo(druga.priimek);

            }
        }
    }



    public static class Urejanje{
        public static void bubbleSort(Comparable[] a){
            int dolzina = a.length;

            if(dolzina <= 1) return;

            int konec = dolzina - 1;

            while (konec > 0){
                int zadnja = -1;

                for(int j = 0; j<konec; j++){
                    int primerjava = a[j].compareTo(a[j+1]);


                    //primerjava * smer, prov obrne stvar.
                    if(Oseba.smer * primerjava > 0){
                        Comparable tmp = a[j];

                        a[j] = a[j+1];
                        a[j+1] = tmp;

                        zadnja = j;
                    }
                }



                if(zadnja == -1){
                    izpisiSled(a, -1);
                    break;
                }
                else{
                    konec = zadnja;
                    izpisiSled(a, konec);
                }
            }



        }


        private static void izpisiSled(Comparable[] a, int konec){
            StringBuilder sb = new StringBuilder();

            if(konec < 0){
                sb.append("| ");
                for(int i = 0; i<a.length; i++){
                    sb.append(a[i]);
                    if(i<a.length-1){
                        sb.append(" ");
                    }
                }

                System.out.println(sb);
                return;
            }

            for(int i = 0; i<a.length; i++){
                sb.append(a[i]);

                if(i == konec){
                    sb.append(" |");
                }

                if(i<a.length - 1){
                    sb.append(" ");
                }
            }

            System.out.println(sb);
        }
    }

    private static void kopirajPolje(Oseba[] src, Oseba[] dst){

        for(int i = 0; i<src.length; i++){
            dst[i] = src[i];
        }
    }


    public class Testi{


        private static void izpisPolij(Oseba[] t){
            for(int i = 0; i<t.length; i++){
                System.out.print(t[i]);
                if(i<t.length-1){
                    System.out.print(" ");
                }
            }
        }

        private static void izpisiPodrobno(Oseba[] t){
            for(int i = 0; i<t.length; i++){
                System.out.printf("%2d: %s%n", i, t[i].izpis());
            }
        }

    }



    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);





        System.out.println("Vnesite velikost n: ");
        int n = sc.nextInt();

        Oseba[] tt = new Oseba[n];
        for(int i = 0; i<n; i++){
            tt[i] = new Oseba();
        }


        while (true){
            Oseba[] t = new Oseba[n];
            kopirajPolje(tt, t);


            System.out.println();
            System.out.println("Izberi atribut: 0=priimek, 1=ime, 2=letoR");
            Oseba.atribut = sc.nextInt();


            System.out.println();
            System.out.println("Polje t:");
            for(int i = 0; i<t.length; i++){
                System.out.print(t[i]);
                if(i<t.length - 1){
                    System.out.print(" ");
                }
            }
            System.out.println();



            System.out.println("Izberi smer (smer): 1=narascajoce, -1=padajoce");
            System.out.print("smer = ");
            Oseba.smer = sc.nextInt();


            Urejanje.bubbleSort(t);


            System.out.println("Urejeno:");
            for (int i = 0; i < t.length; i++) {
                System.out.print(t[i]);
                if (i < t.length - 1) System.out.print(" ");
            }
            System.out.println();

            System.out.print("Izberi ponovitev ali konec (1=ponovi, 0=konec): ");
            int izbira = sc.nextInt();
            if (izbira == 0) break;
        }

        sc.close();
    }
}