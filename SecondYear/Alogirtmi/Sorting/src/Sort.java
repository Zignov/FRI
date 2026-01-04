import java.util.Scanner;

public class Sort {

    //branje
    public static Array readInput(Scanner sc){
        //Scanner sc = new Scanner(System.in);
        Array arr = new Array();

        String line = "";
        while (line.isBlank() && sc.hasNextLine()) {
            line = sc.nextLine();
        }

        if (line.isBlank()) return arr;

        String[] parts = line.trim().split("\\s+");
        for (String p : parts) {
            arr.add(Integer.parseInt(p));
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
                if(i == pivot){
                    sb.append("| ").append(arr.get(i)).append(" |");
                } else {
                    sb.append(arr.get(i));
                }
                if(i < right) sb.append(' ');
            }

            System.out.println(sb.toString());
        }
    }


    private static Array copyArray(Array a){
        Array b = new Array();
        for(int i = 0; i<a.size(); i++){
            b.add(a.get(i));
        }
        return b;
    }


    private static void resverse(Array a){
        int i = 0;
        int size = a.size()-1;

        while(i<size){
            int tmp = a.get(i);
            a.set(i, a.get(size));
            a.set(size, tmp);
            i++;
            size--;
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
            Utils.plusPremik();
            int j = i;

            if(asc) {
                while (j>0) {
                    Utils.plusPrimerjav();
                    if (arr.get(j-1) <= a) break;

                    //Utils.plusPrimerjav();
                    //int prev = arr.get(j-1);

                    arr.set(j, arr.get(j-1));
                    Utils.plusPremik();
                    //if (prev <= a) break;
                    j--;
                }
            }

            else{
                while (j>0) {
                    Utils.plusPrimerjav();
                    if (arr.get(j-1) >= a) break;

                    arr.set(j, arr.get(j-1));
                    Utils.plusPrimerjav();

                    j--;
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


            Utils.swap(arr, i, m);


            if(trace) Utils.visualize(arr, i+1);
        }
    }


    //bubble (izboljsana zamenjava)
    public static void bubble(Array arr, boolean asc, boolean trace){
        int velikost = arr.size();
        Utils.reset();
        //int pipe = -1;

        if (trace) Utils.visualize(arr, -1);

        for(int i = 0; i<=velikost-2; ){
            boolean zamenjano = false;
            int zadnjaZamenjava = i;


            for(int j = velikost-1; j > i; j--){

                Utils.plusPrimerjav();

                int left = arr.get(j-1);
                int right = arr.get(j);

                boolean neUrejeno =
                        (asc && left>right) || (!asc && left<right);

                if(neUrejeno){

                    Utils.swap(arr, j-1, j);
                    zamenjano = true;
                    zadnjaZamenjava = j-1;
                }
            }

            i = zadnjaZamenjava + 1;


            if(!zamenjano) {
                if(trace && asc) Utils.visualize(arr, velikost-1);
                else if (trace) {
                    Utils.visualize(arr, i);
                }
                break;
            }
            else{
                if(trace) Utils.visualize(arr, i);
            }


            /*if(trace) {
                if(asc){
                    Utils.visualize(arr, i+2);
                }
                else{
                    Utils.visualize(arr, i+1);
                }
            }

            if(trace && asc && i == velikost -2){
                Utils.visualize(arr,velikost-1);
            }*/
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
                        (!asc && arr.get(right) < arr.get(best))){
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


    //Z zlivanjem

    public static Array combine (Array left, Array right, boolean asc, boolean trace){
        Array result = new Array();

        int l = 0;
        int r = 0;

        int sizeL = left.size();
        int sizeR = right.size();

        while(l<sizeL && r<sizeR){


            int a = left.get(l);
            int b = right.get(r);

            Utils.plusPrimerjav();


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
            Utils.plusPremik();
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
        Utils.plusPremik();
        int l = left, r = right + 1;

        while (true) {
            if (asc) {
                do {
                    l++;
                    if(l<=right) Utils.plusPrimerjav();
                } while (l <= right && arr.get(l) < p);

                do {
                    r--;
                    //if(r==left) break;
                    Utils.plusPrimerjav();
                } while (arr.get(r) > p);

            } else {
                do {
                    l++;
                    if(l <= right) Utils.plusPrimerjav();
                } while (l <= right && arr.get(l) > p);

                do {
                    r--;
                    //if(r==left) break;
                    Utils.plusPrimerjav();
                } while (arr.get(r) < p);
            }

            //Utils.plusPrimerjav();
            if (l >= r) break;
            Utils.swap(arr, l, r);
        }

        Utils.swap(arr, left, r);
        return r;
    }

        public static void quick(Array arr, boolean asc, boolean trace){
            Utils.reset();

            if(trace){
                Utils.visualize(arr, -1);
            }

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

            //if(trace) Utils.visualize(arr, -1);

            for(int i = 0; i<size; i++){
                if(arr.get(i) > max){
                    max = arr.get(i);
                }
                //Utils.plusPrimerjav();
            }

            if(trace)Utils.visualize(arr, -1);


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
                Utils.plusPrimerjav();
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
                    Utils.plusPrimerjav();
                    Utils.plusPremik();
                }
            }
            else{
                for (int i = 0; i <size; i++) {
                    int val = arr.get(i);

                    int digit = (val / exp) % 10;

                    out[size - count[digit]] = val;
                    count[digit]--;
                    Utils.plusPrimerjav();
                    Utils.plusPremik();
                }
            }


            for (int i = 0; i < size; i++) {
                arr.set(i, out[i]);
                Utils.plusPremik();
            }
        }





        //korensko
        //public static void bucket(Array arr, boolean asc, boolean trace){





        //}


    private static String stetje(String mode, Array arr, boolean asc){
        Utils.reset();

        switch (mode) {
            case "insert":
                insertion(arr, asc, false);
                break;
            case "select":
            case "selection":
                selection(arr, asc, false);
                break;
            case "bubble":
                bubble(arr, asc, false);
                break;
            case "heap":
                heap(arr, asc, false);
                break;
            case "merge":
                arr = merge(arr, asc, false);
                break;
            case "quick":
                quick(arr, asc, false);
                break;
            case "radix":
                radix(arr, asc, false);
                break;
            default:
                System.out.println("Error");
                System.exit(0);
        }

        return Utils.stevecPremikov + " " + Utils.stevecPrimerjav;
    }


    public static void main(String[] args){

        //Branje commanda
        boolean asc = false, trace = false, count = false;
        Scanner sc = new Scanner(System.in);

        String[] cmds = sc.nextLine().trim().split("\\s+");
        Array arr = readInput(sc);
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


        if(count){
            Array a1 = copyArray(arr);
            String s1 = stetje(mode, a1, asc);

            Array a2;
            Array a3;

            if(mode.equals("merge")){
                Array sorted = merge(copyArray(arr), asc, false);
                a2 = copyArray(sorted);
                a3 = copyArray(sorted);
            }
            else{
                a2 = copyArray(a1);
                a3 = copyArray(a1);
            }

            String s2 = stetje(mode, a2, asc);
            resverse(a3);

            String s3 = stetje(mode, a3, asc);

            System.out.println(s1 + " | " + s2 + " | " + s3);
            return;
        }



        //System.out.printf("Trace: \s, mode: \s, asc: \s", trace, mode, asc);

        switch (mode) {

            case "insert":
                insertion(arr, asc, trace);
                break;

            case "select":
                selection(arr, asc, trace);
                break;

            case "bubble":
                bubble(arr, asc, trace);
                break;

            case "heap":
                heap(arr, asc, trace);
                break;

            case "merge":
                if(trace) Utils.visualize(arr, -1);
                arr = merge(arr, asc, trace); // merge returns a new Array
                break;

            case "quick":
                quick(arr, asc, trace);
                break;

            case "radix":
                radix(arr, asc, trace);
                break;

            case "bucket":
                //bucket(arr, asc, trace);
                break;

            default:
                System.out.println("Error");
                System.exit(0);
        }


        //System.out.println(arr.toString());
        //Sort.radix(arr, asc, trace);
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
