from gui import Gui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    gui = Gui()
    gui.window.show()
    app.exec_()
