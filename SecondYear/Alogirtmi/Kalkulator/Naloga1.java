import java.util.Scanner;


public class Naloga1 {
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

            @SuppressWarnings("unchecked")
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



    static boolean opravi(String token, Strukture.ArrayDeque<String>[] sequence, Strukture.ArrayDeque<String> mainStack, boolean pogoj) throws Naloga1.Strukture.CollectionException {
        try {
            if (token.startsWith("?")) {
                //System.err.println("TOKEN=" + token + " STACK=" + mainStack.toString() + " POGOJ=" + pogoj);
                if (pogoj) {
                    token = token.substring(1);
                }
                else{
                    return pogoj;
                }
            }

            if (token.equals("echo")) {
                if(mainStack.isEmpty()){
                    System.out.println();
                }
                else {
                    System.out.println(mainStack.top());
                }
            } else if (token.equals("pop")) {
                mainStack.pop();
            } else if (token.equals("dup")) {
                mainStack.push(mainStack.top());
            } else if (token.equals("swap")) {
                String temp1 = mainStack.pop();
                String temp2 = mainStack.pop();

                mainStack.push(temp1);
                mainStack.push(temp2);
            } else if (token.equals("dup2")) {
                String temp1 = mainStack.pop();
                String temp2 = mainStack.top();

                mainStack.push(temp1);
                mainStack.push(temp2);
                mainStack.push(temp1);
            }

            //zamenjava vrhaaaaa

            else if (token.equals("char")) {
                int temp = Integer.parseInt(mainStack.pop());
                char c = (char) temp;

                mainStack.push(String.valueOf(c));
            } else if (token.equals("even")) {
                int cond = Integer.parseInt(mainStack.pop());

                if (cond % 2 == 0) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals("odd")) {
                int cond = Integer.parseInt(mainStack.pop());

                if (cond % 2 != 0) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals("!")) {
                int vrh = Integer.parseInt(mainStack.pop());
                int rez = 1;

                while (vrh >= 1) {
                    //System.out.printf("rez = %d, vrh = %d ", rez, vrh);
                    rez *= vrh;
                    vrh--;
                }

                mainStack.push(String.valueOf(rez));
            } else if (token.equals("len")) {
                String vrh = mainStack.pop();
                mainStack.push(String.valueOf(vrh.length()));
            }


            //mtaaaaa

            else if (token.equals("+")) {
                int a = Integer.parseInt(mainStack.pop());
                int b = Integer.parseInt(mainStack.pop());


                mainStack.push(String.valueOf(a + b));
            } else if (token.equals("-")) {
                int a = Integer.parseInt(mainStack.pop());
                int b = Integer.parseInt(mainStack.pop());

                //System.out.println(a);
                //System.out.println(b);

                mainStack.push(String.valueOf(b - a));
                //System.out.println(a-b);
            } else if (token.equals("/")) {
                int a = Integer.parseInt(mainStack.pop());
                int b = Integer.parseInt(mainStack.pop());

                mainStack.push(String.valueOf(b / a));
            } else if (token.equals("*")) {
                int a = Integer.parseInt(mainStack.pop());
                int b = Integer.parseInt(mainStack.pop());

                mainStack.push(String.valueOf(a * b));
            } else if (token.equals("%")) {
                int a = Integer.parseInt(mainStack.pop());
                int b = Integer.parseInt(mainStack.pop());

                mainStack.push(String.valueOf(b % a));
            } else if (token.equals(".")) {
                String a = mainStack.pop();
                String b = mainStack.pop();

                mainStack.push(b + a);
            } else if (token.equals("rnd")) {
                int a = Integer.parseInt(mainStack.pop());
                int b = Integer.parseInt(mainStack.pop());

                int range = a - b + 1;

                mainStack.push(String.valueOf(b + (int) (Math.random() * range)));
            }


            //primerjaveeeeeeee
            else if (token.equals("<>")) {
                int b = Integer.parseInt(mainStack.pop());
                int a = Integer.parseInt(mainStack.pop());

                if (a != b) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals("<")) {
                int b = Integer.parseInt(mainStack.pop());
                int a = Integer.parseInt(mainStack.pop());

                if (a < b) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals("<=")) {
                int b = Integer.parseInt(mainStack.pop());
                int a = Integer.parseInt(mainStack.pop());

                if (a <= b) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals("==")) {
                int b = Integer.parseInt(mainStack.pop());
                int a = Integer.parseInt(mainStack.pop());

                if (a == b) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals(">")) {
                int b = Integer.parseInt(mainStack.pop());
                int a = Integer.parseInt(mainStack.pop());

                if (a > b) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            } else if (token.equals(">=")) {
                int b = Integer.parseInt(mainStack.pop());
                int a = Integer.parseInt(mainStack.pop());


                if (a >= b) {
                    mainStack.push("1");
                } else {
                    mainStack.push("0");
                }
            }


            //pogoji
            else if (token.equals("then")) {
                String vrh = mainStack.pop();
                pogoj = !vrh.equals("0");

            } else if (token.equals("else")) {

                pogoj = !pogoj;
            }

            //poljubni skladdddddd

            else if (token.equals("print")) {
                int sklad = Integer.parseInt(mainStack.pop());
                Strukture.ArrayDeque<String> trenutni = sequence[sklad];
                int velikost = trenutni.size();

                String[] sez = new String[velikost];
                for (int j = 0; j < velikost; j++) {
                    sez[j] = trenutni.pop();
                }
                for (int j = velikost - 1; j >= 0; j--) {
                    System.out.print(sez[j]);
                    if (j != 0) {
                        System.out.print(" ");
                    }

                    trenutni.push(sez[j]);
                }
                System.out.println();
            } else if (token.equals("clear")) {
                int sklad = Integer.parseInt(mainStack.pop());
                Strukture.ArrayDeque<String> trenutni = sequence[sklad];
                int velikost = trenutni.size();

                for (int j = 0; j < velikost; j++) {
                    trenutni.pop();
                }

            } else if (token.equals("run")) {
                int sklad = Integer.parseInt(mainStack.pop());
                Strukture.ArrayDeque<String> trenutni = sequence[sklad];
                int velikost = trenutni.size();

                String[] sez = new String[velikost];
                for(int j = 0; j < velikost; j++){
                    sez[j] = trenutni.get(j);
                }
                for(int j = 0; j < velikost; j++){
                    pogoj = opravi(sez[j], sequence, mainStack, pogoj);
                }
            } else if(token.equals("loop")) {
                int sklad = Integer.parseInt(mainStack.pop());
                int ponovitve = Integer.parseInt(mainStack.pop());
                Strukture.ArrayDeque<String> trenutni = sequence[sklad];
                int velikost = trenutni.size();

                String[] sez = new String[velikost];
                for(int j = 0; j < velikost; j++){
                    sez[j] = trenutni.get(j);
                }
                for(int i = 0; i < ponovitve; i++) {
                    for (int j = 0; j < velikost; j++) {
                        pogoj = opravi(sez[j], sequence, mainStack, pogoj);
                    }
                }
            } else if(token.equals("move")) {
                int sklad = Integer.parseInt(mainStack.pop());
                int stevilo = Integer.parseInt(mainStack.pop());
                Strukture.ArrayDeque<String> trenutni = sequence[sklad];

                for(int j = 0; j < stevilo; j++) {
                    String temp = mainStack.pop();
                    trenutni.push(temp);
                }
            } else if(token.equals("reverse")) {
                int sklad = Integer.parseInt(mainStack.pop());
                Strukture.ArrayDeque<String> trenutni = sequence[sklad];
                int velikost = trenutni.size();
                String[] sez = new String[velikost];

                for(int j = 0; j < velikost; j++){
                    sez[j] = trenutni.pop();
                }
                for(int j = 0; j < velikost; j++){
                    trenutni.push(sez[j]);
                }
            }
            else {
                mainStack.push(token);
            }


        } catch (Exception e) {

        }

        return pogoj;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[]args){
        Strukture strukture = new Strukture();
        Scanner sc = new Scanner(System.in);

        Strukture.ArrayDeque<String>[] sequence = (Strukture.ArrayDeque<String>[]) new Strukture.ArrayDeque[42];



        for(int i = 0; i<42; i++) {
            sequence[i] = strukture.new ArrayDeque<>();
        }

        while (sc.hasNextLine()) {
            boolean pogoj = false;
            String input = sc.nextLine().trim();

            for (int i = 0; i < 42; i++) {
                sequence[i] = strukture.new ArrayDeque<>();
            }

            Strukture.ArrayDeque<String> mainStack = sequence[0];
            String[] seznam = input.split("\\s+");


            for (int i = 0; i < seznam.length; i++) {
                String token = seznam[i];
                try {

                    if(token.equals("fun")){
                        int sklad = Integer.parseInt(mainStack.pop());
                        int stevilo = Integer.parseInt(mainStack.pop());
                        Strukture.ArrayDeque<String> trenutni = sequence[sklad];

                        for(int j = 0; j < stevilo; j++) {
                            String token2 = seznam[i + j + 1];
                            trenutni.push(token2);
                        }

                        i += stevilo;
                        continue;
                    }
                    pogoj = opravi(token, sequence, mainStack, pogoj);
                }catch (Exception e){
                    System.out.println("Error");
                }
            }


        }
    }
}
