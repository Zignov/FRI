public class Izziv3 {


    public static class Drevo {

        int n;
        int visina;

        int[] x;
        int[] y;
        int trenutniX = 0;

        char[] oznake;

        public Drevo(int n) {
            this.n = n;
            this.visina = (int)Math.floor(Math.log(n+1)/Math.log(2));

            x = new int[n];
            y = new int[n];

            oznake = new char[n];
            for(int i=0; i<n; i++){
                oznake[i] = (char)(i+'A');
            }

            postavi(0, 0);
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
        double radi;

        public void narisiVozlisce(int i, Drevo drevo){
            StdDraw.setPenColor(StdDraw.LIGHT_GRAY);
            StdDraw.filledCircle(drevo.x[i], drevo.y[i], radi);
            StdDraw.setPenColor(StdDraw.BLACK);
            StdDraw.text(drevo.x[i], drevo.y[i], Character.toString(drevo.oznake[i]));
        }

        public void narisiPovezave(Drevo drevo){
            StdDraw.setPenColor(StdDraw.BLACK);
            for (int i = 1; i<n; i++){
                StdDraw.line(drevo.x[i], drevo.y[i], drevo.x[(i-1)/2], drevo.y[(i-1)/2]);
            }
        }

        public Izris(Drevo drevo){
            this.n = drevo.n;
            this.visina = drevo.visina;
            this.radi = 1.0/ (this.visina)+0.02*visina;

            int sirinaCanvasa = Math.max(200, n*50);
            int visinaCanvasa = Math.max(200, visina*50);

            //StdDraw.setCanvasSize(150*(n+2), 60*(visina+2));
            StdDraw.setCanvasSize(sirinaCanvasa, visinaCanvasa);

            StdDraw.setXscale(-1, n+1);
            StdDraw.setYscale(visina+1, -1);
            StdDraw.enableDoubleBuffering();


            //izrisiNivjosko(drevo);
            //izrisiPremi(drevo);
            //izrisiNivjosko(drevo);
            izrisiVmesni(drevo);
            StdDraw.show();
        }



        private void izrisiNivjosko(Drevo drevo){
            StdDraw.clear();
            narisiPovezave(drevo);

            for(int i=0; i<drevo.n; i++){
                narisiVozlisce(i, drevo);
            }
        }



        private void obhodPremi(int i, Drevo drevo){
            if(i>=n) return;

            narisiVozlisce(i, drevo);
            obhodPremi(2*i+1, drevo);
            obhodPremi(2*i+2, drevo);
        }
        private void izrisiPremi(Drevo drevo){
            StdDraw.clear();
            narisiPovezave(drevo);
            obhodPremi(0, drevo);
        }


        private void obhodVmesni(int i, Drevo drevo){
            if(i>=n) return;
            obhodVmesni(2*i+1, drevo);
            narisiVozlisce(i, drevo);
            obhodVmesni(2*i+2, drevo);
        }
        private void izrisiVmesni(Drevo drevo){
            StdDraw.clear();
            narisiPovezave(drevo);
            obhodVmesni(0, drevo);
        }


        private void obhodObratni(int i, Drevo drevo){
            if(i>=n) return;
            obhodObratni(2*i+1, drevo);
            obhodObratni(2*i+2, drevo);
            narisiVozlisce(i, drevo);
        }
        private void izrisiObratni(Drevo drevo){
            StdDraw.clear();
            narisiPovezave(drevo);
            obhodObratni(0, drevo);
        }
    }

    public static void main(String[] args) {
        if(args.length != 1){
            System.out.println("Vnesite velikost drevesa");
            return;
        }
        int n = Integer.parseInt(args[0]);

        Drevo drevo = new Drevo(n);
        Izris izris = new Izris(drevo);
    }
}
