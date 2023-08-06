#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for exporting horizon as ascii file


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.horizon.inputoutput import inputoutput as horizon_io

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exporthorizonfile(object):

    horizondata = {}
    #
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ExportHorizonFile):
        ExportHorizonFile.setObjectName("ExportHorizonFile")
        ExportHorizonFile.setFixedSize(400, 340)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportHorizonFile.setWindowIcon(icon)
        #
        self.lblhorizon = QtWidgets.QLabel(ExportHorizonFile)
        self.lblhorizon.setObjectName("lblhorizon")
        self.lblhorizon.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwghorizon = QtWidgets.QListWidget(ExportHorizonFile)
        self.lwghorizon.setObjectName("lwghorizon")
        self.lwghorizon.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwghorizon.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblsave = QtWidgets.QLabel(ExportHorizonFile)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 230, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportHorizonFile)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 230, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportHorizonFile)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 230, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportHorizonFile)
        self.btnexportnpy.setObjectName("btnexportnpy")
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 280, 160, 30))
        self.btnexportnpy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportHorizonFile)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportHorizonFile.geometry().center().x()
        _center_y = ExportHorizonFile.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportHorizonFile)
        QtCore.QMetaObject.connectSlotsByName(ExportHorizonFile)


    def retranslateGUI(self, ExportHorizonFile):
        self.dialog = ExportHorizonFile
        #
        _translate = QtCore.QCoreApplication.translate
        ExportHorizonFile.setWindowTitle(_translate("ExportHorizonFile", "Export Horizon File"))
        self.lblhorizon.setText(_translate("ExportHorizonFile", "Select output horizons:"))
        if len(self.horizondata.keys()) > 0:
            for i in sorted(self.horizondata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwghorizon)
                item.setText(_translate("ExportHorizonFile", i))
                self.lwghorizon.addItem(item)
            self.lwghorizon.selectAll()
        self.lblsave.setText(_translate("ExportHorizonFile", "Save as:"))
        self.ldtsave.setText(_translate("ExportHorizonFile", ""))
        self.btnsave.setText(_translate("ExportHorizonFile", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate("ExportHorizonFile", "Export Horizon File"))
        self.btnexportnpy.clicked.connect(self.clickBtnExportHorizonFile)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Horizon File', self.rootpath,
                                        filter="Horizon Ascii files (*.txt);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportHorizonFile(self):
        self.refreshMsgBox()
        #
        _horizonlist = self.lwghorizon.selectedItems()
        if len(_horizonlist) < 1:
            vis_msg.print("ERROR in ExportHorizonFile; No horizon selected for export", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Horizon FIle',
                                           'No horizon selected for export')
            return
        #
        if len(self.ldtsave.text()) < 1:
            vis_msg.print("ERROR in ExportHorizonFile: No name specified for export", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Horizon File',
                                           'No name specified for export')
            return
        print("ExportHorizonFile: Export %d horizons" % (len(_horizonlist)))
        #
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        #
        if len(_horizonlist) > 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Horizon File',
                                                   'Warning: For exporting >=2 horizon, property name used as file name. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        for i in range(len(_horizonlist)):
            if len(_horizonlist) > 1:
                _savename = _horizonlist[i].text()
            #
            horizon_io.writeHorizonToAscii(horizon=self.horizondata[_horizonlist[i].text()],
                                           asciifile=os.path.join(_savepath, _savename),
                                           property_list=list(self.horizondata[_horizonlist[i].text()].keys()))
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Horizon File",
                                          str(len(_horizonlist)) + " horizons exported as Ascii File successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportHorizonFile = QtWidgets.QWidget()
    gui = exporthorizonfile()
    gui.setupGUI(ExportHorizonFile)
    ExportHorizonFile.show()
    sys.exit(app.exec_())