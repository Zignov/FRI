import java.util.Random;


class CollectionException extends Exception {
    public CollectionException(String msg) {
        super(msg);
    }
}
interface Collection {
    static final String ERR_MSG_EMPTY = "Collection is empty.";

    boolean isEmpty();
    int size();
    String toString();
}
interface Queue<T> extends Collection {
    T front() throws CollectionException;
    void enqueue(T x);
    T dequeue() throws CollectionException;
}
interface PriorityQueue<T extends Comparable> extends Queue<T> {
}


//neurejena.......
class ArrayPQ<T extends Comparable<T>> implements PriorityQueue<T> {
    private static final int DEFAULT_CAPACITY = 64;

    private T[] data;
    private int velikost;

    private static int poteze = 0;
    private static int primerjave = 0;

    public ArrayPQ(){
        this.data = (T[]) new Comparable[DEFAULT_CAPACITY];
        this.velikost = 0;
    }

    public ArrayPQ(int capacity){
        this.data = (T[]) new Comparable[capacity];
        this.velikost = 0;
    }

    //helpsss.......

    private void nastavi(int i, T vrednost){
        data[i] = vrednost;
        poteze++;
    }

    private int compare(T a, T b){
        primerjave++;
        return a.compareTo(b);
    }


    private void resize(){
        int novaVelikost = data.length * 2;
        T[] newData = (T[]) new Comparable[novaVelikost];
        for(int i = 0; i < velikost; i++){
            newData[i] = data[i];
            poteze++;
        }
        data = newData;
    }

    public static void reset(){
        poteze = 0;
        primerjave = 0;
    }

    public static int getPoteze(){
        return poteze;
    }

    public static int getPrimerjave(){
        return primerjave;
    }


    //Zbirka..........

    @Override
    public boolean isEmpty() {
        return velikost == 0;
    }

    @Override
    public int size() {
        return velikost;
    }

    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for(int i = 0; i < velikost; i++){
            sb.append(data[i]);
            if(i<velikost-1) sb.append(", ");
        }
        sb.append("]");
        return sb.toString();
    }


    //vrsta..........

    @Override
    public void enqueue(T x){
        if (velikost == data.length){
            resize();
        }
        nastavi(velikost, x);
        velikost++;
    }

    @Override
    public T front() throws CollectionException{
        if(isEmpty()){
            throw new CollectionException(ERR_MSG_EMPTY);
        }

        int max = 0;
        for(int i = 1; i<velikost; i++){
            if(compare(data[i], data[max]) > 0){
                max = i;
            }
        }
        return data[max];
    }

    @Override
    public T dequeue() throws CollectionException{
        if(isEmpty()){
            throw new CollectionException(ERR_MSG_EMPTY);
        }

        int index = 0;
        for(int i = 1; i<velikost; i++){
            if(compare(data[i], data[index]) > 0){
                index = i;
            }
        }

        T max = data[index];
        poteze++;

        nastavi(index, data[velikost-1]);

        data[velikost-1] = null;
        velikost--;

        return max;
    }
}


//implicitna.........
class ArrayHeapPQ<T extends Comparable<T>> implements PriorityQueue<T> {
    private static final int DEFAULT_CAPACITY = 64;

    private T[] kopica;
    private int velikost;
    private static int poteze = 0;
    private static int primerjave = 0;

    public ArrayHeapPQ(){
        this.kopica = (T[]) new Comparable[DEFAULT_CAPACITY];
        this.velikost = 0;
    }

    public ArrayHeapPQ(int capacity){
        this.kopica = (T[]) new Comparable[capacity];
        this.velikost = 0;
    }

    //helpsss......

    public void set (int i, T vrednost){
        kopica[i] = vrednost;
        poteze++;
    }

    private int compare(T a, T b){
        primerjave++;
        return a.compareTo(b);
    }

    private void resize(){
        int novaVelikost = kopica.length * 2;
        T[] novaKopica = (T[]) new Comparable[novaVelikost];
        for(int i = 0; i < velikost; i++){
            novaKopica[i] = kopica[i];
            poteze++;
        }
        kopica = novaKopica;
    }

    private void zamenjaj(int i, int j){
        T tmp = kopica[i];
        set(i, kopica[j]);
        set(j, tmp);
        poteze++;
    }

    private void bubbleUp(int i){
        while(i>0){
            int oce = (i-1)/2;
            if(compare(kopica[i], kopica[oce]) <= 0){
                break;
            }
            zamenjaj(i, oce);
            i = oce;
        }
    }

