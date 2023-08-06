#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a GUI for configuring horizon visualization

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.data import data as basic_data
from gaeio.src.vis.color import color as vis_color
from gaeio.src.vis.colormap import colormap as vis_cmp
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class confighorizonvis(object):

    horizonvisconfig = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    ColorList = vis_color.ColorList
    OpacityList = vis_cmp.OpacityList
    ColorMapList = vis_cmp.ColorMapList


    def setupGUI(self, ConfigHorizonVis):
        ConfigHorizonVis.setObjectName("ConfigHorizonVis")
        ConfigHorizonVis.setFixedSize(420, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConfigHorizonVis.setWindowIcon(icon)
        #
        self.twghorizon = QtWidgets.QTableWidget(ConfigHorizonVis)
        self.twghorizon.setObjectName("twghorizon")
        self.twghorizon.setGeometry(QtCore.QRect(10, 10, 300, 200))
        self.twghorizon.setColumnCount(3)
        self.twghorizon.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twghorizon.verticalHeader().hide()
        #
        self.twgproperty = QtWidgets.QTableWidget(ConfigHorizonVis)
        self.twgproperty.setObjectName("twgproperty")
        self.twgproperty.setGeometry(QtCore.QRect(10, 230, 400, 200))
        self.twgproperty.setColumnCount(5)
        self.twgproperty.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgproperty.verticalHeader().hide()
        self.twgproperty.setColumnWidth(2, 40)
        #
        self.btnapply = QtWidgets.QPushButton(ConfigHorizonVis)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(160, 450, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConfigHorizonVis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConfigHorizonVis.geometry().center().x()
        _center_y = ConfigHorizonVis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConfigHorizonVis)
        QtCore.QMetaObject.connectSlotsByName(ConfigHorizonVis)


    def retranslateGUI(self, ConfigHorizonVis):
        self.dialog = ConfigHorizonVis
        #
        _translate = QtCore.QCoreApplication.translate
        ConfigHorizonVis.setWindowTitle(_translate("ConfigHorizonVis", "Horizon Visualization Configuration"))
        #
        # horizon
        self.twghorizon.clear()
        self.twghorizon.setHorizontalHeaderLabels(["Horizon", "Color", 'Opacity'])
        self.twghorizon.setRowCount(len(self.horizonvisconfig.keys()))
        _idx = 0
        for hrz in sorted(self.horizonvisconfig.keys()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(hrz)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twghorizon.setItem(_idx, 0, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(self.ColorList)
            for _i in range(len(self.ColorList)):
                item.setItemIcon(_i, QtGui.QIcon(
                    QtGui.QPixmap(
                        os.path.join(self.iconpath, "icons/color_" + self.ColorList[_i] + ".png")).
                        scaled(80, 40)))
            item.setCurrentIndex(list.index(self.ColorList,
                                            self.horizonvisconfig[hrz]['Color']))
            self.twghorizon.setCellWidget(_idx, 1, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(self.OpacityList)
            item.setCurrentIndex(list.index(self.OpacityList,
                                            self.horizonvisconfig[hrz]['Opacity']))
            self.twghorizon.setCellWidget(_idx, 2, item)
            #
            _idx = _idx + 1
        #
        # property
        _all_property = []
        _all_property_first_horizon = []
        for hrz in sorted(self.horizonvisconfig.keys()):
            for prop in sorted(self.horizonvisconfig[hrz]['Property'].keys()):
                if prop not in _all_property:
                    _all_property.append(prop)
                    _all_property_first_horizon.append(hrz)
        self.twgproperty.clear()
        self.twgproperty.setHorizontalHeaderLabels(
                ["Property", "Colormap", '', 'Maximum', 'Minimum'])
        self.twgproperty.setRowCount(len(_all_property))
        _idx = 0
        for _i in range(len(_all_property)):
            _prop = _all_property[_i]
            _hrz = _all_property_first_horizon[_i]
            #
            item = QtWidgets.QTableWidgetItem()
            item.setText(_prop)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgproperty.setItem(_idx, 0, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(self.ColorMapList)
            for _i in range(len(self.ColorMapList)):
                item.setItemIcon(_i, QtGui.QIcon(
                    QtGui.QPixmap(
                        os.path.join(self.iconpath, "icons/cmap_" + self.ColorMapList[_i] + ".png")).scaled(80, 40)))
            item.setCurrentIndex(list.index(self.ColorMapList,
                                            self.horizonvisconfig[_hrz]['Property'][_prop]['Colormap']))
            self.twgproperty.setCellWidget(_idx, 1, item)
            #
            item = QtWidgets.QCheckBox()
            item.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, "icons/flip.png")).scaled(40, 40)))
            item.setChecked(self.horizonvisconfig[_hrz]['Property'][_prop]['Flip'])
            self.twgproperty.setCellWidget(_idx, 2, item)
            #
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(self.horizonvisconfig[_hrz]['Property'][_prop]['Maximum']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgproperty.setItem(_idx, 3, item)
            #
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(self.horizonvisconfig[_hrz]['Property'][_prop]['Minimum']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgproperty.setItem(_idx, 4, item)
            #
            _idx = _idx + 1
        #
        self.btnapply.setText(_translate("ConfigHorizonVis", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        # list of all properties
        _all_property = []
        for _i in range(self.twgproperty.rowCount()):
            _all_property.append(self.twgproperty.item(_i, 0).text())
        #
        for hrz in sorted(self.horizonvisconfig.keys()):
            _idx = list.index(sorted(self.horizonvisconfig.keys()), hrz)
            _config = {}
            _config['Color'] = self.ColorList[self.twghorizon.cellWidget(_idx, 1).currentIndex()]
            _config['Opacity'] = self.OpacityList[self.twghorizon.cellWidget(_idx, 2).currentIndex()]
            _config['Property'] = {}
            _props = self.horizonvisconfig[hrz]['Property']
            for prop in _props:
                _idx_in_list = list.index(_all_property, prop)
                _d = {}
                _d['Colormap'] = self.ColorMapList[self.twgproperty.cellWidget(_idx_in_list, 1).currentIndex()]
                _d['Flip'] = self.twgproperty.cellWidget(_idx_in_list, 2).isChecked()
                _max = basic_data.str2float(self.twgproperty.item(_idx_in_list, 3).text())
                _min = basic_data.str2float(self.twgproperty.item(_idx_in_list, 4).text())
                if _max is False:
                    _max = 0
                if _min is False:
                    _min = 0
                _d['Minimum'] = _min
                _d['Maximum'] = _max
                #
                _config['Property'][prop] = _d
            #
            self.horizonvisconfig[hrz] = _config
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigHorizonVis = QtWidgets.QWidget()
    gui = confighorizonvis()
    gui.setupGUI(ConfigHorizonVis)
    ConfigHorizonVis.show()
    sys.exit(app.exec_())