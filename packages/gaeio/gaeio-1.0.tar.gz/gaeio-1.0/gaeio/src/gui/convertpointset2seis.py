#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for converting point sets to seismic


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.basic.data import data as basic_data
from gaeio.src.basic.matdict import matdict as basic_mdt
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.seismic.analysis import analysis as seis_ays
from gaeio.src.vis.messager import messager as vis_msg

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class convertpointset2seis(object):

    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConvertPointSet2Seis):
        ConvertPointSet2Seis.setObjectName("ConvertPointSet2Seis")
        ConvertPointSet2Seis.setFixedSize(400, 410)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConvertPointSet2Seis.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 170, 30))
        self.lwgpoint = QtWidgets.QListWidget(ConvertPointSet2Seis)
        self.lwgpoint.setObjectName("lwgpoint")
        self.lwgpoint.setGeometry(QtCore.QRect(10, 50, 170, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblarrow = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblarrow.setObjectName("lblarrow")
        self.lblarrow.setGeometry(QtCore.QRect(180, 110, 40, 30))
        self.lblattrib = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(220, 10, 170, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertPointSet2Seis)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(220, 50, 170, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblvalue = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblvalue.setObjectName("lblvalue")
        self.lblvalue.setGeometry(QtCore.QRect(220, 270, 80, 30))
        self.ldtvalue = QtWidgets.QLineEdit(ConvertPointSet2Seis)
        self.ldtvalue.setObjectName("ldtvalue")
        self.ldtvalue.setGeometry(QtCore.QRect(310, 270, 80, 30))
        self.lbloverlap = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lbloverlap.setObjectName("lbloverlap")
        self.lbloverlap.setGeometry(QtCore.QRect(220, 310, 80, 30))
        self.cbboverlap = QtWidgets.QComboBox(ConvertPointSet2Seis)
        self.cbboverlap.setObjectName("cbboverlap")
        self.cbboverlap.setGeometry(QtCore.QRect(310, 310, 80, 30))
        self.btnapply = QtWidgets.QPushButton(ConvertPointSet2Seis)
        self.btnapply.setObjectName("btnedit")
        self.btnapply.setGeometry(QtCore.QRect(150, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConvertPointSet2Seis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConvertPointSet2Seis.geometry().center().x()
        _center_y = ConvertPointSet2Seis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConvertPointSet2Seis)
        QtCore.QMetaObject.connectSlotsByName(ConvertPointSet2Seis)


    def retranslateGUI(self, ConvertPointSet2Seis):
        self.dialog = ConvertPointSet2Seis
        #
        _translate = QtCore.QCoreApplication.translate
        ConvertPointSet2Seis.setWindowTitle(_translate("ConvertPointSet2Seis", "Convert PointSet to Seismic"))
        self.lblpoint.setText(_translate("ConvertPointSet2Seis", "Select pointsets:"))
        self.lwgpoint.itemSelectionChanged.connect(self.changeLwgPoint)
        self.lblarrow.setText(_translate("ConvertPointSet2Seis", "==>"))
        self.lblarrow.setAlignment(QtCore.Qt.AlignCenter)
        self.lblattrib.setText(_translate("ConvertPointSet2Seis", "Select properties:"))
        self.lblvalue.setText(_translate("ConvertPointSet2Seis", "Filling-up value:"))
        self.ldtvalue.setText(_translate("ConvertPointSet2Seis", "NaN"))
        self.lbloverlap.setText(_translate("ConvertPointSet2Seis", "Overlap points:"))
        self.cbboverlap.addItems(['Sum', 'Average', 'Maximum', 'Minimum'])
        self.btnapply.setText(_translate("ConvertPointSet2Seis", "Apply"))
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
        if _firstattrib is not None:
            self.lwgattrib.setCurrentItem(_firstattrib)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        _pointlist = self.lwgpoint.selectedItems()
        _pointlist = [f.text() for f in _pointlist]
        if len(_pointlist) < 1:
            vis_msg.print("ERROR in ConvertPointSet2Seis: No pointset selected for conversion", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Seismic',
                                           'No pointset selected for conversion')
            return
        #
        _attriblist = self.lwgattrib.selectedItems()
        _attriblist = [f.text() for f in _attriblist]
        if len(_attriblist) < 1:
            vis_msg.print("ERROR in ConvertPointSet2Seis: No property selected for conversion", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                            'Convert PointSet to Seismic',
                                            'No property selected for conversion')
            return
        #
        if basic_data.str2float(self.ldtvalue.text()) is False:
            vis_msg.print("ERROR in ConvertPointSet2Seis: Non-float filling-up value", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Seismic',
                                           'Non-float filling-up value')
            return
        #
        if checkSurvInfo(self.survinfo) is False:
            vis_msg.print("ERROR in ConvertPointSet2Seis: No seismic survey found for conversion", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Seismic',
                                           'No seismic survey found for conversion')
            return
        #
        for _f in _attriblist:
            if _f in self.seisdata.keys() and checkSeisData(self.seisdata[_f], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Convert PointSet to Seismic',
                                                       _f + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
        #
        _survinfo = self.survinfo
        for _f in _attriblist:
            _seisdata = np.zeros([_survinfo['ZNum'], _survinfo['XLNum'], _survinfo['ILNum']]) + \
                        basic_data.str2float(self.ldtvalue.text())
            for _p in _pointlist:
                _pointsetdata = basic_mdt.exportMatDict(self.pointsetdata[_p], ['Inline', 'Crossline', 'Z', _f])
                _pointsetdata = seis_ays.removeOutofSurveySample(_pointsetdata,
                                                              inlstart=_survinfo['ILStart'], inlend=_survinfo['ILEnd'],
                                                              xlstart=_survinfo['XLStart'], xlend=_survinfo['XLEnd'],
                                                              zstart=_survinfo['ZStart'], zend=_survinfo['ZEnd'])
                if np.shape(_pointsetdata)[0] < 1:
                    continue
                _ijk = seis_ays.convertIXZToIJK(_pointsetdata,
                                                inlstart=_survinfo['ILStart'], inlstep=_survinfo['ILStep'],
                                                xlstart=_survinfo['XLStart'], xlstep=_survinfo['XLStep'],
                                                zstart=_survinfo['ZStart'], zstep=_survinfo['ZStep'])
                for _i in range(np.shape(_ijk)[0]):
                    _ijk_i = int(_ijk[_i, 0])
                    _ijk_j = int(_ijk[_i, 1])
                    _ijk_k = int(_ijk[_i, 2])
                    _data = _seisdata[_ijk_k, _ijk_j, _ijk_i]
                    if (float(_data) == basic_data.str2float(self.ldtvalue.text()))\
                            or (np.isnan(_data) and np.isnan(basic_data.str2float(self.ldtvalue.text()))):
                        _seisdata[_ijk_k, _ijk_j, _ijk_i] = _pointsetdata[_i, 3]
                    else:
                        if self.cbboverlap.currentIndex() == 0:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = _pointsetdata[_i, 3] + _data
                        if self.cbboverlap.currentIndex() == 1:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = 0.5 * (_pointsetdata[_i, 3] + _data)
                        if self.cbboverlap.currentIndex() == 2:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = np.max([_pointsetdata[_i, 3], _data])
                        if self.cbboverlap.currentIndex() == 3:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = np.min([_pointsetdata[_i, 3], _data])

            self.seisdata[_f] = _seisdata
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Convert PointSet to Seismic",
                                          "PointSet converted successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointSet(self, name):
        return point_ays.checkPointSet(self.pointsetdata[name])

def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)

def checkSeisData(seisdata, survinfo):
    return seis_ays.isSeis3DMatConsistentWithSeisInfo(seisdata, survinfo)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConvertPointSet2Seis = QtWidgets.QWidget()
    gui = convertpointset2seis()
    gui.setupGUI(ConvertPointSet2Seis)
    ConvertPointSet2Seis.show()
    sys.exit(app.exec_())