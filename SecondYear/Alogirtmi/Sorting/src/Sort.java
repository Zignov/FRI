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

        static void visualizeQuick(Array arr, int left, int right, int pivot){

            StringBuilder sb = new StringBuilder();

            for(int i = left; i <= right; i++){
                if(i==pivot){
                    if (i>left) sb.append("| ");
                    sb.append(arr.get(i));
                    if (i<right) sb.append(" |");
                }
                else{
                    sb.append(arr.get(i));
                }
                if(i<right){
                    sb.append(' ');
                }
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
        Utils.reset();
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
        }
    }


    //Z zlivanjem

    public static Array combine (Array left, Array right, boolean asc, boolean trace){
        Array result = new Array();

        int l = 0;
        int r = 0;

        int sizeL = left.size();
        int sizeR = right.size();

        while(l<sizeL && r<sizeR){

            Utils.plusPrimerjav();
            Utils.plusPrimerjav();

            int a = left.get(l);
            int b = right.get(r);

            if(asc){
                if(a<=b){
                    result.add(a);
                    l++;
                }
                else{
                    result.add(b);
                    r++;
                }

            }
            else{
                if(a>=b){
                    result.add(a);
                    l++;
                }
                else{
                    result.add(b);
                    r++;
                }
            }
            Utils.plusPrimerjav();
            Utils.plusPremik();
        }

        while (l<sizeL){
            result.add(left.get(l));
            Utils.plusPremik();
            l++;
        }

        while (r<sizeR){
            result.add(right.get(r));
            Utils.plusPremik();
            r++;
        }

        //if(trace) Utils.visualize(result, result.size());

        return result;
    }

    public static Array subArr(Array arr, int start, int end){
        Array result = new Array();

        for(int i = start; i<end; i++){
            result.add(arr.get(i));
        }

        return result;
    }


    public static Array merge(Array arr, boolean asc, boolean trace){
        int size = arr.size();

        if(size<=1){
            return arr;
        }

        int middle = (size + 1) / 2;

        if(trace) Utils.visualize(arr, middle);

        Array left = subArr(arr, 0, middle);
        Array right = subArr(arr, middle, size);

        left = merge(left, asc, trace);
        right = merge(right, asc, trace);

        Array result = combine(left, right, asc, trace);
        if (trace) Utils.visualize(result, -1);
        return result;
    }



    //quicksort
    public static int partition(Array arr, int left, int right, boolean asc, boolean trace) {
        int p = arr.get(left);
        int l = left, r = right + 1;


        while (true) {
            if (asc) {
                do {
                    l++;
                }
                while (l < right && arr.get(l) < p );

                do {
                    r--;
                }
                while (arr.get(r) > p);


                if (l >= r) {
                    break;
                }

                Utils.swap(arr, l, r);
            } else {
                do {
                    l++;
                }
                while (arr.get(l) > p && l < right);

                do {
                    r--;
                }
                while (arr.get(r) < p);


                if (l >= r) {
                    break;
                }

                Utils.swap(arr, l, r);
            }
        }
        Utils.swap(arr, left, r);

        return r;
    }

        public static void quick(Array arr, boolean asc, boolean trace){
            quick(arr, 0, arr.size()-1, asc, trace);

            if(trace){
                Utils.visualize(arr, -1);
            }
        }


        public static void quick(Array arr,int left, int right, boolean asc, boolean trace){
            if(left>=right){
                return;
            }

            int r = partition(arr, left, right, asc, trace);

            if(trace) Utils.visualizeQuick(arr, left, right, r);


            quick(arr, left, r-1, asc, trace);
            quick(arr, r+1, right, asc, trace);

        }



        //korensko urejanje


        public static void radix(Array arr, boolean asc, boolean trace){

            int size = arr.size();
            int max = 0;
            Utils.reset();

            for(int i = 0; i<size; i++){
                if(arr.get(i) > max){
                    max = arr.get(i);
                }
                Utils.plusPrimerjav();
            }

            for(int exp = 1; max/exp > 0; exp *= 10){
                sortByDigit(arr, exp, asc);

                if(trace) Utils.visualize(arr, -1);
            }
        }

        public static void sortByDigit(Array arr, int exp, boolean asc){
            int size = arr.size();

            int [] out = new int[size];
            int [] count = new int[10];

            for(int i = 0; i<size; i++){
                int digit = (arr.get(i) / exp) % 10;
                count[digit]++;
            }

            for(int i = 1; i < 10; i++){
                count[i] += count[i-1];
            }


            if(asc) {
                for (int i = size - 1; i >= 0; i--) {
                    int val = arr.get(i);

                    int digit = (val / exp) % 10;

                    out[count[digit] - 1] = val;
                    count[digit]--;
                }
            }
            else{
                for (int i = 0; i <size; i++) {
                    int val = arr.get(i);

                    int digit = (val / exp) % 10;

                    out[size - count[digit]] = val;
                    count[digit]--;
                }
            }


            for (int i = 0; i < size; i++) {
                arr.set(i, out[i]);
                Utils.plusPremik();
            }
        }


        //korensko
        public static void bucket(Array arr, boolean asc, boolean trace){





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
        Sort.radix(arr, asc, trace);
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
