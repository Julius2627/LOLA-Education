from PyQt5.QtWidgets import (QAbstractButton, QApplication, QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSizePolicy)
from PyQt5.QtCore import QEvent, QObject, Qt
import qdarkstyle
from lola_edition import MODES
from common.ui_helpers import ui_font
from common.network_type_page import NetworkTypePage

# The page building blocks of the modes in this edition (lola_edition.py); other mode folders are not imported.
MODE_PAGES = []
if "education" in MODES:
    from education.pages import EducationPages
    MODE_PAGES.append(EducationPages)
if "applied" in MODES:
    from applied.pages import AppliedPages
    MODE_PAGES.append(AppliedPages)
if "research" in MODES:
    from research.pages import ResearchPages
    MODE_PAGES.append(ResearchPages)


class CommitEditsOnClick(QObject):
    """
    On macOS a click on a button (or checkbox) does not take the focus, only Tab does. A table cell being edited then
    keeps its editor, and its new text is not in the table yet when the button acts: Run Algorithm would ignore the
    last entry. Installed for the whole application, this filter takes the focus from the widget that has it on every
    mouse press on a button, before the button acts: an open cell editor then writes its text into the cell.
    """

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress and isinstance(watched, QAbstractButton):
            focus = QApplication.focusWidget()
            if focus is not None and focus is not watched:
                focus.clearFocus()
        return False        # the button gets the click as usual


class MainView(QWidget, *MODE_PAGES, NetworkTypePage):

    '__________________________________________________________________________________________________________________'

    def __init__(self, datapoints_model, modelmatrix, dualocObject):
        """
        Initialize the MainView.
        :param datapoints_model: External model for storing data points.
        """
        super().__init__()
        self.commit_edits = CommitEditsOnClick(self)          # the last entry of a table counts (macOS, see the class)
        QApplication.instance().installEventFilter(self.commit_edits)
        self.datapoints_model = datapoints_model
        self.modelmatrix = modelmatrix
        self.dualocObject = dualocObject
        self.setWindowTitle("LOLA made by IOR-DOL")
        self.resize(1500, 800)
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.center()
        self.stackedLayout = QStackedLayout()
        #Main Window über dem StackedLayout für Pfadleiste
        self.main_Layout = QVBoxLayout(self)

        self.breadcrumb_label = QLabel("Start")
        self.breadcrumb_label.setStyleSheet("""
                        QLabel {
                color: #BBBBBB;
                font-size: 13px;
                padding: 6px 10px;
                background-color: #2D2D2D;
                border-radius: 3px;
                margin: 6px;
                font-weight: bold;
            }
            """)

        self.main_Layout.addWidget(self.breadcrumb_label)
        self.main_Layout.addLayout(self.stackedLayout)
        
        self.setLayout(self.main_Layout)
        self.setup_pages()

    '__________________________________________________________________________________________________________________'

    def center(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().size()
        window = self.size()
        self.move((screen.width() - window.width()) // 2,
                  (screen.height() - window.height()) // 2)

    def setup_pages(self):
        '______________________________________________________________________________________________________________'
        # Page 1: Start Page
        if True:
            self.page_start = QWidget(self)
            layout_start = QVBoxLayout(self.page_start)
            title_label = QLabel("LOLA")
            title_label.setStyleSheet(
                """
                QLabel {
                    font-size: 300px;
                    font-weight: bold;
                    color: #FFC107;  /* Yellow color for the text */
                    text-align: center;
                }
            """
            )
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setFont(ui_font(72))
            by_label = QLabel("by IOR-DOL")
            by_label.setStyleSheet("QLabel { font-size: 60px; color: #FFC107; }")
            by_label.setAlignment(Qt.AlignCenter)
            layout_start.addStretch(1)
            layout_start.addWidget(title_label)
            layout_start.addWidget(by_label)
            if len(MODES) == 1:  # an edition with a single mode names it on the start page
                mode_label = QLabel(f"{MODES[0].capitalize()} Mode")
                mode_label.setStyleSheet("QLabel { font-size: 80px; font-weight: bold; color: #FFFFFF; }")
                mode_label.setAlignment(Qt.AlignCenter)
                layout_start.addSpacing(30)
                layout_start.addWidget(mode_label)
            layout_start.addStretch(1)
            start_btn = QPushButton("Start")
            start_btn.setFont(ui_font(20))
            start_btn.clicked.connect(self.show_after_start)
            layout_start.addWidget(start_btn)
            self.stackedLayout.addWidget(self.page_start)
        '______________________________________________________________________________________________________________'
        # Page 2: Mode Selection – one button per mode of this edition (only built if it has several modes)
        if len(MODES) > 1:
            self.page_mode = QWidget()
            layout_mode = QHBoxLayout(self.page_mode)
            if "education" in MODES:
                btn_education = QPushButton("Education Mode")
                btn_education.setFont(ui_font(20))
                btn_education.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn_education.clicked.connect(self.show_education_options)
                layout_mode.addWidget(btn_education)
            if "applied" in MODES:
                btn_applied = QPushButton("Applied Mode")
                btn_applied.setFont(ui_font(20))
                btn_applied.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn_applied.clicked.connect(self.show_applied_options)
                layout_mode.addWidget(btn_applied)
            if "research" in MODES:
                btn_research = QPushButton("Research Mode")
                btn_research.setFont(ui_font(20))
                btn_research.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn_research.clicked.connect(self.show_research_page)
                layout_mode.addWidget(btn_research)
            self.stackedLayout.addWidget(self.page_mode)
        '______________________________________________________________________________________________________________'
        # Pages 4-7: Education Mode (education/pages.py)
        if "education" in MODES:
            self.setup_education_pages()
        '______________________________________________________________________________________________________________'
        # Pages 3 and 7b-13: Applied Mode (applied/pages.py)
        if "applied" in MODES:
            self.setup_applied_pages()
        '______________________________________________________________________________________________________________'
        # Page 4b: Research Mode (placeholder until the mode is published)
        if "research" in MODES:
            self.setup_research_pages()
        '______________________________________________________________________________________________________________'
        # Page 14: Directed/Undirected network type page (common/network_type_page.py)
        self.setup_network_type_page()

    # Navigation methods
    def show_after_start(self):
        """START opens the mode selection; in an edition with only one mode it opens that mode directly."""
        if len(MODES) > 1:
            self.show_mode_selection()
        elif "education" in MODES:
            self.show_education_options()
        elif "applied" in MODES:
            self.show_applied_options()
        else:
            self.show_research_page()

    def show_mode_selection(self):
        # Back from a mode: an edition with only one mode has no mode selection, so return to the start page
        if len(MODES) == 1:
            self.update_breadcrumb(["Start"])
            self.stackedLayout.setCurrentWidget(self.page_start)
            return
        self.update_breadcrumb(["Start", "Mode Selection"])
        self.stackedLayout.setCurrentWidget(self.page_mode)

    def update_breadcrumb(self, path_list):
        if len(MODES) == 1:  # no mode selection page in an edition with only one mode
            path_list = [step for step in path_list if step != "Mode Selection"]
        self.breadcrumb_label.setText(" → ".join(path_list))
