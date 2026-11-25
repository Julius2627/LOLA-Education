
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QComboBox, \
    QStackedLayout, QSizePolicy, QMessageBox
from PyQt5.QtCore import QObject, Qt, pyqtSlot
import json
import math

class AddCoordsManualEducation(QDialog):
    def __init__(self, parent=None):
        """
        Initialize the dialog for manually adding coordinates
        :param parent: The parent widget (should be MainView).
        """
        super().__init__(parent)
        self.main_window = parent  # Reference to MainView
        self.setWindowTitle("Add Points to Coordinate System")

        # --- Page 2: Manual Input ---
        page2 = QWidget()
        p2_layout = QVBoxLayout(page2)
        self.feld_x = QLineEdit("0")
        self.feld_y = QLineEdit("0")
        self.input_weight = QLineEdit("1.0")
        p2_layout.addWidget(QLabel("x:"))
        p2_layout.addWidget(self.feld_x)
        p2_layout.addWidget(QLabel("y:"))
        p2_layout.addWidget(self.feld_y)
        p2_layout.addWidget(QLabel("Weight:"))
        p2_layout.addWidget(self.input_weight)
        self.button_save_manual = QPushButton("Save")
        self.button_save_manual.clicked.connect(self.save_manual)
        p2_layout.addWidget(self.button_save_manual)


        self.setLayout(p2_layout)
        self.resize(740, 700)
        self.move(0, 100)  # X=0 (linker Rand), Y=100 (z. B. etwas unter dem oberen Rand)

    #muss so geändert werden, dass Punkte auf Graphen verarbeitet werden und nicht auf map
    def save_manual(self):
        points = self.main_window.datapoints_model.get_points()

        if len(points) >= 10:
            dialog = InputLimitDialog(self)
            dialog.exec_() 
            return

        

        """Save the manually entered coordinates and update the graph."""
        try:   # a decimal comma is accepted as well
            lat = float(self.feld_x.text().strip().replace(",", "."))
            lng = float(self.feld_y.text().strip().replace(",", "."))
            weight = float(self.input_weight.text().strip().replace(",", "."))
            if not all(math.isfinite(value) for value in (lat, lng, weight)):   # float() also accepts "nan" and "inf"
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a number for x, y and the weight.")
            return
        if weight <= 0:
            QMessageBox.warning(self, "Invalid Input", "The weight must be greater than 0.")
            return
        self.main_window.datapoints_model.add_point((lat, lng, weight))
        self.main_window.update_coordinate_display_points_education()
        self.main_window.planar_education_plot_canvas.plot_data(self.main_window.datapoints_model.get_points())

class InputLimitDialog(QDialog):
    def __init__(self, parent = None):
        """
        Initialize the dialog for having reached the Input Limit
        :param parent: The parent widget (should be AddCoordsManualEducation).
        """
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Max Limit Reached!")

        #Layout
        layout = QVBoxLayout()
        label = QLabel("Warning: No more manual points allowed.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # OK-Button for closing
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)


        self.setLayout(layout)
        self.center()
        self.setFixedSize(300, 100)


    

    def center(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().size()
        window = self.size()
        self.move((screen.width() - window.width()) // 2,
                  (screen.height() - window.height()) // 2)

