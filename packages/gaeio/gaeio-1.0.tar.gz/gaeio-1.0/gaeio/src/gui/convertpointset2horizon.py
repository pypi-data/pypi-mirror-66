#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for converting point sets to horizons


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.data import data as basic_data
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.horizon.analysis import analysis as horizon_ays
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class convertpointset2horizon(object):

    horizondata = {}
    pointsetdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConvertPointSet2Horizon):
        ConvertPointSet2Horizon.setObjectName("ConvertPointSet2Horizon")
        ConvertPointSet2Horizon.setFixedSize(400, 360)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConvertPointSet2Horizon.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(ConvertPointSet2Horizon)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 170, 30))
        self.lwgpoint = QtWidgets.QListWidget(ConvertPointSet2Horizon)
        self.lwgpoint.setObjectName("lwgpoint")
        self.lwgpoint.setGeometry(QtCore.QRect(10, 50, 170, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblarrow = QtWidgets.QLabel(ConvertPointSet2Horizon)
        self.lblarrow.setObjectName("lblarrow")
        self.lblarrow.setGeometry(QtCore.QRect(180, 110, 40, 30))
        self.lblattrib = QtWidgets.QLabel(ConvertPointSet2Horizon)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(220, 10, 170, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertPointSet2Horizon)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(220, 50, 170, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblvalue = QtWidgets.QLabel(ConvertPointSet2Horizon)
        self.lblvalue.setObjectName("lblvalue")
        self.lblvalue.setGeometry(QtCore.QRect(220, 270, 80, 30))
        self.ldtvalue = QtWidgets.QLineEdit(ConvertPointSet2Horizon)
        self.ldtvalue.setObjectName("ldtvalue")
        self.ldtvalue.setGeometry(QtCore.QRect(310, 270, 80, 30))
        self.btnapply = QtWidgets.QPushButton(ConvertPointSet2Horizon)
        self.btnapply.setObjectName("btnedit")
        self.btnapply.setGeometry(QtCore.QRect(150, 310, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConvertPointSet2Horizon)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConvertPointSet2Horizon.geometry().center().x()
        _center_y = ConvertPointSet2Horizon.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConvertPointSet2Horizon)
        QtCore.QMetaObject.connectSlotsByName(ConvertPointSet2Horizon)


    def retranslateGUI(self, ConvertPointSet2Horizon):
        self.dialog = ConvertPointSet2Horizon
        #
        _translate = QtCore.QCoreApplication.translate
        ConvertPointSet2Horizon.setWindowTitle(_translate("ConvertPointSet2Horizon", "Convert PointSet to Horizon"))
        self.lblpoint.setText(_translate("ConvertPointSet2Horizon", "Select pointsets:"))
        self.lwgpoint.itemSelectionChanged.connect(self.changeLwgPoint)
        self.lblarrow.setText(_translate("ConvertPointSet2Horizon", "==>"))
        self.lblarrow.setAlignment(QtCore.Qt.AlignCenter)
        self.lblattrib.setText(_translate("ConvertPointSet2Horizon", "Select properties:"))
        self.lblvalue.setText(_translate("ConvertPointSet2Horizon", "Filling-up value:"))
        self.ldtvalue.setText(_translate("ConvertPointSet2Horizon", "NaN"))
        self.btnapply.setText(_translate("ConvertPointSet2Horizon", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        self.lwgpoint.clear()
        if len(self.pointsetdata.keys()) > 0:
            for i in sorted(self.pointsetdata.keys()):
                if self.checkPointSet(i):
                    item = QtWidgets.QListWidgetItem(self.lwgpoint)
                    item.setText(i)
                    self.lwgpoint.addItem(item)


    def changeLwgPoint(self):
        self.lwgattrib.clear()
        _firstattrib = None
        #
        _pointlist = self.lwgpoint.selectedItems()
        _pointlist = [f.text() for f in _pointlist]
        if len(_pointlist) > 0:
            for _k in self.pointsetdata[_pointlist[0]].keys():
                _flag = True
                for _i in range(len(_pointlist)):
                    if _k not in self.pointsetdata[_pointlist[_i]].keys():
                        _flag = False
                        break
                if _flag is True and _k != 'Inline' and _k != 'Crossline' and _k != 'Z':
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(_k)
                    self.lwgattrib.addItem(item)
                    if _firstattrib is None:
                        _firstattrib = item
        # if _firstattrib is not None:
        #     self.lwgattrib.setCurrentItem(_firstattrib)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        _pointlist = self.lwgpoint.selectedItems()
        _pointlist = [f.text() for f in _pointlist]
        if len(_pointlist) < 1:
            vis_msg.print("ERROR in ConvertPointSet2Horizon: No pointset selected for conversion", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Horizon',
                                           'No pointset selected for conversion')
            return
        #
        _attriblist = self.lwgattrib.selectedItems()
        _attriblist = [f.text() for f in _attriblist]
        #
        if basic_data.str2float(self.ldtvalue.text()) is False:
            vis_msg.print("ERROR in ConvertPointSet2Horizon: Non-float filling-up value", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Horizon',
                                           'Non-float filling-up value')
            return
        #
        for _f in _pointlist:
            if _f in self.horizondata.keys() and checkHorizonData(self.horizondata[_f]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Convert PointSet to Horizon',
                                                       _f + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
        #
        for _pts in _pointlist:
            self.horizondata[_pts] = \
                point_ays.convertPointSet2Horizon(self.pointsetdata[_pts], property_list=_attriblist,
                                                  filling_up_value=basic_data.str2float(self.ldtvalue.text()))
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Convert PointSet to Horizon",
                                          "PointSet converted successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointSet(self, name):
        return point_ays.checkPointSet(self.pointsetdata[name])


def checkHorizonData(horizondata):
    return horizon_ays.checkHorizon(horizondata)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConvertPointSet2Horizon = QtWidgets.QWidget()
    gui = convertpointset2horizon()
    gui.setupGUI(ConvertPointSet2Horizon)
    ConvertPointSet2Horizon.show()
    sys.exit(app.exec_())