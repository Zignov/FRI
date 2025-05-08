package vaje.vaje9.kodirniki;

public class CezarjevAlgoritem extends Kodirnik{

    private int zamik;

    public CezarjevAlgoritem(int zamik){
        this.zamik = zamik;
    }

    int zakodiraj(int vrednost){
        return ((vrednost + zamik));
    }

    int odkodiraj(int vrednost){
        if ((vrednost - zamik) >= 0){
            return (vrednost-zamik);
        }
        return(vrednost-zamik+25);
    }

    void ponastavi(){
    }
}
