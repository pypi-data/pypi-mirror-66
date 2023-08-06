#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for converting horizon to pointset


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


class converthorizon2pointset(object):

    survinfo = {}
    horizondata = {}
    pointsetdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConvertHorizon2PointSet):
        ConvertHorizon2PointSet.setObjectName("ConvertHorizon2PointSet")
        ConvertHorizon2PointSet.setFixedSize(400, 370)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConvertHorizon2PointSet.setWindowIcon(icon)
        #
        self.lblhorizon = QtWidgets.QLabel(ConvertHorizon2PointSet)
        self.lblhorizon.setObjectName("lblhorizon")
        self.lblhorizon.setGeometry(QtCore.QRect(10, 10, 170, 30))
        self.lwghorizon = QtWidgets.QListWidget(ConvertHorizon2PointSet)
        self.lwghorizon.setObjectName("lwghorizon")
        self.lwghorizon.setGeometry(QtCore.QRect(10, 50, 170, 200))
        self.lwghorizon.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblarrow = QtWidgets.QLabel(ConvertHorizon2PointSet)
        self.lblarrow.setObjectName("lblarrow")
        self.lblarrow.setGeometry(QtCore.QRect(180, 110, 40, 30))
        self.lblattrib = QtWidgets.QLabel(ConvertHorizon2PointSet)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(220, 10, 170, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertHorizon2PointSet)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(220, 50, 170, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblvalue = QtWidgets.QLabel(ConvertHorizon2PointSet)
        self.lblvalue.setObjectName("lblvalue")
        self.lblvalue.setGeometry(QtCore.QRect(220, 270, 80, 30))
        self.ldtvalue = QtWidgets.QLineEdit(ConvertHorizon2PointSet)
        self.ldtvalue.setObjectName("ldtvalue")
        self.ldtvalue.setGeometry(QtCore.QRect(310, 270, 80, 30))
        self.btnapply = QtWidgets.QPushButton(ConvertHorizon2PointSet)
        self.btnapply.setObjectName("btnedit")
        self.btnapply.setGeometry(QtCore.QRect(150, 320, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConvertHorizon2PointSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConvertHorizon2PointSet.geometry().center().x()
        _center_y = ConvertHorizon2PointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConvertHorizon2PointSet)
        QtCore.QMetaObject.connectSlotsByName(ConvertHorizon2PointSet)


    def retranslateGUI(self, ConvertHorizon2PointSet):
        self.dialog = ConvertHorizon2PointSet
        #
        _translate = QtCore.QCoreApplication.translate
        ConvertHorizon2PointSet.setWindowTitle(_translate("ConvertHorizon2PointSet", "Convert Horizon to PointSet"))
        self.lblhorizon.setText(_translate("ConvertHorizon2PointSet", "Select horizons:"))
        self.lwghorizon.itemSelectionChanged.connect(self.changeLwgHorizon)
        self.lblarrow.setText(_translate("ConvertHorizon2PointSet", "==>"))
        self.lblarrow.setAlignment(QtCore.Qt.AlignCenter)
        self.lblattrib.setText(_translate("ConvertHorizon2PointSet", "Select properties:"))
        self.lblvalue.setText(_translate("ConvertPointSet2Seis", "Undefined value:"))
        self.ldtvalue.setText(_translate("ConvertPointSet2Seis", "NAN"))
        self.btnapply.setText(_translate("ConvertHorizon2PointSet", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        self.lwghorizon.clear()
        if type(self.horizondata) is dict and len(self.horizondata.keys()) > 0:
            for i in sorted(self.horizondata.keys()):
                if checkHorizonData(self.horizondata[i]):
                    item = QtWidgets.QListWidgetItem(self.lwghorizon)
                    item.setText(i)
                    self.lwghorizon.addItem(item)


    def changeLwgHorizon(self):
        self.lwgattrib.clear()
        _firstattrib = None
        #
        _horizonlist = self.lwghorizon.selectedItems()
        _horizonlist = [f.text() for f in _horizonlist]
        if len(_horizonlist) > 0:
            for _k in self.horizondata[_horizonlist[0]]['HorizonData'].keys():
                _flag = True
                for _i in range(len(_horizonlist)):
                    if _k not in self.horizondata[_horizonlist[_i]]['HorizonData'].keys():
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
        _horizonlist = self.lwghorizon.selectedItems()
        _horizonlist = [f.text() for f in _horizonlist]
        if len(_horizonlist) < 1:
            vis_msg.print("ERROR in ConvertHorizon2PointSet: No horizon selected for conversion", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert Horizon to PointSet',
                                           'No horizon selected for conversion')
            return
        #
        _attriblist = self.lwgattrib.selectedItems()
        _attriblist = [f.text() for f in _attriblist]
        #
        if basic_data.str2float(self.ldtvalue.text()) is False:
            vis_msg.print("ERROR in ConvertHorizon2PointSet: Non-float undefined value", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert Horizon to PointSet',
                                           'Non-float undefined value')
            return
        #
        for _f in _horizonlist:
            if _f in self.pointsetdata.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Convert Horizon to PointSet',
                                                       _f + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
        #
        for _hrz in _horizonlist:
            self.pointsetdata[_hrz] =\
                horizon_ays.convertHorizon2PointSet(self.horizondata[_hrz], property_list=_attriblist,
                                                    undefined_value=basic_data.str2float(self.ldtvalue.text()))
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Convert Horizon to PointSet",
                                          "Horizon converted successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


def checkPointSetData(pointset):
    return point_ays.checkPointSet(pointset)

def checkHorizonData(horizon):
    return horizon_ays.checkHorizon(horizon)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConvertHorizon2PointSet = QtWidgets.QWidget()
    gui = converthorizon2pointset()
    gui.setupGUI(ConvertHorizon2PointSet)
    ConvertHorizon2PointSet.show()
    sys.exit(app.exec_())