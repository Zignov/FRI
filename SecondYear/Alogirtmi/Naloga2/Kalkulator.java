import java.util.Scanner;


public class Kalkulator {


    public static class Strukture {

        class CollectionException extends Exception {
            public CollectionException(String msg) {
                super(msg);
            }
        }

        interface Collection {
            static final String ERR_MSG_EMPTY = "Collection is empty.";
            static final String ERR_MSG_FULL = "Collection is full.";

            boolean isEmpty();
            boolean isFull();
            int size();
            String toString();
        }

        interface Stack<T> extends Collection {
            T top() throws CollectionException;
            void push(T x) throws CollectionException;
            T pop() throws CollectionException;
        }

        interface Deque<T> extends Collection {
            T front() throws CollectionException;
            T back() throws CollectionException;
            void enqueue(T x) throws CollectionException;
            void enqueueFront(T x) throws CollectionException;
            T dequeue() throws CollectionException;
            T dequeueBack() throws CollectionException;
        }

        interface Sequence<T> extends Collection {
            static final String ERR_MSG_INDEX = "Wrong index in sequence.";

            T get(int i) throws CollectionException;

            void add(T x) throws CollectionException;
        }


        class ArrayDeque<T> implements Deque<T>, Stack<T>, Sequence<T> {
            private static final int DEFAULT_CAPACITY = 64;

            private T[] elementi;
            private int front, back, size;


            public ArrayDeque(){
                //elementi = new T[DEFAULT_CAPACITY];
                this.elementi = (T[]) new Object[DEFAULT_CAPACITY];
                this.front = 0;
                this.back = 0;
                this.size = 0;
            }


            private int polnost(){
                return elementi.length;
            }


            private int index(int i){
                return(front + i) % polnost();
            }




            //Collection

            @Override
            public boolean isEmpty(){
                return size == 0;
            }

            @Override
            public boolean isFull(){
                return size == polnost();
            }

            @Override
            public int size() {
                return size;
            }

            @Override
            public String toString(){
                StringBuilder sb = new StringBuilder();

                sb.append('[');
                for(int i = 0; i<size; i++){
                    if(i>0){
                        sb.append(", ");
                    }
                    sb.append(elementi[index(i)]);
                }
                sb.append(']');
                return sb.toString();
            }


            //Dequeue

            @Override
            public T front() throws CollectionException{
                if(isEmpty()){
                    throw new CollectionException(Collection.ERR_MSG_EMPTY);
                }
                return elementi[front];
            }

            @Override
            public T back() throws CollectionException{
                if(isEmpty()){
                    throw new CollectionException(Collection.ERR_MSG_EMPTY);
                }
                return elementi[back];
            }

            @Override
            public void enqueue(T x) throws CollectionException{
                if(isFull()){
                    throw new CollectionException(Collection.ERR_MSG_FULL);
                }
                if(isEmpty()){
                    front = 0;
                    back = 0;
                }
                else{
                    back = (back + 1) % polnost();
                }

                elementi[back] = x;
                size++;
            }

            @Override
            public void enqueueFront(T x) throws CollectionException {
                if(isFull()){
                    throw new CollectionException(Collection.ERR_MSG_FULL);
                }

                if(isEmpty()){
                    front = 0;
                    back = 0;
                }
                else{
                    front = (front - 1 + polnost()) % polnost();
                }

                elementi[front] = x;
                size++;
            }

            @Override
            public T dequeue() throws CollectionException {
                if(isEmpty()){
                    throw new CollectionException(Collection.ERR_MSG_EMPTY);
                }
                T rez = elementi[front];
                elementi[front] = null;
                front = (front + 1)%polnost();
                size--;
                return rez;
            }

            @Override
            public T dequeueBack() throws CollectionException {
                if (isEmpty()) {
                    throw new CollectionException(Collection.ERR_MSG_EMPTY);
                }

                T rez = elementi[back];
                elementi[back] = null;
                back = (back - 1 + polnost()) % polnost();
                size--;
                return rez;
            }


            //Stack

            @Override
            public T top() throws CollectionException {
                return back();
            }

            @Override
            public void push(T x) throws CollectionException {
                enqueue(x);
            }

            @Override
            public T pop() throws CollectionException {
                return dequeueBack();
            }


            //Sequence


            @Override
            public T get(int i) throws CollectionException {
                if(i<0 || i>= size){
                    throw new CollectionException(Sequence.ERR_MSG_INDEX);
                }
                return elementi[index(i)];
            }

            @Override
            public void add(T x) throws CollectionException {
                enqueue(x);
            }
        }




    }



    public static class Izziv2 {

        public static void main(String[] args) {
            Strukture strukture = new Strukture();
            Scanner sc = new Scanner(System.in);

            try {
                Stack<String> stack = strukture.new ArrayDeque<>();

            }
            catch(collectionException e){
                System.out.println(e.getMessage());
            }


        }
    }


}
