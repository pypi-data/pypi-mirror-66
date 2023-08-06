#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for calculating seismic attribute (math) (single)


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.seismic.analysis import analysis as seis_ays
from gaeio.src.seismic.attribute import attribute as seis_attrib
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.gui.calculator import calculator as gui_calculator

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class calcmathattribsingle(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    mathattriblist = ['Calculator', 'Cumulative sum', 'First derivative (with z)']


    def setupGUI(self, CalcMathAttribSingle):
        CalcMathAttribSingle.setObjectName("CalcMathAttribSingle")
        CalcMathAttribSingle.setFixedSize(500, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/file.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        CalcMathAttribSingle.setWindowIcon(icon)
        #
        self.lblproperty = QtWidgets.QLabel(CalcMathAttribSingle)
        self.lblproperty.setObjectName("lblproperty")
        self.lblproperty.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgproperty = QtWidgets.QListWidget(CalcMathAttribSingle)
        self.lwgproperty.setObjectName("lwgproperty")
        self.lwgproperty.setGeometry(QtCore.QRect(10, 50, 480, 200))
        self.lwgproperty.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblattrib = QtWidgets.QLabel(CalcMathAttribSingle)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 270, 230, 30))
        self.cbbattrib = QtWidgets.QComboBox(CalcMathAttribSingle)
        self.cbbattrib.setObjectName("cbbattrib")
        self.cbbattrib.setGeometry(QtCore.QRect(10, 310, 230, 30))
        self.lblname = QtWidgets.QLabel(CalcMathAttribSingle)
        self.lblname.setObjectName("lblname")
        self.lblname.setGeometry(QtCore.QRect(310, 310, 80, 30))
        self.ldtname = QtWidgets.QLineEdit(CalcMathAttribSingle)
        self.ldtname.setObjectName("ldtname")
        self.ldtname.setGeometry(QtCore.QRect(390, 310, 100, 30))
        self.btnapply = QtWidgets.QPushButton(CalcMathAttribSingle)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(200, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(CalcMathAttribSingle)
        self.msgbox.setObjectName("msgbox")
        _center_x = CalcMathAttribSingle.geometry().center().x()
        _center_y = CalcMathAttribSingle.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(CalcMathAttribSingle)
        QtCore.QMetaObject.connectSlotsByName(CalcMathAttribSingle)


    def retranslateGUI(self, CalcMathAttribSingle):
        self.dialog = CalcMathAttribSingle
        #
        _translate = QtCore.QCoreApplication.translate
        CalcMathAttribSingle.setWindowTitle(_translate("CalcMathAttribSingle", "Calculate Math Attribute from Single Property"))
        self.lblproperty.setText(_translate("CalcMathAttribSingle", "Select target property:"))
        self.lblattrib.setText(_translate("CalcMathAttribSingle", "Select attribute:"))
        self.cbbattrib.addItems(self.mathattriblist)
        self.cbbattrib.currentIndexChanged.connect(self.changeCbbAttrib)
        self.lblname.setText(_translate("CalcMathAttribSingle", "Output name:"))
        self.ldtname.setText(_translate("CalcMathAttribSingle", "Calculator"))
        self.btnapply.setText(_translate("CalcMathAttribSingle", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnCalcMathAttribSingle)
        #
        self.refreshLwgProperty()


    def changeCbbAttrib(self):
        if self.cbbattrib.currentIndex() == 0:
            self.ldtname.setText('Calculator')
        if self.cbbattrib.currentIndex() == 1:
            self.ldtname.setText('CuSum')
        if self.cbbattrib.currentIndex() == 2:
            self.ldtname.setText('dZ')


    def clickBtnCalcMathAttribSingle(self):
        self.refreshMsgBox()
        #
        _propertylist = self.lwgproperty.selectedItems()
        if len(_propertylist) < 1:
            vis_msg.print("ERROR in CalcMathAttribSingle: No property selected for attribute analysis", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Calculate Math Attribute from Single Property',
                                           'No property selected for attribute analysis')
            return
        if len(self.ldtname.text()) < 1:
            vis_msg.print("ERROR in CalcMathAttribSingle: No name specified for output attribute", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Calculate Math Attribute from Single Property',
                                           'No name specified for output attribute')
            return
        if self.ldtname.text() in self.seisdata.keys() and self.checkSeisData(self.ldtname.text()):
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Calculate Math Attribute from Single Property',
                                                   self.ldtname.text() + ' already exists. Overwrite?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        _seisdata = self.seisdata[_propertylist[0].text()]
        #
        if self.cbbattrib.currentIndex() == 0:
            _math = QtWidgets.QDialog()
            _gui = gui_calculator()
            _gui.data = _seisdata
            _gui.setupGUI(_math)
            _math.exec()
            self.seisdata[self.ldtname.text()] = _gui.data.copy()
            _math.show()
        if self.cbbattrib.currentIndex() == 1:
            _attrib = seis_attrib.calcCumulativeSum(_seisdata)
            self.seisdata[self.ldtname.text()] = _attrib
        if self.cbbattrib.currentIndex() == 2:
            _attrib = seis_attrib.calcFirstDerivative(_seisdata)
            self.seisdata[self.ldtname.text()] = _attrib
        #
        self.refreshLwgProperty()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Calculate Math Attribute from Single Property",
                                          self.mathattriblist[self.cbbattrib.currentIndex()] + " calculated successfully")
        return


    def refreshLwgProperty(self):
        self.lwgproperty.clear()
        if self.checkSurvInfo() is True:
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i) is True:
                    item = QtWidgets.QListWidgetItem(self.lwgproperty)
                    item.setText(i)
                    self.lwgproperty.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("CalcMathAttribSingle: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Calculate Math Attribute from Single Property',
            #                                'Survey not found')
            return False
        return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        #
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CalcMathAttribSingle = QtWidgets.QWidget()
    gui = calcmathattribsingle()
    gui.setupGUI(CalcMathAttribSingle)
    CalcMathAttribSingle.show()
    sys.exit(app.exec_())