    private void bubbleDown(int i){
        while(true){
            int levi = 2*i+1;
            int desni = 2*i+2;
            int najvecji = i;

            if(levi < velikost && compare(kopica[levi], kopica[najvecji]) > 0){
                najvecji = levi;
            }
            if(desni < velikost && compare(kopica[desni], kopica[najvecji]) > 0){
                najvecji = desni;
            }

            if(najvecji == i){
                break;
            }

            zamenjaj(i, najvecji);
            i = najvecji;
        }
    }


    public static void reset(){
        poteze = 0;
        primerjave = 0;
    }

    public static int getPoteze(){
        return poteze;
    }

    public static int getPrimerjave(){
        return primerjave;
    }


    //Zbirka......

    @Override
    public boolean isEmpty() {
        return velikost == 0;
    }

    @Override
    public int size() {
        return velikost;
    }

    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for(int i = 0; i < velikost; i++){
            sb.append(kopica[i]);
            if(i<velikost-1) sb.append(", ");
        }
        sb.append("]");
        return sb.toString();
    }

    //Vrstaa.......

    @Override
    public void enqueue(T x){
        if (velikost == kopica.length){
            resize();
        }

        int index = velikost;
        set(index, x);
        velikost++;
        bubbleUp(index);
    }

    @Override
    public T front() throws CollectionException{
        if(isEmpty()){
            throw new CollectionException(ERR_MSG_EMPTY);
        }
        return kopica[0];
    }

    @Override
    public T dequeue() throws CollectionException{
        if(isEmpty()){
            throw new CollectionException(ERR_MSG_EMPTY);
        }

        T max = kopica[0];
        poteze++;

        if(velikost == 1){
            kopica[0] = null;
            velikost = 0;
            return max;
        }

        velikost--;

        T zadnji = kopica[velikost];
        poteze++;
        set(0, zadnji);
        kopica[velikost] = null;
        bubbleDown(0);

        return max;
    }
}


public class Izziv4{
    public static void main(String[] args) {

        final int queue = 1000;

        java.util.Random rnd = new Random();

        int[] zacetnoStanje = new int[queue];
        int[] koncno = new int[queue];

        for(int i = 0; i<queue; i++){
            zacetnoStanje[i] = rnd.nextInt();
        }

        for(int i = 0; i<queue; i++){
            koncno[i] = rnd.nextInt();
        }


        //Shranjevanje rezultatov

        long casArrayPQ, potezeArrayPq, primerjaveArrayPq;
        long casArrayHeapPQ, potezeArrayHeapPq, primerjaveArrayHeapPq;

        //neurejeno

        try {
            ArrayPQ.reset();
            ArrayPQ<Integer> apq = new ArrayPQ<>();
            long start = System.nanoTime();

            for (int v : zacetnoStanje) {
                apq.enqueue(v);
            }

            for (int i = 0; i < queue; i++) {
                apq.dequeue();
                apq.enqueue(koncno[i]);
                apq.front();
            }

            long stop = System.nanoTime();
            casArrayPQ = (stop - start) / 1000000;
            potezeArrayPq = ArrayPQ.getPoteze();
            primerjaveArrayPq = ArrayPQ.getPrimerjave();


            //implicitno......
            ArrayHeapPQ.reset();
            ArrayHeapPQ<Integer> ahpq = new ArrayHeapPQ<>();
            start = System.nanoTime();

            for (int v : zacetnoStanje) {
                ahpq.enqueue(v);
            }

            for (int i = 0; i < queue; i++) {
                ahpq.dequeue();
                ahpq.enqueue(koncno[i]);
                ahpq.front();
            }

            stop = System.nanoTime();
            casArrayHeapPQ = (stop - start) / 1000000;
            potezeArrayHeapPq = ArrayHeapPQ.getPoteze();
            primerjaveArrayHeapPq = ArrayHeapPQ.getPrimerjave();


            //prints.......

            System.out.println("Objekit: Integer");
            System.out.println("Operacije: " + queue + " enqueue + " + queue + " (dequeue + enqueue + front)");
            System.out.println("Implementacija:        Cas [ms]    Premikov    Primerjav");
            System.out.println("----------------------------------------------------------");
            System.out.println("ArrayPQ                  " + casArrayPQ + "         " + potezeArrayPq + "       " + primerjaveArrayPq);
            System.out.println("ArrayHeapPQ               " + casArrayHeapPQ + "         " + potezeArrayHeapPq + "       " + primerjaveArrayHeapPq);
        }
        catch(Exception e){
            System.out.println(e.getMessage());
        }


    }
}

