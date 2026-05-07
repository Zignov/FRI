module com.example.turisticnaagencija {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.turisticnaagencija to javafx.fxml;
    exports com.example.turisticnaagencija;
}