public class cenik {
    public static void main(String[] args){
        double cena_kepice = 1.25;

        System.out.println("Stevilo kepic | Cena (EUR)");
        System.out.println("---------------------------");

        int i;
        for (i=1; i<=10; i ++){
            System.out.printf("%5d    |  %5.2f\n", i, i*cena_kepice);
        }
    }
}
