#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for editing horizon


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.core.settings import settings as core_set
from gaeio.src.horizon.analysis import analysis as horizon_ays
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.gui.editdataproperty import editdataproperty as gui_editdataproperty

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class edithorizon(object):

    horizondata = {}
    rootpath = ''
    plotstyle = core_set.Visual['Image']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, EditHorizon):
        EditHorizon.setObjectName("EditHorizon")
        EditHorizon.setFixedSize(300, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        EditHorizon.setWindowIcon(icon)
        #
        self.lblhorizon = QtWidgets.QLabel(EditHorizon)
        self.lblhorizon.setObjectName("lblhorizon")
        self.lblhorizon.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwghorizon = QtWidgets.QListWidget(EditHorizon)
        self.lwghorizon.setObjectName("lwghorizon")
        self.lwghorizon.setGeometry(QtCore.QRect(10, 50, 280, 200))
        self.lwghorizon.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblaction = QtWidgets.QLabel(EditHorizon)
        self.lblaction.setObjectName("lblaction")
        self.lblaction.setGeometry(QtCore.QRect(110, 270, 40, 30))
        self.cbbaction = QtWidgets.QComboBox(EditHorizon)
        self.cbbaction.setObjectName("cbbaction")
        self.cbbaction.setGeometry(QtCore.QRect(160, 270, 130, 30))
        self.lblrename = QtWidgets.QLabel(EditHorizon)
        self.lblrename.setObjectName("lblrename")
        self.lblrename.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.ldtrename = QtWidgets.QLineEdit(EditHorizon)
        self.ldtrename.setObjectName("ldtrename")
        self.ldtrename.setGeometry(QtCore.QRect(200, 310, 90, 30))
        self.btnedit = QtWidgets.QPushButton(EditHorizon)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(100, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(EditHorizon)
        self.msgbox.setObjectName("msgbox")
        _center_x = EditHorizon.geometry().center().x()
        _center_y = EditHorizon.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(EditHorizon)
        QtCore.QMetaObject.connectSlotsByName(EditHorizon)


    def retranslateGUI(self, EditHorizon):
        self.dialog = EditHorizon
        #
        _translate = QtCore.QCoreApplication.translate
        EditHorizon.setWindowTitle(_translate("EditHorizon", "Edit Horizon"))
        self.lblhorizon.setText(_translate("EditHorizon", "Available horizon:"))
        self.lblaction.setText(_translate("EditHorizon", "Action:"))
        self.cbbaction.addItems(['Copy', 'Delete', 'Rename', 'Edit property'])
        self.cbbaction.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/copy.png")))
        self.cbbaction.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/delete.png")))
        self.cbbaction.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/rename.png")))
        self.cbbaction.setItemIcon(3, QtGui.QIcon(os.path.join(self.iconpath, "icons/pen.png")))
        self.cbbaction.setCurrentIndex(3)
        self.cbbaction.currentIndexChanged.connect(self.changeCbbAction)
        self.lblrename.setText(_translate("EditHorizon", ""))
        self.lblrename.setVisible(False)
        self.ldtrename.setText(_translate("EditHorizon", ""))
        self.ldtrename.setVisible(False)
        self.btnedit.setText(_translate("EditHorizon", "Apply"))
        self.btnedit.clicked.connect(self.clickBtnEditHorizon)
        #
        self.refreshLwgHorizon()


    def changeCbbAction(self):
        if self.cbbaction.currentIndex() == 2:
            self.lblrename.setText('Name:')
            self.lblrename.setVisible(True)
            self.ldtrename.setVisible(True)
        else:
            self.lblrename.setText('')
            self.lblrename.setVisible(False)
            self.ldtrename.setText('')
            self.ldtrename.setVisible(False)
        #
        if self.cbbaction.currentIndex() == 1:
            self.lwghorizon.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        else:
            self.lwghorizon.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


    def clickBtnEditHorizon(self):
        self.refreshMsgBox()
        #
        _horizonlist = self.lwghorizon.selectedItems()
        if len(_horizonlist) < 1:
            vis_msg.print("ERROR in EditHorizon: No horizon selected for editing", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Edit Horizon',
                                           'No horizon selected for editing')
            return
        #
        if self.cbbaction.currentIndex() == 0:
            self.horizondata[_horizonlist[0].text()+'_copy'] = self.horizondata[_horizonlist[0].text()].copy()
        if self.cbbaction.currentIndex() == 1:
            for _i in range(len(_horizonlist)):
                self.horizondata.pop(_horizonlist[_i].text())
        if self.cbbaction.currentIndex() == 2:
            if len(self.ldtrename.text()) < 1:
                vis_msg.print("ERROR in EditHorizon: No name specified for rename", type='error')
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Edit Horizon',
                                               'No name specified for rename')
                return
            if self.ldtrename.text() in self.horizondata.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Edit Horizon',
                                                       self.ldtrename.text() + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.No:
                    return
            self.horizondata[self.ldtrename.text()] = self.horizondata[_horizonlist[0].text()]
            self.horizondata.pop(_horizonlist[0].text())
        if self.cbbaction.currentIndex() == 3:
            _editproperty = QtWidgets.QDialog()
            _gui = gui_editdataproperty()
            _hrz = self.horizondata[_horizonlist[0].text()]
            _gui.dataproperty = horizon_ays.convertHorizon2PointSet(horizon=_hrz,
                                                                    property_list=list(_hrz['HorizonData'].keys()))
            _gui.rootpath = self.rootpath
            _gui.setupGUI(_editproperty)
            _editproperty.exec()
            _pts = _gui.dataproperty
            self.horizondata[_horizonlist[0].text()] = \
                horizon_ays.convertPointSet2Horizon(pointset=_pts, property_list=list(_pts.keys()))
            _editproperty.show()
        #
        self.refreshLwgHorizon()
        # if self.cbbaction.currentIndex() != 3:
            # QtWidgets.QMessageBox.information(self.msgbox,
            #                                   "Edit Horizon",
            #                                   "Horizon edited successfully")
        return


    def refreshLwgHorizon(self):
        self.lwghorizon.clear()
        if len(self.horizondata.keys()) > 0:
            for i in sorted(self.horizondata.keys()):
                if self.checkHorizonData(i):
                    item = QtWidgets.QListWidgetItem(self.lwghorizon)
                    item.setText(i)
                    self.lwghorizon.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkHorizonData(self, name):
        return horizon_ays.checkHorizon(self.horizondata[name])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditHorizon = QtWidgets.QWidget()
    gui = edithorizon()
    gui.setupGUI(EditHorizon)
    EditHorizon.show()
    sys.exit(app.exec_())