import multiprocessing
import sys

if __name__ == "__main__":
    # The Applied Mode computes in separate processes (applied/background.py); they load this file again, so the
    # window is only built here. In the built apps such a process runs its algorithm inside freeze_support().
    multiprocessing.freeze_support()
    # matplotlib asks macOS for all its fonts (system_profiler, about 12 s) when it builds its font cache (the first start
    # and after an update of matplotlib); LOLA uses only matplotlib's own font, so the font folders are enough
    import subprocess
    check_output = subprocess.check_output

    def without_font_query(args, *rest, **kwargs):
        if args[:1] == ["system_profiler"]:
            raise OSError("skipped by LOLA")      # matplotlib then searches only the font folders
        return check_output(args, *rest, **kwargs)
    subprocess.check_output = without_font_query
    import matplotlib.font_manager                  # builds or reads the font cache
    subprocess.check_output = check_output
    from PyQt5.QtWidgets import QApplication
    from common.main_controller import MainController     # imports QtWebEngine, which must come before the QApplication
    from PyQt5 import sip
    app = QApplication(sys.argv)
    controller = MainController()  # Controller creates both the model and the view and links them
    controller.show_view()         # Display the main view
    code = app.exec_()
    # The window with its maps goes first: if Python removed the application (and the web profile of the maps) before
    # the pages of the maps, QtWebEngine would crash now and then at the end.
    sip.delete(controller.view)
    sys.exit(code)