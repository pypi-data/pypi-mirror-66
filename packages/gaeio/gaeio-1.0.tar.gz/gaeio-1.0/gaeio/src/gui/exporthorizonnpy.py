#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for exporting horizon as numpy


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.matdict import matdict as basic_mdt
from gaeio.src.horizon.analysis import analysis as horizon_ays
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exporthorizonnpy(object):

    horizondata = {}
    #
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ExportHorionNpy):
        ExportHorionNpy.setObjectName("ExportHorionNpy")
        ExportHorionNpy.setFixedSize(400, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportHorionNpy.setWindowIcon(icon)
        #
        self.lblhorizon = QtWidgets.QLabel(ExportHorionNpy)
        self.lblhorizon.setObjectName("lblhorizon")
        self.lblhorizon.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwghorizon = QtWidgets.QListWidget(ExportHorionNpy)
        self.lwghorizon.setObjectName("lwghorizon")
        self.lwghorizon.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwghorizon.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbltype = QtWidgets.QLabel(ExportHorionNpy)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.cbbtype = QtWidgets.QComboBox(ExportHorionNpy)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(160, 230, 230, 30))
        self.lblsave = QtWidgets.QLabel(ExportHorionNpy)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 280, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportHorionNpy)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 280, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportHorionNpy)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 280, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportHorionNpy)
        self.btnexportnpy.setObjectName("btnexportnpy")
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 330, 160, 30))
        self.btnexportnpy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportHorionNpy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportHorionNpy.geometry().center().x()
        _center_y = ExportHorionNpy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportHorionNpy)
        QtCore.QMetaObject.connectSlotsByName(ExportHorionNpy)


    def retranslateGUI(self, ExportHorionNpy):
        self.dialog = ExportHorionNpy
        #
        _translate = QtCore.QCoreApplication.translate
        ExportHorionNpy.setWindowTitle(_translate("ExportHorionNpy", "Export Horizon NumPy"))
        self.lblhorizon.setText(_translate("ExportHorionNpy", "Select output horizons:"))
        if len(self.horizondata.keys()) > 0:
            for i in sorted(self.horizondata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwghorizon)
                item.setText(_translate("ExportHorionNpy", i))
                self.lwghorizon.addItem(item)
            self.lwghorizon.selectAll()
        self.lbltype.setText(_translate("ExportHorionNpy", "Select output type:"))
        self.cbbtype.addItems(['Dictionary (all in one)', 'Dictionary (individual)', '2-D numpy matrix'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/pydict.png")))
        self.cbbtype.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/pydict.png")))
        self.cbbtype.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/vis2d.png")))
        self.cbbtype.setCurrentIndex(1)
        self.lblsave.setText(_translate("ExportHorionNpy", "Save as:"))
        self.ldtsave.setText(_translate("ExportHorionNpy", ""))
        self.btnsave.setText(_translate("ExportHorionNpy", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate("ExportHorionNpy", "Export Horizon NumPy"))
        self.btnexportnpy.clicked.connect(self.clickBtnExportHorionNpy)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Horizon NumPy', self.rootpath,
                                        filter="Horizon NumPy files (*.hrz.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportHorionNpy(self):
        self.refreshMsgBox()
        #
        _horizonlist = self.lwghorizon.selectedItems()
        if len(_horizonlist) < 1:
            vis_msg.print("ERROR in ExportHorionNpy; No horizon selected for export", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Horizon NumPy',
                                           'No horizon selected for export')
            return
        #
        if len(self.ldtsave.text()) < 1:
            vis_msg.print("ERROR in ExportHorionNpy: No name specified for NumPy", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Horizon NumPy',
                                           'No name specified for NumPy')
            return
        print("ExportHorionNpy: Export %d horizons" % (len(_horizonlist)))
        #
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        #
        if len(_horizonlist) > 1 and self.cbbtype.currentIndex() >= 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Horizon Numpy',
                                                   'Warning: For exporting >=2 horizon, property name used as file name. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        if self.cbbtype.currentIndex() == 0:
            _npydata = {}
            for i in range(len(_horizonlist)):
                _npydata[_horizonlist[i].text()] = self.horizondata[_horizonlist[i].text()]
            #
            np.save(os.path.join(_savepath, _savename), _npydata)
        if self.cbbtype.currentIndex() == 1:
            for i in range(len(_horizonlist)):
                _data = self.horizondata[_horizonlist[i].text()]
                if len(_horizonlist) > 1:
                    _savename = _horizonlist[i].text() + '.hrz.npy'
                #
                np.save(os.path.join(_savepath, _savename), _data)
        if self.cbbtype.currentIndex() == 2:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Horizon Numpy',
                                                   'Warning: property header not saved in numpy matrix. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            for i in range(len(_horizonlist)):
                # convert to pointset
                _pointsetdata = \
                    horizon_ays.convertHorizon2PointSet(horizon=self.horizondata[_horizonlist[i].text()],
                                                        property_list=list(self.horizondata[_horizonlist[i].text()]['HorizonData'].keys()))
                _data = basic_mdt.exportMatDict(_pointsetdata, ['Inline', 'Crossline', 'Z'])
                for j in _pointsetdata.keys():
                    if j != 'Inline' and j != 'Crossline' and j != 'Z':
                        _data = np.concatenate((_data, _pointsetdata[j]), axis=1)
                #
                if len(_horizonlist) > 1:
                    _savename = _horizonlist[i].text() + '.hrz.npy'
                #
                np.save(os.path.join(_savepath, _savename), _data)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Horizon NumPy",
                                          str(len(_horizonlist)) + " horizons exported as NumPy successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportHorionNpy = QtWidgets.QWidget()
    gui = exporthorizonnpy()
    gui.setupGUI(ExportHorionNpy)
    ExportHorionNpy.show()
    sys.exit(app.exec_())