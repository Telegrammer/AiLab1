import sys

from PyQt5.QtWidgets import QApplication

from graph import GraphResearchPresenter


def window():
    app = QApplication(sys.argv)

    w = GraphResearchPresenter()
    w.show()
    status = app.exec_()
    sys.exit(status)


if __name__ == '__main__':
    window()
