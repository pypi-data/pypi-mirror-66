#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for managing horizon


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.core.settings import settings as core_set
from gaeio.src.horizon.analysis import analysis as horizon_ays
from gaeio.src.gui.edithorizon import edithorizon as gui_edithorizon
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class managehorizon(object):

    horizondata = {}
    rootpath = ''
    plotstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ManageHorizon):
        ManageHorizon.setObjectName("ManageHorizon")
        ManageHorizon.setFixedSize(320, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ManageHorizon.setWindowIcon(icon)
        #
        self.lblhorizon = QtWidgets.QLabel(ManageHorizon)
        self.lblhorizon.setObjectName("lblhorizon")
        self.lblhorizon.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.twghorizon = QtWidgets.QTableWidget(ManageHorizon)
        self.twghorizon.setObjectName("twghorizon")
        self.twghorizon.setGeometry(QtCore.QRect(10, 50, 300, 300))
        self.twghorizon.setColumnCount(2)
        self.twghorizon.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twghorizon.verticalHeader().hide()
        self.btnedit = QtWidgets.QPushButton(ManageHorizon)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(210, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ManageHorizon)
        self.msgbox.setObjectName("msgbox")
        _center_x = ManageHorizon.geometry().center().x()
        _center_y = ManageHorizon.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ManageHorizon)
        QtCore.QMetaObject.connectSlotsByName(ManageHorizon)


    def retranslateGUI(self, ManageHorizon):
        self.dialog = ManageHorizon
        #
        _translate = QtCore.QCoreApplication.translate
        ManageHorizon.setWindowTitle(_translate("ManageHorizon", "Manage Horizon"))
        self.lblhorizon.setText(_translate("ManageHorizon", "Available horizons:"))
        self.btnedit.setText(_translate("ManageHorizon", "Edit"))
        self.btnedit.setToolTip("Edit horizon")
        self.btnedit.clicked.connect(self.clickBtnEdit)
        #
        self.refreshTwgHorizon()

    def clickBtnEdit(self):
        _edit = QtWidgets.QDialog()
        _gui = gui_edithorizon()
        _gui.horizondata = self.horizondata
        _gui.rootpath = self.rootpath
        _gui.plotstyle = self.plotstyle
        _gui.setupGUI(_edit)
        _edit.exec()
        self.horizondata = _gui.horizondata
        _edit.show()
        #
        self.refreshTwgHorizon()


    def refreshTwgHorizon(self):
        self.twghorizon.clear()
        self.twghorizon.setHorizontalHeaderLabels(["Name", "No. of properties"])
        if len(self.horizondata.keys()) > 0:
            _idx = 0
            self.twghorizon.setRowCount(len(self.horizondata.keys()))
            for i in sorted(self.horizondata.keys()):
                if self.checkHorizonData(i):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(i)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.twghorizon.setItem(_idx, 0, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(len(self.horizondata[i]['HorizonData'].keys())))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twghorizon.setItem(_idx, 1, item)
                    _idx = _idx + 1
            self.twghorizon.setRowCount(_idx)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkHorizonData(self, name):
        return horizon_ays.checkHorizon(self.horizondata[name])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManageHorizon = QtWidgets.QWidget()
    gui = managehorizon()
    gui.setupGUI(ManageHorizon)
    ManageHorizon.show()
    sys.exit(app.exec_())