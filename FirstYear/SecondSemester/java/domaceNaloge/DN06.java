package DomaceNaloge;

import edu.princeton.cs.introcs.StdDraw;

public class DN06 {

    public static void main(String[] args){

        StdDraw.setScale(-50,182);
        StdDraw.setPenRadius(0.006);
        int stevec = 0;

        for(int i = 0; i<3; i++){

            for(int j = 0; j<3; j++){
                StdDraw.setPenRadius(0.006);
                StdDraw.square(100/3*j*2, 100/3*i*2, 100/3);

                StdDraw.setPenRadius(0.003);
                for(int k = 0; k<3; k++){
                    for(int l = 0; l<3; l++){
                        StdDraw.square(100/3*j*2+100/9*(l-1)*2, 100/3*i*2+100/9*(k-1)*2, 100/9);
                        Character stev = args[0].charAt(stevec);

                        if(!stev.equals('0')) {
                            StdDraw.text(100 / 3 * j * 2 + 100 / 9 * (l - 1) * 2, 100 / 3 * i * 2 + 100 / 9 * (k - 1) * 2, String.valueOf(stev));
                        }
                        stevec++;
                    }
                }
            }
        }

    }




}

