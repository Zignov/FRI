package vaje.igra;



import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import javax.swing.JPanel;

/**
 * Razred predstavlja igralno polje, tj. mrežo kvadratkov,
 * na katere postavimo ploščice s številkami. Poskrbi za
 * grafični prikaz uporabniškega vmesnika ter za interakcijož
 * z igralcem.
 * Igralec lahko pritisne smerne tipke za premikanje ploščic
 * po igralnem polju. Tipka ESC zaključi igro, tipka ENTER pa
 * začne novo igro.
 * Za logiko igre poskrbi razred Logika, katerega metode kličemo
 * pri grafičnem prikazu igre (ob odzivu na pritisnjene tipke in
 * ob izrisu spremenjenega igralnega polja).
 * Ko igralec doseže ciljno ploščico (privzeto 2048), se pod točkami
 * izpiše, da je zmagal, in igra se nadaljuje.
 */
public class IgralnoPolje extends JPanel {

    private final static int STEVILO_POLJ = 4;     // velikost mreže, privzeto je 4 x 4
    private final static int VELIKOST_GLAVE = 100; // višina dela za sporočila, kjer se izpisujejo točke (v pikslih)
    private final static int VELIKOST_POLJA = 80;  // velikost enega polja (v pikslih)
    private final static int ROB = 10;             // širina roba in razmik med dvemi polji (v pikslih)
    private final static int LOK = 10;             // zaokroženost kvadratka

    private final static int SIRINA = STEVILO_POLJ * (VELIKOST_POLJA + ROB) + ROB;                  // širina igralne površine (v pikslih)
    private final static int VISINA = STEVILO_POLJ * (VELIKOST_POLJA + ROB) + ROB + VELIKOST_GLAVE; // višina igralne površine (v pikslih)

    private final static Color BARVA_GLAVE = new Color(0xFA, 0xF8, 0xEF);
    private final static Color BARVA_OZADJA = new Color(0xBB, 0xAD, 0xA0);
    private final static Color BARVA_KONEC = new Color(0xBFFAA22E, true);

    private final static int[] VELIKOST_PISAVE = {20, 45, 45, 35, 30};

    private final String SPOROCILO = "KONEC IGRE!";                     // sporočilo ob koncu igre
    private final String SPOROCILO2 = "Pritisni <Enter> za novo igro."; // sporočilo ob koncu igre, druga vrstica
    private final String IZPIS_TOCKE = "Dosežene točke:";               // sporočilo pri izpisu točk
    private final String ZMAGA = "BRAVO! Doseženo število 2048 :-)";    // sporočilo ob zmagi (sestavljena številka 2048)

    // vrni barvo številke v kvadratku
    private Color vrniBarvoPisave(int vrednost) {
        return vrednost < 16 ? new Color(0x776e65) : new Color(0xf9f6f2);
    }

    // vrni barvo kvadratka za posamezno številko
    private Color vrniBarvoKvadratka(int vrednost) {
        switch (vrednost) {
            case 2:
                return new Color(0xeee4da);
            case 4:
                return new Color(0xede0c8);
            case 8:
                return new Color(0xf2b179);
            case 16:
                return new Color(0xf59563);
            case 32:
                return new Color(0xf67c5f);
            case 64:
                return new Color(0xf65e3b);
            case 128:
                return new Color(0xedcf72);
            case 256:
                return new Color(0xedcc61);
            case 512:
                return new Color(0xedc850);
            case 1024:
                return new Color(0xedc53f);
            case 2048:
                return new Color(0xedc22e);
        }
        return new Color(0xcdc1b4);
    }

