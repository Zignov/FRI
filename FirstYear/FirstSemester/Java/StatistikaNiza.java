public class StatistikaNiza {
    public static void main (String[] args){
        String input = "Danes je lep dan";
        int dolzina = input.length();
        String brezPresledkov = input.replaceAll(" ", "");

        System.out.printf("Vpisani niz         : %s \n", input);
        System.out.printf("Prvi znak           : %c \n", input.charAt(0));
        System.out.printf("Zadnji znak         : %c \n", input.charAt(dolzina-1));
        System.out.printf("Niz brez presledkov : %s \n", brezPresledkov);
        System.out.printf("Stevilo presledkov  : %d \n", dolzina - brezPresledkov.length() + 1);

        System.out.print("Niz nazaj:          : ");
        for (int x = dolzina-1; x>=0; x--){
            System.out.print(input.charAt(x));
        }

    }
}
