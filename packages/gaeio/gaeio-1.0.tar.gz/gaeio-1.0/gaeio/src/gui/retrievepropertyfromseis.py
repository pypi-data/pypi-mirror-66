#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for retrieving seismic properties from a given numpy dictionary


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.seismic.analysis import analysis as seis_ays
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.basic.data import data as basic_data
from gaeio.src.basic.matdict import matdict as basic_mdt
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class retrievepropertyfromseis(object):

    pointsetdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    npydata = None
    npyinfo = {}


    def setupGUI(self, RetrievePropertyFromSeis):
        RetrievePropertyFromSeis.setObjectName("RetrievePropertyFromSeis")
        RetrievePropertyFromSeis.setFixedSize(400, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/retrieve.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        RetrievePropertyFromSeis.setWindowIcon(icon)
        #
        self.lblfrom = QtWidgets.QLabel(RetrievePropertyFromSeis)
        self.lblfrom.setObjectName("lblfrom")
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.ldtfrom = QtWidgets.QLineEdit(RetrievePropertyFromSeis)
        self.ldtfrom.setObjectName("ldtfrom")
        self.ldtfrom.setGeometry(QtCore.QRect(160, 10, 160, 30))
        self.btnfrom = QtWidgets.QPushButton(RetrievePropertyFromSeis)
        self.btnfrom.setObjectName("btnfrom")
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblattrib = QtWidgets.QLabel(RetrievePropertyFromSeis)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 50, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(RetrievePropertyFromSeis)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(160, 50, 230, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbldims = QtWidgets.QLabel(RetrievePropertyFromSeis)
        self.lbldims.setObjectName("lbldims")
        self.lbldims.setGeometry(QtCore.QRect(10, 270, 150, 30))
        self.ldtdimsinl = QtWidgets.QLineEdit(RetrievePropertyFromSeis)
        self.ldtdimsinl.setObjectName("ldtdimsinl")
        self.ldtdimsinl.setGeometry(QtCore.QRect(160, 270, 60, 30))
        self.ldtdimsxl = QtWidgets.QLineEdit(RetrievePropertyFromSeis)
        self.ldtdimsxl.setObjectName("ldtdimsxl")
        self.ldtdimsxl.setGeometry(QtCore.QRect(245, 270, 60, 30))
        self.ldtdimsz = QtWidgets.QLineEdit(RetrievePropertyFromSeis)
        self.ldtdimsz.setObjectName("ldtdimsz")
        self.ldtdimsz.setGeometry(QtCore.QRect(330, 270, 60, 30))
        self.btnrtrvprop = QtWidgets.QPushButton(RetrievePropertyFromSeis)
        self.btnrtrvprop.setObjectName("btnrtrvprop")
        self.btnrtrvprop.setGeometry(QtCore.QRect(120, 330, 160, 30))
        self.btnrtrvprop.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(RetrievePropertyFromSeis)
        self.msgbox.setObjectName("msgbox")
        _center_x = RetrievePropertyFromSeis.geometry().center().x()
        _center_y = RetrievePropertyFromSeis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(RetrievePropertyFromSeis)
        QtCore.QMetaObject.connectSlotsByName(RetrievePropertyFromSeis)


    def retranslateGUI(self, RetrievePropertyFromSeis):
        self.dialog = RetrievePropertyFromSeis
        #
        _translate = QtCore.QCoreApplication.translate
        RetrievePropertyFromSeis.setWindowTitle(_translate("RetrievePropertyFromSeis",
                                                           "Retrieve Data Property from Seismic"))
        self.lblfrom.setText(_translate("RetrievePropertyFromSeis", "Seismic NumPy Dictionary:"))
        self.ldtfrom.setText(_translate("RetrievePropertyFromSeis", ""))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate("RetrievePropertyFromSeis", "Browse"))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblattrib.setText(_translate("RetrievePropertyFromSeis", "Select target properties:"))
        self.lbldims.setText(_translate("RetrievePropertyFromSeis", "Retrieval radius (IL/XL/Z):"))
        self.ldtdimsinl.setText(_translate("RetrievePropertyFromSeis", "0"))
        self.ldtdimsinl.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsxl.setText(_translate("RetrievePropertyFromSeis", "0"))
        self.ldtdimsxl.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsz.setText(_translate("RetrievePropertyFromSeis", "0"))
        self.ldtdimsz.setAlignment(QtCore.Qt.AlignCenter)
        self.btnrtrvprop.setText(_translate("RetrievePropertyFromSeis", "Retrieve Property"))
        self.btnrtrvprop.clicked.connect(self.clickBtnRetrievePropertyFromSeis)


    def changeLdtFrom(self):
        self.refreshMsgBox()
        #
        self.lwgattrib.clear()
        #
        if os.path.exists(self.ldtfrom.text()) is False:
            vis_msg.print("ERROR in RetrievePropertyFromSeis: No NumPy selected for retrieval", type='error')
            return
        #
        try:
            self.npydata = np.load(self.ldtfrom.text(), allow_pickle=True).item()
            if ('SeisInfo' not in self.npydata.keys())\
                    or (seis_ays.checkSeisInfo(self.npydata['SeisInfo']) is False):
                vis_msg.print("ERROR in RetrievePropertyFromSeis: NumPy dictionary contains no information about seismic survey",
                              type='error')
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Retrieve Data Property from Seismic',
                                               'NumPy dictionary contains no information about seismic')
                return
            self.npyinfo = self.npydata['SeisInfo']
            self.npydata.pop('SeisInfo')
            if 'SeisData' in self.npydata.keys() and type(self.npydata['SeisData']) is dict:
                for key in self.npydata['SeisData'].keys():
                    if checkSeisData(self.npydata['SeisData'][key], self.npyinfo) is False:
                        self.npydata['SeisData'].pop(key)
            if 'SeisData' in self.npydata.keys() and type(self.npydata['SeisData']) is not dict:
                _filename = (os.path.basename(self.ldtfrom.text())).replace('.seis.npy', '')
                _data = {}
                if checkSeisData(self.npydata['SeisData'], self.npyinfo) is True:
                    _data[_filename] = self.npydata['SeisData']
                self.npydata['SeisData'] = _data
        except ValueError:
            vis_msg.print("ERROR in RetrievePropertyFromSeis: NumPy Dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Retrieve Data Property from Seismic',
                                           'NumPy dictionary expected')
            return
        #
        if seis_ays.checkSeisInfo(self.npyinfo) is False:
            vis_msg.print("ERROR in RetrievePropertyFromSeis: Selected not seismic numpy", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Retrieve Data Property from Seismic',
                                           'Selected not seismic numpy')
            return
        #
        _firstattrib = None
        for i in sorted(self.npydata['SeisData'].keys()):
            item = QtWidgets.QListWidgetItem(self.lwgattrib)
            item.setText(i)
            self.lwgattrib.addItem(item)
            if _firstattrib is None:
                _firstattrib = item
        self.lwgattrib.setCurrentItem(_firstattrib)


    def clickBtnFrom(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Seismic NumPy Dictionary', self.rootpath,
                                        filter="NumPy files (*.seis.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])



    def clickBtnRetrievePropertyFromSeis(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if len(_attriblist) < 1:
            vis_msg.print("ERROR in RtrvSeisProb: No property selected for retrieval", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Retrieve Data Property from Seismic',
                                           'No property selected for export')
            return
        if self.checkPointSetData() is False:
            vis_msg.print("ERROR in RetrievePropertyFromSeis: No point loaded for retrieval", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Retrieve Data Property from Seismic',
                                           'No point loaded for retrieval')
            return
        #
        _wdinl = basic_data.str2int(self.ldtdimsinl.text())
        _wdxl = basic_data.str2int(self.ldtdimsxl.text())
        _wdz = basic_data.str2int(self.ldtdimsz.text())
        if _wdinl is False or _wdxl is False or _wdz is False:
            vis_msg.print("ERROR in RetrievePropertyFromSeis: Non-integer retrieval window", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Retrieve Data Property from Seismic',
                                           'Non-integer retrieval window')
            return
        if _wdinl < 0 or _wdxl < 0 or _wdz < 0:
            vis_msg.print("ERROR in RetrievePropertyFromSeis: Non-positive retrieval window", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Retrieve Data Property from Seismic',
                                           'Non-positive retrieval window')
            return
        #
        _wdsize = (2*_wdinl+1)*(2*_wdxl+1)*(2*_wdz+1)
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/retrieve.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Retrieve Seismic Property')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        #
        _targetdata = basic_mdt.exportMatDict(self.pointsetdata, ['Inline', 'Crossline', 'Z'])
        #
        for i in range(len(_attriblist)):
            #
            _pgsdlg.setWindowTitle('Retrieve ' + str(i + 1) + ' of ' + str(len(_attriblist)) + ' Property')
            #
            print("RetrievePropertyFromSeis: Retrieve %d of %d Properties: %s" % (i + 1, len(_attriblist), _attriblist[i].text()))
            _npydata = self.npydata['SeisData'][_attriblist[i].text()]
            _data = seis_ays.retrieveSeisWindowFrom3DMat(_npydata, _targetdata, seisinfo=self.npyinfo,
                                                         wdinl=_wdinl, wdxl=_wdxl, wdz=_wdz,
                                                         verbose=False, qpgsdlg=_pgsdlg)
            _data = _data[:, 3:3+_wdsize]
            _data = np.mean(_data, axis=1)
            _data = np.reshape(_data, [-1, 1])

            #
            if _attriblist[i].text() in self.pointsetdata.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Retrieve Data Property from Seismic',
                                                       _attriblist[i].text() + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.pointsetdata[_attriblist[i].text()] = np.reshape(_data, [-1, 1])
            #
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Retrieve Data Property from Seismic",
                                          str(len(_attriblist)) + " properties retrieved successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointSetData(self):
        return point_ays.checkPointSet(self.pointsetdata)


def checkSeisData(seisdata, survinfo={}):
    return seis_ays.isSeis3DMatConsistentWithSeisInfo(seisdata, survinfo)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RetrievePropertyFromSeis = QtWidgets.QWidget()
    gui = retrievepropertyfromseis()
    gui.setupGUI(RetrievePropertyFromSeis)
    RetrievePropertyFromSeis.show()
    sys.exit(app.exec_())