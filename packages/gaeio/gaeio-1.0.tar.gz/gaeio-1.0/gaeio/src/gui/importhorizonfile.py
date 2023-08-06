#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for import horizons from a file


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.data import data as basic_data
from gaeio.src.horizon.inputoutput import inputoutput as horizon_io
from gaeio.src.horizon.analysis import analysis as horizon_ays
from gaeio.src.vis.messager import messager as vis_msg


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importhorizonfile(object):

    horizondata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    filelist = []

    def setupGUI(self, ImportHorionFile):
        ImportHorionFile.setObjectName("ImportHorionFile")
        ImportHorionFile.setFixedSize(600, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportHorionFile.setWindowIcon(icon)
        self.lblfile = QtWidgets.QLabel(ImportHorionFile)
        self.lblfile.setObjectName("lblfile")
        self.lblfile.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtfile = QtWidgets.QLineEdit(ImportHorionFile)
        self.ldtfile.setObjectName("ldtfile")
        self.ldtfile.setGeometry(QtCore.QRect(130, 10, 390, 30))
        self.btnfile = QtWidgets.QPushButton(ImportHorionFile)
        self.btnfile.setObjectName("btnfile")
        self.btnfile.setGeometry(QtCore.QRect(530, 10, 60, 30))
        self.lbltype = QtWidgets.QLabel(ImportHorionFile)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(30, 50, 100, 30))
        self.cbbtype = QtWidgets.QComboBox(ImportHorionFile)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(130, 50, 460, 30))
        #
        self.lblpara = QtWidgets.QLabel(ImportHorionFile)
        self.lblpara.setObjectName("lblpara")
        self.lblpara.setGeometry(QtCore.QRect(10, 100, 110, 30))
        self.lblinl = QtWidgets.QLabel(ImportHorionFile)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(20, 140, 100, 30))
        self.cbbinl = QtWidgets.QComboBox(ImportHorionFile)
        self.cbbinl.setObjectName("cbbinl")
        self.cbbinl.setGeometry(QtCore.QRect(130, 140, 60, 30))
        self.lblxl = QtWidgets.QLabel(ImportHorionFile)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(20, 180, 100, 30))
        self.cbbxl = QtWidgets.QComboBox(ImportHorionFile)
        self.cbbxl.setObjectName("cbbxl")
        self.cbbxl.setGeometry(QtCore.QRect(130, 180, 60, 30))
        self.lblz = QtWidgets.QLabel(ImportHorionFile)
        self.lblz.setObjectName("lbz")
        self.lblz.setGeometry(QtCore.QRect(20, 220, 100, 30))
        self.cbbz = QtWidgets.QComboBox(ImportHorionFile)
        self.cbbz.setObjectName("cbbz")
        self.cbbz.setGeometry(QtCore.QRect(130, 220, 60, 30))
        self.lblcomment = QtWidgets.QLabel(ImportHorionFile)
        self.lblcomment.setObjectName("lblcomment")
        self.lblcomment.setGeometry(QtCore.QRect(220, 140, 100, 30))
        self.cbbcomment = QtWidgets.QComboBox(ImportHorionFile)
        self.cbbcomment.setObjectName("cbbcomment")
        self.cbbcomment.setGeometry(QtCore.QRect(330, 140, 60, 30))
        self.lbldelimiter = QtWidgets.QLabel(ImportHorionFile)
        self.lbldelimiter.setObjectName("lbldelimiter")
        self.lbldelimiter.setGeometry(QtCore.QRect(220, 180, 100, 30))
        self.cbbdelimiter = QtWidgets.QComboBox(ImportHorionFile)
        self.cbbdelimiter.setObjectName("cbbdelimiter")
        self.cbbdelimiter.setGeometry(QtCore.QRect(330, 180, 60, 30))
        self.lblvalueundefined = QtWidgets.QLabel(ImportHorionFile)
        self.lblvalueundefined.setObjectName("lblvalueundefined")
        self.lblvalueundefined.setGeometry(QtCore.QRect(420, 140, 100, 30))
        self.ldtvalueundefined = QtWidgets.QLineEdit(ImportHorionFile)
        self.ldtvalueundefined.setObjectName("ldtvalueundefined")
        self.ldtvalueundefined.setGeometry(QtCore.QRect(530, 140, 60, 30))
        self.lblvaluefillup = QtWidgets.QLabel(ImportHorionFile)
        self.lblvaluefillup.setObjectName("lblvaluefillup")
        self.lblvaluefillup.setGeometry(QtCore.QRect(420, 180, 100, 30))
        self.ldtvaluefillup = QtWidgets.QLineEdit(ImportHorionFile)
        self.ldtvaluefillup.setObjectName("ldtvaluefillup")
        self.ldtvaluefillup.setGeometry(QtCore.QRect(530, 180, 60, 30))
        #
        self.btnimport = QtWidgets.QPushButton(ImportHorionFile)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(220, 270, 160, 30))
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportHorionFile)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportHorionFile.geometry().center().x()
        _center_y = ImportHorionFile.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportHorionFile)
        QtCore.QMetaObject.connectSlotsByName(ImportHorionFile)


    def retranslateGUI(self, ImportHorionFile):
        self.dialog = ImportHorionFile
        #
        _translate = QtCore.QCoreApplication.translate
        ImportHorionFile.setWindowTitle(_translate("ImportHorionFile", "Import Horizon from File"))
        self.lblfile.setText(_translate("ImportHorionFile", "Select horizon files:"))
        self.lblfile.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtfile.setText(_translate("ImportHorionFile", os.path.abspath(self.rootpath)))
        self.btnfile.setText(_translate("ImportHorionFile", "Browse"))
        self.btnfile.clicked.connect(self.clickBtnFile)
        self.lbltype.setText(_translate("ImportHorionFile", "\t    Type:"))
        self.cbbtype.addItems(['Kingdom 3D interpretation lines (ASCII) (*.*)',
                               'Seisworks 3D interpretation (ASCII) (*.*)',
                               'Customized (ASCII) (*.*)'])
        self.cbbtype.currentIndexChanged.connect(self.changeCbbType)
        #
        self.lblpara.setText(_translate("ImportHorionFile", "Settings:"))
        self.lblinl.setText(_translate("ImportHorionFile", "Inline column"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.cbbinl.addItems([str(i+1) for i in range(10)])
        self.cbbinl.setCurrentIndex(2)
        self.cbbinl.setEnabled(False)
        self.lblxl.setText(_translate("ImportHorionFile", "Crossline column:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.cbbxl.addItems([str(i + 1) for i in range(10)])
        self.cbbxl.setCurrentIndex(3)
        self.cbbxl.setEnabled(False)
        self.lblz.setText(_translate("ImportHorionFile", "Time/depth column:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.cbbz.addItems([str(i + 1) for i in range(10)])
        self.cbbz.setCurrentIndex(4)
        self.cbbz.setEnabled(False)
        self.lblcomment.setText(_translate("ImportHorionFile", "Header with "))
        self.lblcomment.setAlignment(QtCore.Qt.AlignRight)
        self.cbbcomment.addItems(['None', '#', '!'])
        self.cbbcomment.setCurrentIndex(0)
        self.cbbcomment.setEnabled(False)
        self.lbldelimiter.setText(_translate("ImportHorionFile", "Delimiter: "))
        self.lbldelimiter.setAlignment(QtCore.Qt.AlignRight)
        self.cbbdelimiter.addItems(['Space', 'Comma'])
        self.cbbdelimiter.setCurrentIndex(0)
        self.cbbdelimiter.setEnabled(False)
        self.lblvalueundefined.setText(_translate("ImportHorionFile", "Undefined value:"))
        self.lblvalueundefined.setAlignment(QtCore.Qt.AlignRight)
        self.ldtvalueundefined.setText(_translate("ImportHorionFile", "-999"))
        self.lblvaluefillup.setText(_translate("ImportHorionFile", "Filling-up value:"))
        self.lblvaluefillup.setAlignment(QtCore.Qt.AlignRight)
        self.ldtvaluefillup.setText(_translate("ImportHorionFile", "NaN"))
        #
        self.btnimport.setText(_translate("ImportHorionFile", "Import Horizon"))
        self.btnimport.clicked.connect(self.clickBtnImportHorionFile)


    def clickBtnFile(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Horizon File(s)', self.rootpath,
                                         filter="All files (*.*)")
        if len(_file[0]) > 0:
            self.filelist = _file[0]
            self.ldtfile.setText(str(_file[0]))


    def changeCbbType(self):
        if self.cbbtype.currentIndex() == 0:
            self.cbbinl.setCurrentIndex(2)
            self.cbbinl.setEnabled(False)
            self.cbbxl.setCurrentIndex(3)
            self.cbbxl.setEnabled(False)
            self.cbbz.setCurrentIndex(4)
            self.cbbz.setEnabled(False)
            self.cbbcomment.setCurrentIndex(0)
            self.cbbcomment.setEnabled(False)
            self.cbbdelimiter.setCurrentIndex(0)
            self.cbbdelimiter.setEnabled(False)
        if self.cbbtype.currentIndex() == 1:
            self.cbbinl.setCurrentIndex(0)
            self.cbbinl.setEnabled(False)
            self.cbbxl.setCurrentIndex(1)
            self.cbbxl.setEnabled(False)
            self.cbbz.setCurrentIndex(4)
            self.cbbz.setEnabled(False)
            self.cbbcomment.setCurrentIndex(0)
            self.cbbcomment.setEnabled(False)
            self.cbbdelimiter.setCurrentIndex(0)
            self.cbbdelimiter.setEnabled(False)
        if self.cbbtype.currentIndex() == 2:
            self.cbbinl.setCurrentIndex(4)
            self.cbbinl.setEnabled(True)
            self.cbbxl.setCurrentIndex(3)
            self.cbbxl.setEnabled(True)
            self.cbbz.setCurrentIndex(2)
            self.cbbz.setEnabled(True)
            self.cbbcomment.setCurrentIndex(1)
            self.cbbcomment.setEnabled(True)
            self.cbbdelimiter.setCurrentIndex(0)
            self.cbbdelimiter.setEnabled(True)


    def clickBtnImportHorionFile(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.filelist)
        if _nfile <= 0:
            vis_msg.print("ERROR in ImportHorizonFile: No file selected for import", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Horizon from File',
                                           'No file selected for import')
            return
        #
        _undefined_value = basic_data.str2float(self.ldtvalueundefined.text())
        if _undefined_value is False:
            vis_msg.print("ERROR in ImportHorizonFile: Non-float undefined value", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Horizon from File',
                                           'Nom-float undefined value')
            return
        _fillup_value = basic_data.str2float(self.ldtvaluefillup.text())
        if _fillup_value is False:
            vis_msg.print("ERROR in ImportHorizonFile: Non-float filled-up value", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Horizon from File',
                                           'Nom-float filled-up value')
            return
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import ' + str(_nfile) + ' Horizon files')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nfile)
        #
        _horizondata = {}
        #
        for i in range(_nfile):
            #
            QtCore.QCoreApplication.instance().processEvents()
            #
            _filename = self.filelist[i]
            print("ImportHorionFile: Import %d of %d horizon files: %s" % (i + 1, _nfile, _filename))
            #
            _comment = None
            if self.cbbcomment.currentIndex() == 0:
                _comment = None
            if self.cbbcomment.currentIndex() == 1:
                _comment = '#'
            if self.cbbcomment.currentIndex() == 2:
                _comment = '!'
            #
            _delimiter = None
            if self.cbbdelimiter.currentIndex() == 1:
                _delimiter = ','

            #
            _filenamemain = os.path.splitext(os.path.basename(_filename))[0]
            _horizondata[_filenamemain] = horizon_io.readHorizonFromAscii(_filename,
                                                                          comment=_comment,
                                                                          delimiter=_delimiter,
                                                                          inlcol=self.cbbinl.currentIndex(),
                                                                          xlcol=self.cbbxl.currentIndex(),
                                                                          zcol=self.cbbz.currentIndex(),
                                                                          filling_up_value=_fillup_value,
                                                                          undefined_value=_undefined_value)
            #
            # reverse the z
            if 'Z' in _horizondata[_filenamemain]['HorizonData'].keys():
                _z = _horizondata[_filenamemain]['HorizonData']['Z']
                if np.min(_z[~np.isnan(_z)]) >= 0:
                    _horizondata[_filenamemain]['HorizonData']['Z'] *= -1.0
            #
            _pgsdlg.setValue(i + 1)
            #
        #
        # add new data to horizondata
        for key in _horizondata.keys():
            if key in self.horizondata.keys() and checkHorizonData(self.horizondata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Horizon from File',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.horizondata[key] = _horizondata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Horizon from File",
                                          str(_nfile) + " file(s) imported successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


def checkHorizonData(horizon):
    return horizon_ays.checkHorizon(horizon)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportHorionFile = QtWidgets.QWidget()
    gui = importhorizonfile()
    gui.setupGUI(ImportHorionFile)
    ImportHorionFile.show()
    sys.exit(app.exec_())