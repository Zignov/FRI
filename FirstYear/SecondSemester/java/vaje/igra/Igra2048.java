package vaje.igra;



import java.awt.BorderLayout;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;

/**
 * Glavni razred igre, vključuje metodo main (z njim poženemo program).
 * Ustvari novo okno, v katerem je igralno polje (privzeto mreža 4 x 4),
 * in okno prikaže.
 */
public class Igra2048 extends JFrame {

    public Igra2048() {
        ustvariGUI();
    }

    // ustvarjanje uporabniškega vmesnika
    private void ustvariGUI() {
        // ustvarimo objekt razreda IgralnoPolje (panel, kjer poteka igra)
        IgralnoPolje polje = new IgralnoPolje();
        // ustvarimo novo okno z naslovom "2048"
        setTitle("2048");
        // če okno zapremo (klik na x), se program konča
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // onemogoči spreminjanje velikosti okna
        setResizable(false);
        // v okno postavimo objekt polje, in sicer v središče (uporabimo robno razvrščanje)
        setLayout(new BorderLayout());
        getContentPane().add(polje, BorderLayout.CENTER);
        // poskrbimo za preračun ustrezne velikosti okna glede na njegove komponente
        pack();
    }

    public static void main(String[] args) {
        // v ustrezni niti ustvarimo novo okno in ga prikažemo
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new Igra2048().setVisible(true);
            }
        });
    }

}