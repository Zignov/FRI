import java.util.Scanner;

public class Sort {

    //branje
    public static Array readInput(){
        Scanner sc = new Scanner(System.in);
        Array arr = new Array();

        String branje = sc.nextLine();
        String[] deli = branje.trim().split("\\s+");


        for (int i = 0; i<deli.length; i++){
            arr.add(Integer.parseInt(deli[i]));
        }

        return arr;
    }


    //pomoci
    static class Utils{
        static int stevecPremikov = 0;
        static int stevecPrimerjav = 0;

        static void reset(){
            stevecPremikov = 0;
            stevecPrimerjav = 0;
        }

        static void plusPremik(){
            stevecPremikov++;
        }

        static void plusPrimerjav(){
            stevecPrimerjav++;
        }

        static void swap(Array arr, int i, int j){
            int tmp = arr.get(i);
            arr.set(i, arr.get(j));
            arr.set(j, tmp);

            stevecPremikov += 3;
        }

        static void visualize(Array arr, int sortedSize){
            StringBuilder sb = new StringBuilder();
            int size = arr.size();

            for(int i = 0; i < size; i++){

                if (i == sortedSize){
                    sb.append("| ");
                }
                sb.append(arr.get(i)+" ");
            }

            if (sortedSize == size){
                sb.append("|");
            }

            System.out.println(sb.toString());
        }
    }


    //vstavljanje
    public static void insertion(Array arr, boolean asc, boolean trace){
        int velikost = arr.size();
        Utils.reset();

        if(trace){
            Utils.visualize(arr, -1);
        }

        for(int i = 1; i < velikost; i++){
            int a = arr.get(i);
            int j = i;

            if(asc) {
                while ((j > 0) && (arr.get(j - 1) > a)) {
                    arr.set(j, arr.get(j - 1));
                    Utils.plusPremik();
                    j--;

                    Utils.plusPrimerjav();
                    Utils.plusPrimerjav();

                }
            }

            else{
                while ((j > 0) && (arr.get(j - 1) < a)) {
                    arr.set(j, arr.get(j - 1));
                    Utils.plusPremik();
                    j--;

                    Utils.plusPrimerjav();
                    Utils.plusPrimerjav();

                }
            }

            arr.set(j, a);
            Utils.plusPremik();

            if(trace){
                Utils.visualize(arr, i+1);
            }
        }
    }


    //izbiranje
    public static void selection(Array arr, boolean asc, boolean trace){
        int velikost = arr.size();
        Utils.reset();

        if (trace) Utils.visualize(arr, -1);

        for(int i = 0; i<=velikost-2; i++){
            int m = i;

            for(int j = i+1; j<=velikost-1; j++){
                if(asc && (arr.get(j) < arr.get(m))){
                    m = j;

                } else if (!asc && (arr.get(j) > arr.get(m))) {
                    m = j;
                }
                Utils.plusPrimerjav();
            }

            if(m != i) {
                Utils.plusPrimerjav();
                Utils.swap(arr, i, m);
            }

            if(trace) Utils.visualize(arr, i+1);
        }
    }


    //bubble (izboljsana zamenjava)
    public static void bubble(Array arr, boolean asc, boolean trace){
        int velikost = arr.size();
        Utils.reset();
        int pipe = -1;

        if (trace) Utils.visualize(arr, pipe);

        for(int i = 0; i<=velikost-2; i++){
            boolean zamenjano = false;



            for(int j = velikost-1; j > i; j--){

                Utils.plusPrimerjav();

                int left = arr.get(j-1);
                int right = arr.get(j);

                boolean neUrejeno =
                        (asc && left>right) || (!asc && left<right);

                if(neUrejeno){
                    pipe = j;
                    Utils.swap(arr, j-1, j);
                    zamenjano = true;
                }
            }

            if(!zamenjano) break;

            if(trace) Utils.visualize(arr, pipe);
        }
    }



    //kopice
    public static void heapify(Array arr, int heapSize, int i, boolean asc){
        while (true){
            int best = i;
            int left = 2*i +1;
            int right = 2*i+2;


            if(left<heapSize){
                Utils.plusPrimerjav();

                if((asc && arr.get(left) > arr.get(best)) ||
                        (!asc && arr.get(left) < arr.get(best))){
                    best = left;
                }
            }

            if(right<heapSize){
                Utils.plusPrimerjav();

                if((asc && arr.get(right) > arr.get(best)) ||
                        (!asc && arr.get(left) < arr.get(best))){
                    best = right;
                }
            }

            if (best == i) break;
            Utils.swap(arr, i ,best);
            i = best;
        }
    }


    public static void heap(Array arr, boolean asc, boolean trace){
        int size = arr.size();
        Utils.reset();

        if (trace) Utils.visualize(arr,-1);

        for(int i = size/2-1; i>=0; i--){
            heapify(arr, size, i, asc);
        }

        if (trace) Utils.visualize(arr, size);


        for(int zadnja = size -1; zadnja > 0; zadnja--){
            Utils.swap(arr, 0, zadnja);

            heapify(arr, zadnja, 0, asc);

            if(trace) Utils.visualize(arr, zadnja);
        }
    }






    public static void main(String[] args){

        //Branje commanda
        boolean asc = false, trace = false, count = false;
        Scanner sc = new Scanner(System.in);

        String[] cmds = sc.nextLine().trim().split("\\s+");
        String mode = cmds [1];

        if (cmds[0].equals("trace")){
            trace = true;
        } else if (cmds[0].equals("count")) {
            count = true;
        }
        else{
            System.out.println("Error");
            System.exit(0);
        }


        if (cmds[2].equals("up")){
            asc = true;
        } else if (cmds[2].equals("down")) {
            asc = false;
        }
        else{
            System.out.println("Error");
            System.exit(0);
        }



        Array arr = readInput();
        System.out.println();
        //System.out.println(arr.toString());
        Sort.heap(arr, asc, trace);
        //System.out.println(arr.toString());
    }
}



class Array{

    private int[] data = new int[16];
    private int size = 0;

    public void add(int x){
        if (size == data.length){
            resize();
        }

        data[size++] = x;
    }

    public void resize(){
        int [] tmp = new int[data.length*2];
        for(int i = 0; i < size; i++){
            tmp[i] = data[i];
        }

        data = tmp;
    }

    public int size(){
        return(size);
    }

    public int get(int i){
        return(data[i]);
    }

    public void set(int index, int j){
        data[index] = j;
    }


    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        sb.append('[');

        for(int i = 0; i < size; i++){
            if(i > 0){
                sb.append(", ");
            }
            sb.append(data[i]);
        }
        sb.append(']');

        return sb.toString();
    }
}
