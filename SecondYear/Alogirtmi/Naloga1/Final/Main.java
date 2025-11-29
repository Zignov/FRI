


public class Main {

    public static final int ponovitve = 100000;

    public static int[] generateTable(int n){
        int[] tabela = new int[n];

        for(int i = 0; i<n; i++){
            //System.out.println(i);
            tabela[i] = i+1;
        }
        return tabela;
    }


    public static int findLinear(int[] a, int v){
        for(int i = 0; i<a.length; i++){
            if(a[i] == v){
                return i;
            }
        }
        return -1;
    }


    public static int findBinary(int[] a, int v){
        int l = 0;
        int r = a.length - 1;

        while(l<=r){
            int m = (l+r)/2;
            int temp = a[m];
            //System.out.println(m);
            if(temp == v){
                return m;
            } else if (temp < v) {
                l = m+1;
            }
            else{
                r = m-1;
            }
        }
        return -1;
    }


    public static long timeLinear(int n){
        int[] tabela = generateTable(n);
        int[] iskane = new int[ponovitve];

        for(int i = 0; i<ponovitve; i++){
            iskane[i] = (int)((Math.random()*n)+1);
        }

        int ses = 0;
        long zacetek = System.nanoTime();

        for(int i = 0; i<ponovitve; i++){

            ses += findLinear(tabela, iskane[i]);
        }
        long konec = System.nanoTime();
        return (konec - zacetek)/ponovitve  ;
    }

    public static long timeBinary(int n){
        int[] tabela = generateTable(n);
        int[] iskane = new int[ponovitve];

        for(int i = 0; i<ponovitve; i++){
            iskane[i] = (int)((Math.random()*n)+1);
        }

        int ses = 0;
        long zacetek = System.nanoTime();

        for(int i = 0; i<ponovitve; i++){

            ses += findBinary(tabela, iskane[i]);
        }
        long konec = System.nanoTime();
        return (konec - zacetek)/ponovitve  ;
    }




    public static void main(String[] args) {


        //System.out.printf("lin: %d \n", findLinear(test, 33));
        //System.out.printf("bin: %d", findBinary(test, 33));


        System.out.println("      n      |    linearno   |      binarno     |");
        System.out.println("=========================================================");
        for(int n = 20000; n<=100000; n+=20000){
            System.out.printf("   %d     |      %d     |        %d       |\n", n, timeLinear(n), timeBinary(n));
        }

    }
}