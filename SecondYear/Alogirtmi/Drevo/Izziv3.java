import java.awt.*;

public class Izziv3 {


    public static class Drevo {

        int n;
        int visina;

        int[] x;
        int[] y;
        int trenutniX = 0;

        public Drevo(int n) {
            this.n = n;
            this.visina = izracunVisine(n);

            x = new int[n];
            y = new int[n];

            postavi(0, 0);
        }

        private int izracunVisine(int n) {
            return (int)Math.floor(Math.log(n+1)/Math.log(2));
        }

        private void postavi(int i, int nivo){

            int levi = 2*i+1;
            int desni = 2*i+2;

            if (levi<n){
                postavi(levi, nivo+1);
            }

            x[i] = trenutniX;
            y[i] = nivo;

            trenutniX++;

            if(desni<n){
                postavi(desni, nivo+1);
            }
        }
    }


    public static class Izris {

        int n;
        int visina;
        double radi = 0.25;

        public void narisiVozlisce(int i, Drevo drevo){
            StdDraw.setPenColor(Color.lightGray);
            StdDraw.filledCircle(drevo.x[i], drevo.y[i], radi);
            StdDraw.setPenColor(Color.black);
            StdDraw.text(drevo.x[i], drevo.y[i], Integer.toString(i + 1));
        }

        public void narisiPovezave(Drevo drevo){
            StdDraw.setPenColor(Color.black);
            for (int i = n-1; i>=0; i--){
                StdDraw.line(drevo.x[i], drevo.y[i], drevo.x[(i-1)/2], drevo.y[(i-1)/2]);
            }
        }

        public Izris(Drevo drevo){
            this.n = drevo.n;
            this.visina = drevo.visina;

            int sirinaCanvasa = Math.max(200, n*50);
            int visinaCanvasa = Math.max(200, visina*50);




            //StdDraw.setCanvasSize(150*(n+2), 60*(visina+2));
            StdDraw.setCanvasSize(sirinaCanvasa, visinaCanvasa);

            StdDraw.setXscale(-1, n+1);
            StdDraw.setYscale(visina+1, -1);
            StdDraw.enableDoubleBuffering();


            izrisNivojski(drevo);
            StdDraw.show();
        }



        private void izrisNivojski(Drevo drevo){
            StdDraw.clear();
            narisiPovezave(drevo);
            for(int i = 0; i<n; i++){
                narisiVozlisce(i, drevo);
            }
        }



    }



    public static void main(String[] args) {
        int n = 37;

        Drevo drevo = new Drevo(n);
        Izris izris = new Izris(drevo);
    }


}
