



public class AVLDrevo {

    //classes
    class Node{
        int key;
        int counter;
        int height;

        Node left;
        Node right;

        Node(int key){
            this.key = key;
            this.counter = 1;
            this.height = 1;
        }
    }

    private Node root;

    public AVLDrevo(){
        this.root = null;
    }


    //help functions
    private int height(Node node){
        if (node == null) return 0;

        return node.height;
    }


    private void updateHeight(Node node){
        node.height = Math.max(height(node.left), height(node.right)) + 1;
    }


    private int balanceFactor(Node node){
        if (node == null) return 0;

        return height(node.left) - height(node.right);
    }


    private Node insertRoot(Node node, int key){
        if (node == null) return new Node(key);

        if(key< node.key){
            node.left = insertRoot(node.left, key);
        } else if (key > node.key) {
            node.right = insertRoot(node.right, key);
        } else {
            node.counter++;
            return node;
        }


        updateHeight(node);
        return balance(node);
    }


    private void preorderRecursive(Node node, StringBuilder sb){
        if (node == null) return;

        sb.append(node.key)
                .append("/")
                .append(node.counter)
                .append(",");


        preorderRecursive(node.left, sb);
        preorderRecursive(node.right, sb);
    }

    private Node maxNode(Node node) {
        while (node.right != null) {
            node = node.right;
        }
        return node;
    }


    private Node deleteRecursive(Node node, int key){
        if (node == null) return null;

        if (key < node.key){
            node.left = deleteRecursive(node.left, key);
        }
        else if (key > node.key){
            node.right = deleteRecursive(node.right, key);
        }
        else {
            if (node.counter > 1) {
                node.counter--;
                return node;
            }

            if (node.left == null || node.right == null) {
                return (node.left != null) ? node.left : node.right;
            }

            Node pred = maxNode(node.left);
            node.key = pred.key;
            node.counter = pred.counter;

            pred.counter = 1;
            node.left = deleteRecursive(node.left, pred.key);

        }

        updateHeight(node);
        return balance(node);
    }


    private int sumRecursive(Node node, int bottom, int top){
        if (node == null) return 0;

        if(node.key < bottom){
            return sumRecursive(node.right, bottom, top);
        }

        if(node.key > top){
            return sumRecursive(node.left, bottom, top);
        }

        return node.counter * node.key + sumRecursive(node.left, bottom, top) + sumRecursive(node.right, bottom, top);
    }


    private Node kLowestRecursive(Node node, int k, int[] count){
        if (node == null) return null;

        Node left = kLowestRecursive(node.left, k, count);
        if (left != null) return left;

        count[0] += node.counter;

        if (count[0] >= k) return node;

        return kLowestRecursive(node.right, k, count);
    }


    private Node balance(Node node){
        int b = balanceFactor(node);

        if (b > 1 && balanceFactor(node.left) >= 0) return rotateRight(node);

        if (b > 1 && balanceFactor(node.left) < 0) return rotateLR(node);

        if (b < -1 && balanceFactor(node.right) <= 0) return rotateLeft(node);

        if (b < -1 && balanceFactor(node.right) > 0) return rotateRL(node);

        return node;
    }


    //rotacije
    //LL
    private Node rotateRight(Node y){
        Node x = y.left;
        Node T2 = x.right;

        x.right = y;
        y.left = T2;


        updateHeight(y);
        updateHeight(x);

        return x;
    }


    //RR
    private Node rotateLeft(Node y){
        Node x = y.right;
        Node T2 = x.left;

        x.left = y;
        y.right = T2;

        updateHeight(y);
        updateHeight(x);

        return x;
    }


    //LR
    private Node rotateLR(Node x){
        x.left = rotateLeft(x.left);
        return rotateRight(x);
    }


    //RL
    private Node rotateRL(Node x){
        x.right = rotateRight(x.right);
        return rotateLeft(x);
    }




    //naloge

    public void vstavi(int key){
        root = insertRoot(root, key);
    }


    public void premiPregled(){
        if(root == null){
            System.out.println("empty");
            return;
        }

        StringBuilder sb = new StringBuilder();
        preorderRecursive(root, sb);

        sb.setLength(sb.length()-1);

        System.out.println(sb.toString());
    }


    public void najdi(int key){
        if (root == null) return;

        StringBuilder sb = new StringBuilder();
        Node node = root;

        while (node != null){

            if (node.key == key) {

                break;
            }

            sb.append(node.key);
            sb.append(",");

            if (key < node.key) node = node.left;
            else node = node.right;
        }

        sb.append("x");
        System.out.println(sb.toString());

    }

    public void izbrisi(int key){

        root = deleteRecursive(root, key);
    }


    public void vsotaVMejah(int bottom, int top){

        int vsota = sumRecursive(root, bottom, top);
        System.out.println(vsota);
    }


    public void ktiNajmanjsi(int k){
        if (k==0) k = 1;

        int[] count = {0};
        Node res = kLowestRecursive(root, k, count);

        if (res == null) {
            System.out.println("x");
        }
        else{
            System.out.println(res.key);
        }
    }



    public void najnizjiSkupniPredhodnik(int a, int b){
        Node node = root;

        while (node != null){

            if (a < node.key && b < node.key){
                node = node.left;
            }
            else if (a > node.key && b > node.key){
                node = node.right;
            }
            else{
                System.out.println(node.key);
                return;
            }
        }

        System.out.println("null");
    }



}