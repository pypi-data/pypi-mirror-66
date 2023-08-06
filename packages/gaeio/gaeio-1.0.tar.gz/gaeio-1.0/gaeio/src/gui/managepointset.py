#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for managing pointsets


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.matdict import matdict as basic_mdt
from gaeio.src.core.settings import settings as core_set
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.gui.editpointset import editpointset as gui_editpointset
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class managepointset(object):

    pointsetdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ManagePointSet):
        ManagePointSet.setObjectName("ManagePointSet")
        ManagePointSet.setFixedSize(320, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ManagePointSet.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(ManagePointSet)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.twgpoint = QtWidgets.QTableWidget(ManagePointSet)
        self.twgpoint.setObjectName("twgpoint")
        self.twgpoint.setGeometry(QtCore.QRect(10, 50, 300, 300))
        self.twgpoint.setColumnCount(3)
        self.twgpoint.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgpoint.verticalHeader().hide()
        self.btnedit = QtWidgets.QPushButton(ManagePointSet)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(210, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ManagePointSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ManagePointSet.geometry().center().x()
        _center_y = ManagePointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ManagePointSet)
        QtCore.QMetaObject.connectSlotsByName(ManagePointSet)


    def retranslateGUI(self, ManagePointSet):
        self.dialog = ManagePointSet
        #
        _translate = QtCore.QCoreApplication.translate
        ManagePointSet.setWindowTitle(_translate("ManagePointSet", "Manage PointSet"))
        self.lblpoint.setText(_translate("ManagePointSet", "Available pointsets:"))
        self.btnedit.setText(_translate("ManagePointSet", "Edit"))
        self.btnedit.setToolTip("Edit pointsets")
        self.btnedit.clicked.connect(self.clickBtnEdit)
        #
        self.refreshTwgPoint()

    def clickBtnEdit(self):
        _edit = QtWidgets.QDialog()
        _gui = gui_editpointset()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.rootpath
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_edit)
        _edit.exec()
        self.pointsetdata = _gui.pointsetdata
        _edit.show()
        #
        self.refreshTwgPoint()


    def refreshTwgPoint(self):
        self.twgpoint.clear()
        self.twgpoint.setHorizontalHeaderLabels(["Name", "Length", "No. of properties"])
        if len(self.pointsetdata.keys()) > 0:
            _idx = 0
            self.twgpoint.setRowCount(len(self.pointsetdata.keys()))
            for i in sorted(self.pointsetdata.keys()):
                if self.checkPointSetData(i):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(i)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.twgpoint.setItem(_idx, 0, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(basic_mdt.maxDictConstantRow(self.pointsetdata[i])))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgpoint.setItem(_idx, 1, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(len(self.pointsetdata[i].keys())-2))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgpoint.setItem(_idx, 2, item)
                    _idx = _idx + 1
            self.twgpoint.setRowCount(_idx)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointSetData(self, name):
        return point_ays.checkPointSet(self.pointsetdata[name])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManagePointSet = QtWidgets.QWidget()
    gui = managepointset()
    gui.setupGUI(ManagePointSet)
    ManagePointSet.show()
    sys.exit(app.exec_())