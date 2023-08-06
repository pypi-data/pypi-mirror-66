#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a window for editing data properties


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.gui.retrievepropertyfromseis import retrievepropertyfromseis as gui_retrievepropertyfromseis
from gaeio.src.gui.calculator import calculator as gui_calculator

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class editdataproperty(object):

    dataproperty = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, EditDataProperty):
        EditDataProperty.setObjectName("EditDataProperty")
        EditDataProperty.setFixedSize(300, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/attribute.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        EditDataProperty.setWindowIcon(icon)
        #
        self.lblattrib = QtWidgets.QLabel(EditDataProperty)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(EditDataProperty)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(10, 50, 280, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblaction = QtWidgets.QLabel(EditDataProperty)
        self.lblaction.setObjectName("lblaction")
        self.lblaction.setGeometry(QtCore.QRect(110, 270, 40, 30))
        self.cbbaction = QtWidgets.QComboBox(EditDataProperty)
        self.cbbaction.setObjectName("cbbaction")
        self.cbbaction.setGeometry(QtCore.QRect(160, 270, 130, 30))
        self.ldtrename = QtWidgets.QLineEdit(EditDataProperty)
        self.ldtrename.setObjectName("ldtrename")
        self.ldtrename.setGeometry(QtCore.QRect(160, 310, 130, 30))
        self.btnedit = QtWidgets.QPushButton(EditDataProperty)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(100, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(EditDataProperty)
        self.msgbox.setObjectName("msgbox")
        _center_x = EditDataProperty.geometry().center().x()
        _center_y = EditDataProperty.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(EditDataProperty)
        QtCore.QMetaObject.connectSlotsByName(EditDataProperty)


    def retranslateGUI(self, EditDataProperty):
        self.dialog = EditDataProperty
        #
        _translate = QtCore.QCoreApplication.translate
        EditDataProperty.setWindowTitle(_translate("EditDataProperty", "Edit Property"))
        self.lblattrib.setText(_translate("EditDataProperty", "List of available properties:"))
        self.lblaction.setText(_translate("EditDataProperty", "Action:"))
        self.cbbaction.addItems(['Copy', 'Rename', 'Delete', 'Add', 'Math'])
        self.cbbaction.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/copy.png")))
        self.cbbaction.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/rename.png")))
        self.cbbaction.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/delete.png")))
        self.cbbaction.setItemIcon(3, QtGui.QIcon(os.path.join(self.iconpath, "icons/retrieve.png")))
        self.cbbaction.setItemIcon(4, QtGui.QIcon(os.path.join(self.iconpath, "icons/math.png")))
        self.cbbaction.setCurrentIndex(4)
        self.cbbaction.currentIndexChanged.connect(self.changeCbbAction)
        self.ldtrename.setText(_translate("EditDataProperty", ""))
        self.ldtrename.setVisible(False)
        self.btnedit.setText(_translate("EditDataProperty", "Apply"))
        self.btnedit.clicked.connect(self.clickBtnEditDataProperty)
        #
        self.refreshLwgAttrib()


    def changeCbbAction(self):
        if self.cbbaction.currentIndex() == 1:
            self.ldtrename.setVisible(True)
        else:
            self.ldtrename.setText('')
            self.ldtrename.setVisible(False)
        if self.cbbaction.currentIndex() == 2:
            self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        else:
            self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)



    def clickBtnEditDataProperty(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if self.cbbaction.currentIndex() != 3 and len(_attriblist) < 1:
            vis_msg.print("ERROR in EditDataProperty: No property selected for editing", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Edit Property',
                                           'No property selected for editing')
            return
        #
        if self.cbbaction.currentIndex() == 0:
            self.dataproperty[_attriblist[0].text()+'_copy'] = self.dataproperty[_attriblist[0].text()].copy()
        if self.cbbaction.currentIndex() == 1:
            if len(self.ldtrename.text()) < 1:
                vis_msg.print("ERROR in EditDataProperty: No name specified for rename", type='error')
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Edit Property',
                                               'No name specified for rename')
                return
            if self.ldtrename.text() in self.dataproperty.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Edit Property',
                                                       self.ldtrename.text() + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.No:
                    return
            self.dataproperty[self.ldtrename.text()] = self.dataproperty[_attriblist[0].text()]
            self.dataproperty.pop(_attriblist[0].text())
        if self.cbbaction.currentIndex() == 2:
            for _i in range(len(_attriblist)):
                self.dataproperty.pop(_attriblist[_i].text())
        if self.cbbaction.currentIndex() == 3:
            _rtrvprop = QtWidgets.QDialog()
            _gui = gui_retrievepropertyfromseis()
            _gui.pointsetdata = self.dataproperty.copy()
            _gui.rootpath = self.rootpath
            _gui.setupGUI(_rtrvprop)
            _rtrvprop.exec()
            self.dataproperty = _gui.pointsetdata.copy()
            _rtrvprop.show()
        if self.cbbaction.currentIndex() == 4:
            _math = QtWidgets.QDialog()
            _gui = gui_calculator()
            _gui.data = self.dataproperty[_attriblist[0].text()].copy()
            _gui.setupGUI(_math)
            _math.exec()
            self.dataproperty[_attriblist[0].text()] = _gui.data.copy()
            _math.show()
        #
        self.refreshLwgAttrib()
        #
        # QtWidgets.QMessageBox.information(self.msgbox,
        #                                   "Edit Property",
        #                                   "Property edited successfully")
        return


    def refreshLwgAttrib(self):
        self.lwgattrib.clear()
        if self.checkSeisPointSet() is True:
            for i in sorted(self.dataproperty.keys()):
                if i != "Inline" and i != "Crossline" and i != "Z":
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(i)
                    self.lwgattrib.addItem(item)
            if "Inline" in self.dataproperty.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText("Inline")
                self.lwgattrib.addItem(item)
            if "Crossline" in self.dataproperty.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText("Crossline")
                self.lwgattrib.addItem(item)
            if "Z" in self.dataproperty.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText("Z")
                self.lwgattrib.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSeisPointSet(self):
        return point_ays.checkPointSet(self.dataproperty)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditDataProperty = QtWidgets.QWidget()
    gui = editdataproperty()
    gui.setupGUI(EditDataProperty)
    EditDataProperty.show()
    sys.exit(app.exec_())