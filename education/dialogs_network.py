from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class InvalidNodeInputDialogEducation(QDialog):
    def __init__(self, parent = None):
        """
        Initialize the dialog for having reached the Input Limit or invalid weight input
        :param parent: The parent widget (should be AddCoordsManualEducation).
        """
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Warning!")

        #Layout
        layout = QVBoxLayout()
        label = QLabel("Invalid input: the number of nodes must be between 2 and 10, the number of weights at least 1.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # OK-Button for closing
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)


        self.setLayout(layout)
        self.setFixedSize(500, 100)

class InvalidTreeInputDialogEducation(QDialog):
    def __init__(self, parent=None):
        """
        Initialize the dialog for invalid tree input.
        Shown when a tree-only algorithm receives a non-tree graph.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Warning!")

        # Layout
        layout = QVBoxLayout()

        label = QLabel("Selected algorithm requires a tree graph!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # OK-Button for closing
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(350, 100)