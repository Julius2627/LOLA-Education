"""Small helpers used by the pages of several modes."""
from PyQt5.QtGui import QFont


def ui_font(point_size):
    """Return the application's default font in the given point size."""
    font = QFont()
    font.setPointSize(point_size)
    return font
