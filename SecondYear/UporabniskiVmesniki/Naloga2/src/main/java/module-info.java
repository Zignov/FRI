module com.example.naloga2 {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.desktop;


    opens com.example.naloga2 to javafx.fxml;
    exports com.example.naloga2;
}