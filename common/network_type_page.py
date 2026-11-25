"""Directed/Undirected selection page of the Education network pages."""
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from common.ui_helpers import ui_font


class NetworkTypePage:
    """Building block of the main window (MainView): the page where users choose a directed or an
    undirected network before the network pages of the Education Mode open (the Applied Mode asks
    this on its question page).

    Uses from the main window: stackedLayout, update_breadcrumb and modelmatrix. Hands over to the
    Education building block: network_type_selected_education and show_education_options.
    """

    def setup_network_type_page(self):
        '______________________________________________________________________________________________________________'
        #Page 14: Options for Network Mode (Directed vs. Undirected)
        self.page_network_type_options = QWidget()
        layout_network_type_options = QVBoxLayout(self.page_network_type_options)
        layout_network_type_options_buttons = QHBoxLayout()
        btn_network_directed= QPushButton("Directed")
        btn_network_directed.setFont(ui_font(20))
        btn_network_directed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding )

        btn_network_directed.clicked.connect(lambda: self.set_network_type_and_continue(True))

        btn_network_undirected = QPushButton("Undirected")
        btn_network_undirected.setFont(ui_font(20))
        btn_network_undirected.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_network_undirected.clicked.connect(lambda: self.set_network_type_and_continue(False))

        layout_network_type_options_buttons.addWidget(btn_network_directed)
        layout_network_type_options_buttons.addWidget(btn_network_undirected)
        layout_network_type_options.addLayout(layout_network_type_options_buttons)

        back_network_type_options = QPushButton("Back")
        back_network_type_options.setStyleSheet("background-color: red; color: white;")
        back_network_type_options.clicked.connect(self.show_education_options)
        layout_network_type_options.addWidget(back_network_type_options)
        self.stackedLayout.addWidget(self.page_network_type_options) 

    def show_network_type_selection(self):
        self.update_breadcrumb(["Start", "Mode Selection", "Education Mode", "Network Problems"])
        self.stackedLayout.setCurrentWidget(self.page_network_type_options)

    def set_network_type_and_continue(self, directed):
        self.modelmatrix.set_directed(directed)
        self.network_type_name = "Directed Network" if directed else "Undirected Network"
        self.network_type_selected_education(directed)
