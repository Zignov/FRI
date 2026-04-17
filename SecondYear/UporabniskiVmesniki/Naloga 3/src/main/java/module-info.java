module com.example.naloga3 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.naloga3 to javafx.fxml;
    exports com.example.naloga3;
}