#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for import points from a file


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.data import data as basic_data
from gaeio.src.pointset.inputoutput import inputoutput as point_io
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.vis.messager import messager as vis_msg


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importpointsetfile(object):

    pointsetdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    filelist = []

    def setupGUI(self, ImportPointSetFile):
        ImportPointSetFile.setObjectName("ImportPointSetFile")
        ImportPointSetFile.setFixedSize(600, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportPointSetFile.setWindowIcon(icon)
        self.lblfile = QtWidgets.QLabel(ImportPointSetFile)
        self.lblfile.setObjectName("lblfile")
        self.lblfile.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtfile = QtWidgets.QLineEdit(ImportPointSetFile)
        self.ldtfile.setObjectName("ldtfile")
        self.ldtfile.setGeometry(QtCore.QRect(130, 10, 390, 30))
        self.btnfile = QtWidgets.QPushButton(ImportPointSetFile)
        self.btnfile.setObjectName("btnfile")
        self.btnfile.setGeometry(QtCore.QRect(530, 10, 60, 30))
        self.lbltype = QtWidgets.QLabel(ImportPointSetFile)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(30, 50, 100, 30))
        self.cbbtype = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(130, 50, 460, 30))
        #
        self.lblpara = QtWidgets.QLabel(ImportPointSetFile)
        self.lblpara.setObjectName("lblpara")
        self.lblpara.setGeometry(QtCore.QRect(10, 100, 110, 30))
        self.lblinl = QtWidgets.QLabel(ImportPointSetFile)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(20, 140, 100, 30))
        self.cbbinl = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbinl.setObjectName("cbbinl")
        self.cbbinl.setGeometry(QtCore.QRect(130, 140, 60, 30))
        self.lblxl = QtWidgets.QLabel(ImportPointSetFile)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(20, 180, 100, 30))
        self.cbbxl = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbxl.setObjectName("cbbxl")
        self.cbbxl.setGeometry(QtCore.QRect(130, 180, 60, 30))
        self.lblz = QtWidgets.QLabel(ImportPointSetFile)
        self.lblz.setObjectName("lbz")
        self.lblz.setGeometry(QtCore.QRect(20, 220, 100, 30))
        self.cbbz = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbz.setObjectName("cbbz")
        self.cbbz.setGeometry(QtCore.QRect(130, 220, 60, 30))
        self.lblcomment = QtWidgets.QLabel(ImportPointSetFile)
        self.lblcomment.setObjectName("lblcomment")
        self.lblcomment.setGeometry(QtCore.QRect(220, 140, 100, 30))
        self.cbbcomment = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbcomment.setObjectName("cbbcomment")
        self.cbbcomment.setGeometry(QtCore.QRect(330, 140, 60, 30))
        self.lbldelimiter = QtWidgets.QLabel(ImportPointSetFile)
        self.lbldelimiter.setObjectName("lbldelimiter")
        self.lbldelimiter.setGeometry(QtCore.QRect(220, 180, 100, 30))
        self.cbbdelimiter = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbdelimiter.setObjectName("cbbdelimiter")
        self.cbbdelimiter.setGeometry(QtCore.QRect(330, 180, 60, 30))
        self.lblvalueundefined = QtWidgets.QLabel(ImportPointSetFile)
        self.lblvalueundefined.setObjectName("lblvalueundefined")
        self.lblvalueundefined.setGeometry(QtCore.QRect(420, 140, 100, 30))
        self.ldtvalueundefined = QtWidgets.QLineEdit(ImportPointSetFile)
        self.ldtvalueundefined.setObjectName("ldtvalueundefined")
        self.ldtvalueundefined.setGeometry(QtCore.QRect(530, 140, 60, 30))
        #
        self.btnimport = QtWidgets.QPushButton(ImportPointSetFile)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(220, 270, 160, 30))
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportPointSetFile)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportPointSetFile.geometry().center().x()
        _center_y = ImportPointSetFile.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportPointSetFile)
        QtCore.QMetaObject.connectSlotsByName(ImportPointSetFile)


    def retranslateGUI(self, ImportPointSetFile):
        self.dialog = ImportPointSetFile
        #
        _translate = QtCore.QCoreApplication.translate
        ImportPointSetFile.setWindowTitle(_translate("ImportPointSetFile", "Import PointSet from File"))
        self.lblfile.setText(_translate("ImportPointSetFile", "Select pointset files:"))
        self.lblfile.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtfile.setText(_translate("ImportPointSetFile", os.path.abspath(self.rootpath)))
        self.btnfile.setText(_translate("ImportPointSetFile", "Browse"))
        self.btnfile.clicked.connect(self.clickBtnFile)
        self.lbltype.setText(_translate("ImportPointSetFile", "\t    Type:"))
        self.cbbtype.addItems(['Kingdom 3D interpretation lines (ASCII) (*.*)',
                               'Seisworks 3D interpretation (ASCII) (*.*)',
                               'Customized (ASCII) (*.*)'])
        self.cbbtype.currentIndexChanged.connect(self.changeCbbType)
        #
        self.lblpara.setText(_translate("ImportPointSetFile", "Settings:"))
        self.lblinl.setText(_translate("ImportPointSetFile", "Inline column"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.cbbinl.addItems([str(i+1) for i in range(10)])
        self.cbbinl.setCurrentIndex(2)
        self.cbbinl.setEnabled(False)
        self.lblxl.setText(_translate("ImportPointSetFile", "Crossline column:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.cbbxl.addItems([str(i + 1) for i in range(10)])
        self.cbbxl.setCurrentIndex(3)
        self.cbbxl.setEnabled(False)
        self.lblz.setText(_translate("ImportPointSetFile", "Time/depth column:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.cbbz.addItems([str(i + 1) for i in range(10)])
        self.cbbz.setCurrentIndex(4)
        self.cbbz.setEnabled(False)
        self.lblcomment.setText(_translate("ImportPointSetFile", "Header with "))
        self.lblcomment.setAlignment(QtCore.Qt.AlignRight)
        self.cbbcomment.addItems(['None', '#', '!'])
        self.cbbcomment.setCurrentIndex(0)
        self.cbbcomment.setEnabled(False)
        self.lbldelimiter.setText(_translate("ImportPointSetFile", "Delimiter: "))
        self.lbldelimiter.setAlignment(QtCore.Qt.AlignRight)
        self.cbbdelimiter.addItems(['Space', 'Comma'])
        self.cbbdelimiter.setCurrentIndex(0)
        self.cbbdelimiter.setEnabled(False)
        self.lblvalueundefined.setText(_translate("ImportPointSetFile", "Undefined value:"))
        self.lblvalueundefined.setAlignment(QtCore.Qt.AlignRight)
        self.ldtvalueundefined.setText(_translate("ImportHorionFile", "-999"))
        #
        self.btnimport.setText(_translate("ImportPointSetFile", "Import PointSet"))
        self.btnimport.clicked.connect(self.clickBtnImportPointSetFile)


    def clickBtnFile(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select PointSet File(s)', self.rootpath,
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


    def clickBtnImportPointSetFile(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.filelist)
        if _nfile <= 0:
            vis_msg.print("ERROR in ImportPointSetFile: No file selected for import", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet from File',
                                           'No file selected for import')
            return
        #
        _undefined_value = basic_data.str2float(self.ldtvalueundefined.text())
        if _undefined_value is False:
            vis_msg.print("ERROR in ImportPointSetFile: Non-float undefined value", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet from File',
                                           'Nom-float undefined value')
            return
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import ' + str(_nfile) + ' PointSet files')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nfile)
        #
        _pointsetdata = {}
        #
        for i in range(_nfile):
            #
            QtCore.QCoreApplication.instance().processEvents()
            #
            _filename = self.filelist[i]
            print("ImportPointSetFile: Import %d of %d pointset files: %s" % (i + 1, _nfile, _filename))
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
            _pointsetdata[_filenamemain] = point_io.readPointSetFromAscii(_filename,
                                                                          comment=_comment,
                                                                          delimiter=_delimiter,
                                                                          inlcol=self.cbbinl.currentIndex(),
                                                                          xlcol=self.cbbxl.currentIndex(),
                                                                          zcol=self.cbbz.currentIndex(),
                                                                          undefined_value=_undefined_value)
            #
            if 'Z' in _pointsetdata[_filenamemain].keys() and np.min(_pointsetdata[_filenamemain]['Z']) >= 0:
                _pointsetdata[_filenamemain]['Z'] = - _pointsetdata[_filenamemain]['Z']
            #
            _pgsdlg.setValue(i + 1)
            #
        #
        # add new data to seisdata
        for key in _pointsetdata.keys():
            if key in self.pointsetdata.keys() and checkPointSetData(self.pointsetdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import PointSet from File',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.pointsetdata[key] = _pointsetdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import PointSet from File",
                                          str(_nfile) + " file(s) imported successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


def checkPointSetData(pointdata):
    return point_ays.checkPointSet(pointdata)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportPointSetFile = QtWidgets.QWidget()
    gui = importpointsetfile()
    gui.setupGUI(ImportPointSetFile)
    ImportPointSetFile.show()
    sys.exit(app.exec_())