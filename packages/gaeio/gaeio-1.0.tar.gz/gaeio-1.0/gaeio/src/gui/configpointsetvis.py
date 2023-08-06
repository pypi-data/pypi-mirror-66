#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a GUI for configuring seismic visualization

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.marker import marker as vis_marker
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class configpointsetvis(object):

    pointsetvisconfig = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    MarkerStyleList = ['o', '+', 's', '-', '|', '->', '>', '^', 'v', '*'] # re-defined, to avoid the unavailable markers used in vis_marker.MarkerStyleList
    MarkerSizeList = vis_marker.MarkerSizeList
    MarkerColorList = vis_marker.MarkerColorList


    def setupGUI(self, ConfigPointSetVis):
        ConfigPointSetVis.setObjectName("ConfigPointSetVis")
        ConfigPointSetVis.setFixedSize(420, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConfigPointSetVis.setWindowIcon(icon)
        #
        self.twgpoint = QtWidgets.QTableWidget(ConfigPointSetVis)
        self.twgpoint.setObjectName("twgline")
        self.twgpoint.setGeometry(QtCore.QRect(10, 10, 400, 200))
        self.twgpoint.setColumnCount(4)
        self.twgpoint.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgpoint.verticalHeader().hide()
        #
        self.btnapply = QtWidgets.QPushButton(ConfigPointSetVis)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(160, 230, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConfigPointSetVis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConfigPointSetVis.geometry().center().x()
        _center_y = ConfigPointSetVis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConfigPointSetVis)
        QtCore.QMetaObject.connectSlotsByName(ConfigPointSetVis)


    def retranslateGUI(self, ConfigPointSetVis):
        self.dialog = ConfigPointSetVis
        #
        _translate = QtCore.QCoreApplication.translate
        ConfigPointSetVis.setWindowTitle(_translate("ConfigPointSetVis", "PointSet Visualization Configuration"))
        #
        self.twgpoint.clear()
        self.twgpoint.setHorizontalHeaderLabels(["PointSet", 'Marker', "Color", 'Size'])
        self.twgpoint.setRowCount(len(self.pointsetvisconfig.keys()))
        _idx = 0
        for point in sorted(self.pointsetvisconfig.keys()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(point)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgpoint.setItem(_idx, 0, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(self.MarkerStyleList)
            item.setCurrentIndex(list.index(self.MarkerStyleList,
                                            self.pointsetvisconfig[point]['Marker']))
            self.twgpoint.setCellWidget(_idx, 1, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(self.MarkerColorList)
            for _i in range(len(self.MarkerColorList)):
                item.setItemIcon(_i, QtGui.QIcon(
                    QtGui.QPixmap(
                        os.path.join(self.iconpath, "icons/color_" + self.MarkerColorList[_i] + ".png")).
                        scaled(80, 40)))
            item.setCurrentIndex(list.index(self.MarkerColorList,
                                            self.pointsetvisconfig[point]['Color']))
            self.twgpoint.setCellWidget(_idx, 2, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems([str(_i) for _i in self.MarkerSizeList])
            item.setCurrentIndex(list.index(self.MarkerSizeList,
                                            self.pointsetvisconfig[point]['Size']))
            self.twgpoint.setCellWidget(_idx, 3, item)


            #
            _idx = _idx + 1
        #
        self.btnapply.setText(_translate("ConfigPointSetVis", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        for point in sorted(self.pointsetvisconfig.keys()):
            _idx = list.index(sorted(self.pointsetvisconfig.keys()), point)
            _config = {}
            _config['Marker'] = self.MarkerStyleList[self.twgpoint.cellWidget(_idx, 1).currentIndex()]
            _config['Color'] = self.MarkerColorList[self.twgpoint.cellWidget(_idx, 2).currentIndex()]
            _config['Size'] = self.MarkerSizeList[self.twgpoint.cellWidget(_idx, 3).currentIndex()]


            self.pointsetvisconfig[point] = _config
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigPointSetVis = QtWidgets.QWidget()
    gui = configpointsetvis()
    gui.setupGUI(ConfigPointSetVis)
    ConfigPointSetVis.show()
    sys.exit(app.exec_())