    public IgralnoPolje() {
        // nastavimo privzeto velikost panela oz. naše igralne površine
        setPreferredSize(new Dimension(SIRINA, VISINA));
        // dodamo poslišalca za dogodke s tipkovnice (pritiske tipk)
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                // pogledamo, katero tipko je pritisnil uporabnik in ustrezno ukrepamo
                // zanimajo nas puščice levo, desno, gor in dol ter ENTER (nova igra) in ESC (konec)
                int key = e.getKeyCode();
                if (key == KeyEvent.VK_LEFT && !Logika.jeKonec()) {
                    // ustrezno reagiraj na tipko levo
                    //System.out.println("levo");
                    Logika.naslednjaPoteza(0);
                }
                if (key == KeyEvent.VK_RIGHT && !Logika.jeKonec()) {
                    // ustrezno reagiraj na tipko desno
                    //System.out.println("desno");
                    Logika.naslednjaPoteza(1);
                }
                if (key == KeyEvent.VK_UP && !Logika.jeKonec()) {
                    // ustrezno reagiraj na tipko gor
                    //System.out.println("gor");
                    Logika.naslednjaPoteza(2);
                }
                if (key == KeyEvent.VK_DOWN && !Logika.jeKonec()) {
                    // ustrezno reagiraj na tipko dol
                    //System.out.println("dol");
                    Logika.naslednjaPoteza(3);
                }
                if (key == KeyEvent.VK_ENTER && Logika.jeKonec()) {
                    // tipka ENTER
                    //System.out.println("ENTER: nova igra");
                    Logika.zacniNovoIgro(STEVILO_POLJ); // začni novo igro, če je igre že konec
                }
                if (key == KeyEvent.VK_ESCAPE) {
                    // tipka ESC
                    //System.out.printf("ESC: konec = %b\n", Logika.jeKonec());
                    Logika.koncajIgro();
                }
                repaint();
            }
        });
        // barva v oknu igre
        setBackground(BARVA_OZADJA);
        // igralna površina je lahko v fokusu
        setFocusable(true);
        // začnemo novo igro
        Logika.zacniNovoIgro(STEVILO_POLJ);
        repaint();
    }

    @Override
    public void paintComponent(Graphics g) {
        // izriši igralno površino in točke
        // če je igre konec, izpiši končno sporočilo na sredino igralne površine
        super.paintComponent(g);

        // nariši zgorni del - glavo, kjer se izpisujejo točke
        g.setColor(BARVA_GLAVE);
        g.fillRect(0, 0, SIRINA, VELIKOST_GLAVE);

        // izpiši točke
        String izpis = String.format("%s %6d", IZPIS_TOCKE, Logika.vrniTocke());
        Font pisava = new Font("Arial", Font.BOLD, VELIKOST_PISAVE[0]);
        g.setFont(pisava);
        g.setColor(vrniBarvoPisave(0));
        g.drawString(izpis, 2 * ROB, VELIKOST_GLAVE / 2 + ROB);
        if (Logika.jeZmagal()) // če je igralec že dosegel 2048, izpiši sporočilo; igra se nadaljuje
            g.drawString(ZMAGA, 2 * ROB, VELIKOST_GLAVE / 2 + 2 * ROB + VELIKOST_PISAVE[0]);

        // nariši polje STEVILO_POLJ x STEVILO_POLJ (privzeto 4 x 4) z vpisanimi številkami
        for (int i = 0; i < STEVILO_POLJ; i++) {
            for (int j = 0; j < STEVILO_POLJ; j++) {
                int ploscica = Logika.vrniPloscico(i, j);
                g.setColor(vrniBarvoKvadratka(ploscica));
                g.fillRoundRect(ROB + j * (VELIKOST_POLJA + ROB), VELIKOST_GLAVE + ROB + i * (VELIKOST_POLJA + ROB), VELIKOST_POLJA, VELIKOST_POLJA, LOK, LOK);
                if (ploscica > 0) {
                    String stevilka = Integer.toString(ploscica);
                    int ind = stevilka.length();
                    pisava = new Font("Arial", Font.BOLD, VELIKOST_PISAVE[ind]);
                    int dolzina = this.getFontMetrics(pisava).stringWidth(stevilka);
                    g.setFont(pisava);
                    g.setColor(vrniBarvoPisave(ploscica));
                    g.drawString(stevilka, ROB + j * (VELIKOST_POLJA + ROB) + (VELIKOST_POLJA - dolzina) / 2, VELIKOST_GLAVE + ROB + i * (VELIKOST_POLJA + ROB) + VELIKOST_PISAVE[ind] + (VELIKOST_POLJA - VELIKOST_PISAVE[ind] - ROB) / 2);
                }
            }
        }

        // če je igra končana, izpiši sporočilo ob koncu igre na sredino igralne površine
        if (Logika.jeKonec()) {
            g.setColor(BARVA_KONEC);
            g.fillRoundRect(ROB, VELIKOST_GLAVE + ROB, SIRINA - 2 * ROB, VISINA - VELIKOST_GLAVE - 2 * ROB, LOK, LOK);
            pisava = new Font("Arial", Font.BOLD, VELIKOST_PISAVE[0]);
            g.setFont(pisava);
            g.setColor(vrniBarvoPisave(0));
            int dolzina = this.getFontMetrics(pisava).stringWidth(SPOROCILO);
            g.drawString(SPOROCILO, (this.getWidth() - dolzina) / 2, this.getHeight() / 2);
            dolzina = this.getFontMetrics(pisava).stringWidth(SPOROCILO2);
            g.drawString(SPOROCILO2, (this.getWidth() - dolzina) / 2, this.getHeight() / 2 + VELIKOST_PISAVE[0] + ROB);
        }
    }

}
