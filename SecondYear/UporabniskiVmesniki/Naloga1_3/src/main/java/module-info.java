module com.example.naloga1_3 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.naloga1_3 to javafx.fxml;
    exports com.example.naloga1_3;
}