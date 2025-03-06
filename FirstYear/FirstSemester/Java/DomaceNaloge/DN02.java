public class DN02 {
    public static void main (String[] args){
        if (args.length!=4){
            System.out.println("Napaka");
        }

        else{
            int s = Integer.parseInt(args[0]);
            int v = Integer.parseInt(args[1]);
            int x = Integer.parseInt(args[2]);
            int y = Integer.parseInt(args[3]);

            for (int i = 0; i<y;i++) {
                polna(s, x);
                System.out.println();
                for (int j = 0; j<v-2; j++) {
                    prazna(s, x);
                    System.out.println();
                }
            }
            polna(s, x);
        }
    }

    static void polna(int s, int x) {
        for (int j = 0; j < x; j++) {
            for (int i = 0; i < s - 1; i++) {
                System.out.print("*");
            }
        }
        System.out.print("*");
    }

    static void prazna(int s, int x){
        for (int j = 0; j<x+1;j++){
            System.out.print("*");
            for (int i = 0; i<(s-2);i++){
                System.out.print(" ");
            }
        }
    }
}
