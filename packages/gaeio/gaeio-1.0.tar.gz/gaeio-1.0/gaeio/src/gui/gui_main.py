#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# Create a GUI for mainwindow

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os
import sys
import shutil
import webbrowser
import vispy.io as vispy_io
from vispy import scene
from vispy.color import Colormap
import matplotlib.colors as mplt_color
from functools import partial
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
#
from gaeio.src.basic.data import data as basic_data
from gaeio.src.basic.matdict import matdict as basic_mdt
#
from gaeio.src.seismic.analysis import analysis as seis_ays
from gaeio.src.psseismic.analysis import analysis as psseis_ays
from gaeio.src.horizon.analysis import analysis as horizon_ays
from gaeio.src.pointset.analysis import analysis as point_ays
from gaeio.src.core.settings import settings as core_set
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.vis.colormap import colormap as vis_cmap
#
from gaeio.src.gui.importsurveymanual import importsurveymanual as gui_importsurveymanual
from gaeio.src.gui.importsurveysegy import importsurveysegy as gui_importsurveysegy
from gaeio.src.gui.importseissegy import importseissegy as gui_importseissegy
from gaeio.src.gui.importseisimageset import importseisimageset as gui_importseisimageset
from gaeio.src.gui.importpsseissegy import importpsseissegy as gui_importpsseissegy
from gaeio.src.gui.importpsseisimageset import importpsseisimageset as gui_importpsseisimageset
from gaeio.src.gui.importhorizonfile import importhorizonfile as gui_importhorizonfile
from gaeio.src.gui.importpointsetfile import importpointsetfile as gui_importpointsetfile
from gaeio.src.gui.exportsurvey import exportsurvey as gui_exportsurvey
from gaeio.src.gui.exportseissegy import exportseissegy as gui_exportseissegy
from gaeio.src.gui.exportseisnpy import exportseisnpy as gui_exportseisnpy
from gaeio.src.gui.exportseisimageset import exportseisimageset as gui_exportseisimageset
from gaeio.src.gui.exportpsseisnpy import exportpsseisnpy as gui_exportpsseisnpy
from gaeio.src.gui.exporthorizonfile import exporthorizonfile as gui_exporthorizonfile
from gaeio.src.gui.exporthorizonnpy import exporthorizonnpy as gui_exporthorizonnpy
from gaeio.src.gui.exportpointsetfile import exportpointsetfile as gui_exportpointsetfile
from gaeio.src.gui.exportpointsetnpy import exportpointsetnpy as gui_exportpointsetnpy
#
from gaeio.src.gui.managesurvey import managesurvey as gui_managesurvey
from gaeio.src.gui.manageseis import manageseis as gui_manageseis
from gaeio.src.gui.managepsseis import managepsseis as gui_managepsseis
from gaeio.src.gui.managehorizon import managehorizon as gui_managehorizon
from gaeio.src.gui.managepointset import managepointset as gui_managepointset
#
from gaeio.src.gui.convertseis2psseis import convertseis2psseis as gui_convertseis2psseis
from gaeio.src.gui.convertseis2pointset import convertseis2pointset as gui_convertseis2pointset
from gaeio.src.gui.convertpsseis2seis import convertpsseis2seis as gui_convertpsseis2seis
from gaeio.src.gui.converthorizon2pointset import converthorizon2pointset as gui_converthorizon2pointset
from gaeio.src.gui.convertpointset2seis import convertpointset2seis as gui_convertpointset2seis
from gaeio.src.gui.convertpointset2horizon import convertpointset2horizon as gui_convertpointset2horizon
#
from gaeio.src.gui.calcmathattribsingle import calcmathattribsingle as gui_calcmathattribsingle
from gaeio.src.gui.calcmathattribmultiple import calcmathattribmultiple as gui_calcmathattribmultiple
from gaeio.src.gui.calcinstanattrib import calcinstanattrib as gui_calcinstanattrib
#
from gaeio.src.gui.configseisvis import configseisvis as gui_configseisvis
from gaeio.src.gui.confighorizonvis import confighorizonvis as gui_confighorizonvis
from gaeio.src.gui.configpointsetvis import configpointsetvis as gui_configpointsetvis
from gaeio.src.gui.plotvis1dseisz import plotvis1dseisz as gui_plotvis1dseisz
from gaeio.src.gui.plotvis1dseisfreq import plotvis1dseisfreq as gui_plotvis1dseisfreq
from gaeio.src.gui.plotvis2dseisinl import plotvis2dseisinl as gui_plotvis2dseisinl
from gaeio.src.gui.plotvis2dseisxl import plotvis2dseisxl as gui_plotvis2dseisxl
from gaeio.src.gui.plotvis2dseisz import plotvis2dseisz as gui_plotvis2dseisz
from gaeio.src.gui.plotvis2dpsseisshot import plotvis2dpsseisshot as gui_plotvis2dpsseisshot
from gaeio.src.gui.plotvis2dpointsetcrossplt import plotvis2dpointsetcrossplt as gui_plotvis2dpointsetcrossplt
from gaeio.src.gui.plotvis3dseisinlxlz import plotvis3dseisinlxlz as gui_plotvis3dseisinlxlz
#
from gaeio.src.gui.settingsgui import settingsgui as gui_settingsgui
from gaeio.src.gui.settingsgeneral import settingsgeneral as gui_settingsgeneral
from gaeio.src.gui.settingsvisual import settingsvisual as gui_settingsvisual
from gaeio.src.gui.settingsviewer import settingsviewer as gui_settingsviewer
#
from gaeio.src.gui.about import about as gui_about

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


__all__ = ['start']


class mainwindow(object):

    projname = 'New project'
    projpath = ''
    survinfo = {}
    seisdata = {}
    psseisdata = {}
    horizondata = {}
    faultpatchdata = {}
    pointsetdata = {}
    welllogdata = {}
    #
    settings = core_set.Settings
    #
    canvas = None
    view = None
    canvasproperties = {}
    canvascomponents = {}
    seisvisconfig = {}
    horizonvisconfig = {}
    pointsetvisconfig = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1440, 960)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/logo.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 30))
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.toolbarleft = QtWidgets.QToolBar(MainWindow)
        self.toolbarleft.setObjectName("toolbarleft")
        self.toolbarleft.setGeometry(QtCore.QRect(0, 50, 40, 880))
        self.toolbarright = QtWidgets.QToolBar(MainWindow)
        self.toolbarright.setObjectName("toolbarright")
        self.toolbarright.setGeometry(QtCore.QRect(1400, 50, 40, 880))
        self.toolbartop = QtWidgets.QToolBar(MainWindow)
        self.toolbartop.setObjectName("toolbartop")
        self.toolbartop.setGeometry(QtCore.QRect(0, 20, 1440, 30))
        self.toolbarbottom = QtWidgets.QToolBar(MainWindow)
        self.toolbarbottom.setObjectName("toolbarbottom")
        self.toolbarbottom.setGeometry(QtCore.QRect(0, 930, 1440, 30))
        #
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menumanage = QtWidgets.QMenu(self.menubar)
        self.menumanage.setObjectName("menumanage")
        self.menutool = QtWidgets.QMenu(self.menubar)
        self.menutool.setObjectName("menutool")
        self.menuvis = QtWidgets.QMenu(self.menubar)
        self.menuvis.setObjectName("menuvis")
        self.menuutil = QtWidgets.QMenu(self.menubar)
        self.menuutil.setObjectName("menuutil")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        #
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        #
        # -------------------- File menu ----------------------------
        # project
        self.actionnewproject = QtWidgets.QAction(MainWindow)
        self.actionnewproject.setObjectName("actionnewproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/new.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionnewproject.setIcon(icon)
        self.actionopenproject = QtWidgets.QAction(MainWindow)
        self.actionopenproject.setObjectName("actionopenproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/folder.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionopenproject.setIcon(icon)
        self.actionsaveproject = QtWidgets.QAction(MainWindow)
        self.actionsaveproject.setObjectName("actionsaveproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/disk.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsaveproject.setIcon(icon)
        self.actionsaveasproject = QtWidgets.QAction(MainWindow)
        self.actionsaveasproject.setObjectName("actionsaveasproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/diskwithpen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsaveasproject.setIcon(icon)
        # import & export
        # . import
        self.menuimport = QtWidgets.QMenu(self.menufile)
        self.menuimport.setObjectName("menuimport")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/import.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimport.setIcon(icon)
        # .. survey
        self.menuimportsurvey = QtWidgets.QMenu(self.menuimport)
        self.menuimportsurvey.setObjectName("menuimportsurvey")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportsurvey.setIcon(icon)
        self.actionimportsurveymanual = QtWidgets.QAction(MainWindow)
        self.actionimportsurveymanual.setObjectName("actionimportsurveymanual")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/supervised.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportsurveymanual.setIcon(icon)
        self.actionimportsurveysegy = QtWidgets.QAction(MainWindow)
        self.actionimportsurveysegy.setObjectName("actionimportsurveysegy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportsurveysegy.setIcon(icon)
        self.actionimportsurveynpy = QtWidgets.QAction(MainWindow)
        self.actionimportsurveynpy.setObjectName("actionimportsurveynpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportsurveynpy.setIcon(icon)
        # .. seismic
        self.menuimportseis = QtWidgets.QMenu(self.menuimport)
        self.menuimportseis.setObjectName("menuimportseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportseis.setIcon(icon)
        self.actionimportseissegy = QtWidgets.QAction(MainWindow)
        self.actionimportseissegy.setObjectName("actionimportseissegy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseissegy.setIcon(icon)
        self.menuimportseisnpy = QtWidgets.QMenu(self.menuimport)
        self.menuimportseisnpy.setObjectName("menuimportseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportseisnpy.setIcon(icon)
        self.actionimportseisnpydictall = QtWidgets.QAction(MainWindow)
        self.actionimportseisnpydictall.setObjectName("actionimportseisnpydictall")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseisnpydictall.setIcon(icon)
        self.actionimportseisnpydictone = QtWidgets.QAction(MainWindow)
        self.actionimportseisnpydictone.setObjectName("actionimportseisnpydictone")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseisnpydictone.setIcon(icon)
        self.actionimportseisnpymat = QtWidgets.QAction(MainWindow)
        self.actionimportseisnpymat.setObjectName("actionimportseisnpymat")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/matrix.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseisnpymat.setIcon(icon)
        self.actionimportseisimageset = QtWidgets.QAction(MainWindow)
        self.actionimportseisimageset.setObjectName("actionimportseisimageset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseisimageset.setIcon(icon)
        # .. pre-stack seismic
        self.menuimportpsseis = QtWidgets.QMenu(self.menuimport)
        self.menuimportpsseis.setObjectName("menuimportpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportpsseis.setIcon(icon)
        self.actionimportpsseissegy = QtWidgets.QAction(MainWindow)
        self.actionimportpsseissegy.setObjectName("actionimportpsseissegy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpsseissegy.setIcon(icon)
        self.menuimportpsseisnpy = QtWidgets.QMenu(self.menuimport)
        self.menuimportpsseisnpy.setObjectName("menuimportpsseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportpsseisnpy.setIcon(icon)
        self.actionimportpsseisnpydictall = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisnpydictall.setObjectName("actionimportpsseisnpydictall")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpsseisnpydictall.setIcon(icon)
        self.actionimportpsseisnpydictone = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisnpydictone.setObjectName("actionimportpsseisnpydictone")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpsseisnpydictone.setIcon(icon)
        self.actionimportpsseisnpymat = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisnpymat.setObjectName("actionimportpsseisnpymat")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/matrix.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpsseisnpymat.setIcon(icon)
        self.actionimportpsseisimageset = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisimageset.setObjectName("actionimportpsseisimageset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpsseisimageset.setIcon(icon)
        # .. horizon
        self.menuimporthorizon = QtWidgets.QMenu(self.menuimport)
        self.menuimporthorizon.setObjectName("menuimporthorizon")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimporthorizon.setIcon(icon)
        self.actionimporthorizonfile = QtWidgets.QAction(MainWindow)
        self.actionimporthorizonfile.setObjectName("actionimporthorizonfile")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimporthorizonfile.setIcon(icon)
        self.menuimporthorizonnpy = QtWidgets.QMenu(self.menuimport)
        self.menuimporthorizonnpy.setObjectName("menuimporthorizonnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimporthorizonnpy.setIcon(icon)
        self.actionimporthorizonnpydictall = QtWidgets.QAction(MainWindow)
        self.actionimporthorizonnpydictall.setObjectName("actionimporthorizonnpydictall")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimporthorizonnpydictall.setIcon(icon)
        self.actionimporthorizonnpydictone = QtWidgets.QAction(MainWindow)
        self.actionimporthorizonnpydictone.setObjectName("actionimporthorizonnpydictone")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimporthorizonnpydictone.setIcon(icon)
        self.actionimporthorizonnpymat = QtWidgets.QAction(MainWindow)
        self.actionimporthorizonnpymat.setObjectName("actionimporthorizonnpymat")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/matrix.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimporthorizonnpymat.setIcon(icon)
        # .. pointset
        self.menuimportpointset = QtWidgets.QMenu(self.menuimport)
        self.menuimportpointset.setObjectName("menuimportpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportpointset.setIcon(icon)
        self.actionimportpointsetfile = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetfile.setObjectName("actionimportpointsetfile")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpointsetfile.setIcon(icon)
        self.menuimportpointsetnpy = QtWidgets.QMenu(self.menuimport)
        self.menuimportpointsetnpy.setObjectName("menuimportpointsetnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportpointsetnpy.setIcon(icon)
        self.actionimportpointsetnpydictall = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetnpydictall.setObjectName("actionimportpointsetnpydictall")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpointsetnpydictall.setIcon(icon)
        self.actionimportpointsetnpydictone = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetnpydictone.setObjectName("actionimportpointsetnpydictone")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pydict.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpointsetnpydictone.setIcon(icon)
        self.actionimportpointsetnpymat = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetnpymat.setObjectName("actionimportpointsetnpymat")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/matrix.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpointsetnpymat.setIcon(icon)
        # .export
        self.menuexport = QtWidgets.QMenu(self.menufile)
        self.menuexport.setObjectName("menuexport")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/export.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexport.setIcon(icon)
        # .. survey
        self.actionexportsurvey = QtWidgets.QAction(MainWindow)
        self.actionexportsurvey.setObjectName("actionexportsurvey")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportsurvey.setIcon(icon)
        # .. seismic
        self.menuexportseis = QtWidgets.QMenu(self.menuexport)
        self.menuexportseis.setObjectName("menuexportseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexportseis.setIcon(icon)
        self.actionexportseissegy = QtWidgets.QAction(MainWindow)
        self.actionexportseissegy.setObjectName("actionexportseissegy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportseissegy.setIcon(icon)
        self.actionexportseisnpy = QtWidgets.QAction(MainWindow)
        self.actionexportseisnpy.setObjectName("actionexportseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportseisnpy.setIcon(icon)
        self.actionexportseisimageset = QtWidgets.QAction(MainWindow)
        self.actionexportseisimageset.setObjectName("actionexportseisimageset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportseisimageset.setIcon(icon)
        # .. pre-stack seismic
        self.menuexportpsseis = QtWidgets.QMenu(self.menuexport)
        self.menuexportpsseis.setObjectName("menuexportpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexportpsseis.setIcon(icon)
        self.actionexportpsseisnpy = QtWidgets.QAction(MainWindow)
        self.actionexportpsseisnpy.setObjectName("actionexportpsseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportpsseisnpy.setIcon(icon)
        # .. horizon
        self.menuexporthorizon = QtWidgets.QMenu(self.menuimport)
        self.menuexporthorizon.setObjectName("menuexporthorizon")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexporthorizon.setIcon(icon)
        self.actionexporthorizonfile = QtWidgets.QAction(MainWindow)
        self.actionexporthorizonfile.setObjectName("actionexporthorizonfile")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexporthorizonfile.setIcon(icon)
        self.actionexporthorizonnpy = QtWidgets.QAction(MainWindow)
        self.actionexporthorizonnpy.setObjectName("actionexporthorizonnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexporthorizonnpy.setIcon(icon)
        # .. pointset
        self.menuexportpointset = QtWidgets.QMenu(self.menuimport)
        self.menuexportpointset.setObjectName("menuexportpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexportpointset.setIcon(icon)
        self.actionexportpointsetfile = QtWidgets.QAction(MainWindow)
        self.actionexportpointsetfile.setObjectName("actionexportpointsetfile")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportpointsetfile.setIcon(icon)
        self.actionexportpointsetnpy = QtWidgets.QAction(MainWindow)
        self.actionexportpointsetnpy.setObjectName("actionexportpointsetnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportpointsetnpy.setIcon(icon)
        # quit
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName("actionquit")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/close.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionquit.setIcon(icon)
        # -------------- end of File menu ----------------------
        #
        # -------------- Manage menu ----------------------------
        # Survey
        self.actionmanagesurvey = QtWidgets.QAction(MainWindow)
        self.actionmanagesurvey.setObjectName("actionmanagesurvey")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagesurvey.setIcon(icon)
        # Seismic & pre-stack seismic
        # . seismic
        self.actionmanageseis = QtWidgets.QAction(MainWindow)
        self.actionmanageseis.setObjectName("actionmanageseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanageseis.setIcon(icon)
        # . pre-stack seismic
        self.actionmanagepsseis = QtWidgets.QAction(MainWindow)
        self.actionmanagepsseis.setObjectName("actionmanagepsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagepsseis.setIcon(icon)
        # Horizon
        self.actionmanagehorizon = QtWidgets.QAction(MainWindow)
        self.actionmanagehorizon.setObjectName("actionmanagehorizon")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagehorizon.setIcon(icon)
        # PointSet
        self.actionmanagepointset = QtWidgets.QAction(MainWindow)
        self.actionmanagepointset.setObjectName("actionmanagepointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagepointset.setIcon(icon)
        # ----------------- End of Manage menu ------------------------------
        #
        # ----------------- ToolBox menu -----------------------------------
        # Data conversion
        self.menudataconversion = QtWidgets.QMenu(self.menutool)
        self.menudataconversion.setObjectName("menudataconversion")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/exchange.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menudataconversion.setIcon(icon)
        # . seismic
        self.menuconvertseis = QtWidgets.QMenu(self.menudataconversion)
        self.menuconvertseis.setObjectName("menuconvertseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuconvertseis.setIcon(icon)
        self.actionconvertseis2psseis = QtWidgets.QAction(MainWindow)
        self.actionconvertseis2psseis.setObjectName("actionconvertseis2psseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertseis2psseis.setIcon(icon)
        self.actionconvertseis2pointset = QtWidgets.QAction(MainWindow)
        self.actionconvertseis2pointset.setObjectName("actionconvertseis2pointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertseis2pointset.setIcon(icon)
        # . pre-stack seismic
        self.menuconvertpsseis = QtWidgets.QMenu(self.menudataconversion)
        self.menuconvertpsseis.setObjectName("menuconvertpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuconvertpsseis.setIcon(icon)
        self.actionconvertpsseis2seis = QtWidgets.QAction(MainWindow)
        self.actionconvertpsseis2seis.setObjectName("actionconvertpsseis2seis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertpsseis2seis.setIcon(icon)
        # . horizon
        self.menuconverthorizon = QtWidgets.QMenu(self.menudataconversion)
        self.menuconverthorizon.setObjectName("menuconverthorizon")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuconverthorizon.setIcon(icon)
        self.actionconverthorizon2pointset = QtWidgets.QAction(MainWindow)
        self.actionconverthorizon2pointset.setObjectName("actionconverthorizon2pointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconverthorizon2pointset.setIcon(icon)
        # . pointset
        self.menuconvertpointset = QtWidgets.QMenu(self.menudataconversion)
        self.menuconvertpointset.setObjectName("menuconvertpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuconvertpointset.setIcon(icon)
        self.actionconvertpointset2seis = QtWidgets.QAction(MainWindow)
        self.actionconvertpointset2seis.setObjectName("actionconvertpointset2seis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertpointset2seis.setIcon(icon)
        self.actionconvertpointset2horizon = QtWidgets.QAction(MainWindow)
        self.actionconvertpointset2horizon.setObjectName("actionconvertpointset2horizon")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertpointset2horizon.setIcon(icon)
        # Seismic attribute engine
        self.menuattribengine = QtWidgets.QMenu(self.menutool)
        self.menuattribengine.setObjectName("menuattribengine")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/attribute.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuattribengine.setIcon(icon)
        # . mathematics
        self.menumathattrib = QtWidgets.QMenu(self.menuattribengine)
        self.menumathattrib.setObjectName("menumathattrib")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/math.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menumathattrib.setIcon(icon)
        # .. single
        self.actioncalcmathattribsingle = QtWidgets.QAction(MainWindow)
        self.actioncalcmathattribsingle.setObjectName("actioncalcmathattribsingle")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/file.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actioncalcmathattribsingle.setIcon(icon)
        # .. multiple
        self.actioncalcmathattribmultiple = QtWidgets.QAction(MainWindow)
        self.actioncalcmathattribmultiple.setObjectName("actioncalcmathattribmultiple")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actioncalcmathattribmultiple.setIcon(icon)
        # . instantaneous
        self.actioncalcinstanattrib = QtWidgets.QAction(MainWindow)
        self.actioncalcinstanattrib.setObjectName("actioncalcinstanattrib")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/hilbert.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actioncalcinstanattrib.setIcon(icon)
        # ------------------ End of Toolbox menu -----------------------------
        #
        # ------------------ Visualization menu ------------------------------
        # 1D
        self.menu1dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu1dwindow.setObjectName("menu1dwindow")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/vis1d.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu1dwindow.setIcon(icon)
        # . seismic
        self.menu1dwindowseis = QtWidgets.QMenu(self.menu1dwindow)
        self.menu1dwindowseis.setObjectName("menu1dwindowseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu1dwindowseis.setIcon(icon)
        self.actionplotvis1dseisz = QtWidgets.QAction(MainWindow)
        self.actionplotvis1dseisz.setObjectName("actionplotvis1dseisz")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/waveform.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis1dseisz.setIcon(icon)
        self.actionplotvis1dseisfreq = QtWidgets.QAction(MainWindow)
        self.actionplotvis1dseisfreq.setObjectName("actionplotvis1dseisfreq")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotcurve.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis1dseisfreq.setIcon(icon)
        # 2D
        self.menu2dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu2dwindow.setObjectName("menu2dwindow")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/vis2d.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindow.setIcon(icon)
        # . seismic
        self.menu2dwindowseis = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowseis.setObjectName("menu2dwindowseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindowseis.setIcon(icon)
        self.actionplotvis2dseisinl = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dseisinl.setObjectName("actionplotvis2dseisinl")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/visinl.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis2dseisinl.setIcon(icon)
        self.actionplotvis2dseisxl = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dseisxl.setObjectName("actionplotvis2dseisxl")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/visxl.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis2dseisxl.setIcon(icon)
        self.actionplotvis2dseisz = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dseisz.setObjectName("actionplotvis2dseisz")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/visz.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis2dseisz.setIcon(icon)
        # . pre-stack seismic
        self.menu2dwindowpsseis = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowpsseis.setObjectName("menu2dwindowpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindowpsseis.setIcon(icon)
        self.actionplotvis2dpsseisshot = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dpsseisshot.setObjectName("actionplotvis2dpsseisshot")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/gather.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis2dpsseisshot.setIcon(icon)
        # . pointset
        self.menu2dwindowpointset = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowpointset.setObjectName("menu2dwindowpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindowpointset.setIcon(icon)
        self.actionplotvis2dpointsetcrossplt = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dpointsetcrossplt.setObjectName("actionplotvis2dpointsetcrossplt")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotpoint.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis2dpointsetcrossplt.setIcon(icon)
        # 3D
        self.menu3dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu3dwindow.setObjectName("menu3dwindow")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/vis3d.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu3dwindow.setIcon(icon)
        # . seismic
        self.menu3dwindowseis = QtWidgets.QMenu(self.menu3dwindow)
        self.menu3dwindowseis.setObjectName("menu3dwindowseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu3dwindowseis.setIcon(icon)
        self.actionplotvis3dseisinlxlz = QtWidgets.QAction(MainWindow)
        self.actionplotvis3dseisinlxlz.setObjectName("actionplotvis3dseisinlxlz")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/box.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplotvis3dseisinlxlz.setIcon(icon)
        # ------------------------- End of Visualization menu -------------------------
        #
        # --------------------- Utilities menu ----------------------------
        # Settings
        self.menusettings = QtWidgets.QMenu(self.menuutil)
        self.menusettings.setObjectName("menusettings")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menusettings.setIcon(icon)
        self.actionsettingsgui = QtWidgets.QAction(MainWindow)
        self.actionsettingsgui.setObjectName("actionsettingsgui")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/logo.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsgui.setIcon(icon)
        self.actionsettingsgeneral = QtWidgets.QAction(MainWindow)
        self.actionsettingsgeneral.setObjectName("actionsettingsgeneral")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsgeneral.setIcon(icon)
        self.actionsettingsvisual = QtWidgets.QAction(MainWindow)
        self.actionsettingsvisual.setObjectName("actionsettingsvisual")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsvisual.setIcon(icon)
        self.actionsettingsviewer = QtWidgets.QAction(MainWindow)
        self.actionsettingsviewer.setObjectName("actionsettingsviewer")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/dice.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsviewer.setIcon(icon)
        # ----------------------- End of Utilities menu --------------------------
        #
        # --------------------- Help menu -------------------------------
        # Menu & online support
        self.actionmanual = QtWidgets.QAction(MainWindow)
        self.actionmanual.setObjectName("actionmanual")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/manual.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanual.setIcon(icon)
        self.actionsupport = QtWidgets.QAction(MainWindow)
        self.actionsupport.setObjectName("actionsupport")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/support.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsupport.setIcon(icon)
        # About
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName("actionabout")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/about.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionabout.setIcon(icon)
        # -------------------- End of Help menu -------------------------------
        #
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menumanage.menuAction())
        self.menubar.addAction(self.menutool.menuAction())
        self.menubar.addAction(self.menuvis.menuAction())
        self.menubar.addAction(self.menuutil.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())
        #
        # ------------------- File menu ----------------------------------
        # Projects
        self.menufile.addAction(self.actionnewproject)
        self.menufile.addAction(self.actionopenproject)
        self.menufile.addAction(self.actionsaveproject)
        self.menufile.addAction(self.actionsaveasproject)
        # Import & export
        # . import
        self.menufile.addSeparator()
        self.menufile.addAction(self.menuimport.menuAction())
        # .. survey
        self.menuimport.addAction(self.menuimportsurvey.menuAction())
        self.menuimportsurvey.addAction(self.actionimportsurveymanual)
        self.menuimportsurvey.addAction(self.actionimportsurveysegy)
        self.menuimportsurvey.addAction(self.actionimportsurveynpy)
        # .. seismic
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.menuimportseis.menuAction())
        self.menuimportseis.addAction(self.actionimportseissegy)
        self.menuimportseis.addAction(self.menuimportseisnpy.menuAction())
        self.menuimportseisnpy.addAction(self.actionimportseisnpydictall)
        self.menuimportseisnpy.addAction(self.actionimportseisnpydictone)
        self.menuimportseisnpy.addAction(self.actionimportseisnpymat)
        self.menuimportseis.addAction(self.actionimportseisimageset)
        # .. pre-stack seismic
        self.menuimport.addAction(self.menuimportpsseis.menuAction())
        self.menuimportpsseis.addAction(self.actionimportpsseissegy)
        self.menuimportpsseis.addAction(self.menuimportpsseisnpy.menuAction())
        self.menuimportpsseisnpy.addAction(self.actionimportpsseisnpydictall)
        self.menuimportpsseisnpy.addAction(self.actionimportpsseisnpydictone)
        self.menuimportpsseisnpy.addAction(self.actionimportpsseisnpymat)
        self.menuimportpsseis.addAction(self.actionimportpsseisimageset)
        # .. horizon
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.menuimporthorizon.menuAction())
        self.menuimporthorizon.addAction(self.actionimporthorizonfile)
        self.menuimporthorizon.addAction(self.menuimporthorizonnpy.menuAction())
        self.menuimporthorizonnpy.addAction(self.actionimporthorizonnpydictall)
        self.menuimporthorizonnpy.addAction(self.actionimporthorizonnpydictone)
        self.menuimporthorizonnpy.addAction(self.actionimporthorizonnpymat)
        # .. pointset
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.menuimportpointset.menuAction())
        self.menuimportpointset.addAction(self.actionimportpointsetfile)
        self.menuimportpointset.addAction(self.menuimportpointsetnpy.menuAction())
        self.menuimportpointsetnpy.addAction(self.actionimportpointsetnpydictall)
        self.menuimportpointsetnpy.addAction(self.actionimportpointsetnpydictone)
        self.menuimportpointsetnpy.addAction(self.actionimportpointsetnpymat)
        # . export
        self.menufile.addAction(self.menuexport.menuAction())
        # .. survey
        self.menuexport.addAction(self.actionexportsurvey)
        # .. seismic
        self.menuexport.addSeparator()
        self.menuexport.addAction(self.menuexportseis.menuAction())
        self.menuexportseis.addAction(self.actionexportseissegy)
        self.menuexportseis.addAction(self.actionexportseisnpy)
        self.menuexportseis.addAction(self.actionexportseisimageset)
        self.menuexport.addAction(self.menuexportpsseis.menuAction())
        self.menuexportpsseis.addAction(self.actionexportpsseisnpy)
        # .. horizon
        self.menuexport.addSeparator()
        self.menuexport.addAction(self.menuexporthorizon.menuAction())
        self.menuexporthorizon.addAction(self.actionexporthorizonfile)
        self.menuexporthorizon.addAction(self.actionexporthorizonnpy)
        # .. pointset
        self.menuexport.addSeparator()
        self.menuexport.addAction(self.menuexportpointset.menuAction())
        self.menuexportpointset.addAction(self.actionexportpointsetfile)
        self.menuexportpointset.addAction(self.actionexportpointsetnpy)
        # Quit
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionquit)
        # --------------------- End of File menu --------------------------------
        #
        # -------------------- Manage menu --------------------------
        # Survey
        self.menumanage.addAction(self.actionmanagesurvey)
        # Seismic and pre-stack seismic
        self.menumanage.addSeparator()
        self.menumanage.addAction(self.actionmanageseis)
        self.menumanage.addAction(self.actionmanagepsseis)
        # Horizon
        self.menumanage.addSeparator()
        self.menumanage.addAction(self.actionmanagehorizon)
        # PointSet
        self.menumanage.addSeparator()
        self.menumanage.addAction(self.actionmanagepointset)
        # ------------------ End of Manage menu ----------------------
        #
        # ------------------ Toolbox menu ----------------------------
        # Data conversion
        self.menutool.addAction(self.menudataconversion.menuAction())
        # . seismic
        self.menudataconversion.addAction(self.menuconvertseis.menuAction())
        self.menuconvertseis.addAction(self.actionconvertseis2psseis)
        self.menuconvertseis.addAction(self.actionconvertseis2pointset)
        # . pre-stack seismic
        self.menudataconversion.addAction(self.menuconvertpsseis.menuAction())
        self.menuconvertpsseis.addAction(self.actionconvertpsseis2seis)
        # . horizon
        self.menudataconversion.addSeparator()
        self.menudataconversion.addAction(self.menuconverthorizon.menuAction())
        self.menuconverthorizon.addAction(self.actionconverthorizon2pointset)
        # . pointset
        self.menudataconversion.addSeparator()
        self.menudataconversion.addAction(self.menuconvertpointset.menuAction())
        self.menuconvertpointset.addAction(self.actionconvertpointset2seis)
        self.menuconvertpointset.addAction(self.actionconvertpointset2horizon)
        # seismic attribute engine
        self.menutool.addSeparator()
        self.menutool.addAction(self.menuattribengine.menuAction())
        # . mathematics
        self.menuattribengine.addAction(self.menumathattrib.menuAction())
        self.menumathattrib.addAction(self.actioncalcmathattribsingle)
        self.menumathattrib.addAction(self.actioncalcmathattribmultiple)
        # . instantaneous
        self.menuattribengine.addAction(self.actioncalcinstanattrib)
        # -------------------------- End of Tool menu ------------------
        #
        # ---------------------- Visualization menu --------------------
        # 1D
        self.menuvis.addAction(self.menu1dwindow.menuAction())
        # . seismic
        self.menu1dwindow.addAction(self.menu1dwindowseis.menuAction())
        self.menu1dwindowseis.addAction(self.actionplotvis1dseisz)
        self.menu1dwindowseis.addAction(self.actionplotvis1dseisfreq)
        # 2D
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu2dwindow.menuAction())
        # . seismic
        self.menu2dwindow.addAction(self.menu2dwindowseis.menuAction())
        self.menu2dwindowseis.addAction(self.actionplotvis2dseisinl)
        self.menu2dwindowseis.addAction(self.actionplotvis2dseisxl)
        self.menu2dwindowseis.addAction(self.actionplotvis2dseisz)
        # . pre-stack seismic
        self.menu2dwindow.addAction(self.menu2dwindowpsseis.menuAction())
        self.menu2dwindowpsseis.addAction(self.actionplotvis2dpsseisshot)
        # . pointset
        self.menu2dwindow.addSeparator()
        self.menu2dwindow.addAction(self.menu2dwindowpointset.menuAction())
        self.menu2dwindowpointset.addAction(self.actionplotvis2dpointsetcrossplt)
        # 3D
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu3dwindow.menuAction())
        # . seismic
        self.menu3dwindow.addAction(self.menu3dwindowseis.menuAction())
        self.menu3dwindowseis.addAction(self.actionplotvis3dseisinlxlz)
        # -------------------------- End of Visualization menu -----------------
        #
        # -------------------- Utilities menu ----------------------------
        # Settings
        self.menuutil.addAction(self.menusettings.menuAction())
        self.menusettings.addAction(self.actionsettingsgui)
        self.menusettings.addAction(self.actionsettingsgeneral)
        self.menusettings.addAction(self.actionsettingsvisual)
        self.menusettings.addAction(self.actionsettingsviewer)
        # ------------------- End of Utilities menu -----------------
        #
        # ----------------- Help menu ----------------
        # Manual and online support
        self.menuhelp.addAction(self.actionmanual)
        self.menuhelp.addAction(self.actionsupport)
        # About
        self.menuhelp.addSeparator()
        self.menuhelp.addAction(self.actionabout)
        # ------------------- End of Help menu -------------------------------
        #
        # ------------------------- Tool bar ------------------------
        # Left
        self.toolbarleft.setOrientation(QtCore.Qt.Vertical)
        self.toolbarleft.addAction(self.menuimport.menuAction())
        self.toolbarleft.addSeparator()
        self.toolbarleft.addAction(self.menuexport.menuAction())
        # Right
        self.toolbarright.setOrientation(QtCore.Qt.Vertical)
        self.toolbarright.addAction(self.menudataconversion.menuAction())
        self.toolbarright.addSeparator()
        self.toolbarright.addAction(self.menuattribengine.menuAction())
        # Top
        self.toolbartop.addAction(self.actionmanagesurvey)
        self.toolbartop.addSeparator()
        self.toolbartop.addAction(self.actionmanageseis)
        self.toolbartop.addAction(self.actionmanagepsseis)
        self.toolbartop.addAction(self.actionmanagehorizon)
        self.toolbartop.addAction(self.actionmanagepointset)
        # Bottom
        self.toolbarbottom.addAction(self.menu1dwindow.menuAction())
        self.toolbarbottom.addSeparator()
        self.toolbarbottom.addAction(self.menu2dwindow.menuAction())
        self.toolbarbottom.addSeparator()
        self.toolbarbottom.addAction(self.menu3dwindow.menuAction())
        # ---------------------- End of Tool bar -------------------------
        #
        self.msgbox = QtWidgets.QMessageBox(MainWindow)
        self.msgbox.setObjectName("msgbox")
        _center_x = MainWindow.geometry().center().x()
        _center_y = MainWindow.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x-150, _center_y-50, 300, 100))
        #
        # Background image
        # self.bkimage = QtWidgets.QLabel(MainWindow)
        # self.bkimage.setObjectName("bkimage")
        # self.bkimage.setGeometry(QtCore.QRect(100, 130, 700, 300))
        #
        # --------------------- main canvas ---------------------------------------
        # seismic
        self.lblseisicon = QtWidgets.QLabel(MainWindow)
        self.lblseisicon.setObjectName("lblseisicon")
        self.lblseisicon.setGeometry(QtCore.QRect(10, 60, 20, 20))
        self.lblseisicon.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")).
                                   scaled(20, 20, QtCore.Qt.KeepAspectRatio))
        self.lblseis = QtWidgets.QLabel(MainWindow)
        self.lblseis.setObjectName("lblseis")
        self.lblseis.setGeometry(QtCore.QRect(40, 60, 50, 20))
        # config seismic
        self.btnconfigseisvis = QtWidgets.QPushButton(MainWindow)
        self.btnconfigseisvis.setObjectName("btnconfigseisvis")
        self.btnconfigseisvis.setGeometry(QtCore.QRect(100, 60, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfigseisvis.setIcon(icon)
        # seismic list
        self.cbblistseis = QtWidgets.QComboBox(MainWindow)
        self.cbblistseis.setObjectName("cbblistseis")
        self.cbblistseis.setGeometry(QtCore.QRect(10, 85, 190, 20))
        # add to canvas
        self.btnaddseis2canvas = QtWidgets.QPushButton(MainWindow)
        self.btnaddseis2canvas.setObjectName("btnaddseis2canvas")
        self.btnaddseis2canvas.setGeometry(QtCore.QRect(210, 85, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/add.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnaddseis2canvas.setIcon(icon)
        # seismic on canvas
        self.twgseisoncanvas = QtWidgets.QTableWidget(MainWindow)
        self.twgseisoncanvas.setObjectName("twgseisoncanvas")
        self.twgseisoncanvas.setGeometry(QtCore.QRect(10, 110, 220, 300))
        self.twgseisoncanvas.setColumnCount(5)
        self.twgseisoncanvas.setRowCount(0)
        self.twgseisoncanvas.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgseisoncanvas.horizontalHeader().hide()
        self.twgseisoncanvas.verticalHeader().hide()
        self.twgseisoncanvas.setColumnWidth(0, 18)
        self.twgseisoncanvas.setColumnWidth(1, 102)
        self.twgseisoncanvas.setColumnWidth(2, 55)
        self.twgseisoncanvas.setColumnWidth(3, 60)
        self.twgseisoncanvas.setColumnWidth(4, 30)
        #
        # horizon
        self.lblhorizonicon = QtWidgets.QLabel(MainWindow)
        self.lblhorizonicon.setObjectName("lblhorizonicon")
        self.lblhorizonicon.setGeometry(QtCore.QRect(10, 430, 20, 20))
        self.lblhorizonicon.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/surface.png")).
                                       scaled(20, 20, QtCore.Qt.KeepAspectRatio))
        self.lblhorizon = QtWidgets.QLabel(MainWindow)
        self.lblhorizon.setObjectName("lblhorizon")
        self.lblhorizon.setGeometry(QtCore.QRect(40, 430, 50, 20))
        # config horizon
        self.btnconfighorizonvis = QtWidgets.QPushButton(MainWindow)
        self.btnconfighorizonvis.setObjectName("btnconfighorizonvis")
        self.btnconfighorizonvis.setGeometry(QtCore.QRect(100, 430, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfighorizonvis.setIcon(icon)
        # horizon list
        self.cbblisthorizon = QtWidgets.QComboBox(MainWindow)
        self.cbblisthorizon.setObjectName("cbblisthorizon")
        self.cbblisthorizon.setGeometry(QtCore.QRect(10, 455, 190, 20))
        # add to canvas
        self.btnaddhorizon2canvas = QtWidgets.QPushButton(MainWindow)
        self.btnaddhorizon2canvas.setObjectName("btnaddhorizon2canvas")
        self.btnaddhorizon2canvas.setGeometry(QtCore.QRect(210, 455, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/add.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnaddhorizon2canvas.setIcon(icon)
        # horizon on canvas
        self.twghorizononcanvas = QtWidgets.QTableWidget(MainWindow)
        self.twghorizononcanvas.setObjectName("twghorizononcanvas")
        self.twghorizononcanvas.setGeometry(QtCore.QRect(10, 480, 220, 150))
        self.twghorizononcanvas.setColumnCount(4)
        self.twghorizononcanvas.setRowCount(0)
        self.twghorizononcanvas.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twghorizononcanvas.horizontalHeader().hide()
        self.twghorizononcanvas.verticalHeader().hide()
        self.twghorizononcanvas.setColumnWidth(0, 18)
        self.twghorizononcanvas.setColumnWidth(1, 102)
        self.twghorizononcanvas.setColumnWidth(2, 70)
        self.twghorizononcanvas.setColumnWidth(3, 30)
        #
        # pointset
        self.lblpointseticon = QtWidgets.QLabel(MainWindow)
        self.lblpointseticon.setObjectName("lblpointseticon")
        self.lblpointseticon.setGeometry(QtCore.QRect(10, 650, 20, 20))
        self.lblpointseticon.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")).
                                       scaled(20, 20, QtCore.Qt.KeepAspectRatio))
        self.lblpointset = QtWidgets.QLabel(MainWindow)
        self.lblpointset.setObjectName("lblpointset")
        self.lblpointset.setGeometry(QtCore.QRect(40, 650, 50, 20))
        # config pointset
        self.btnconfigpointsetvis = QtWidgets.QPushButton(MainWindow)
        self.btnconfigpointsetvis.setObjectName("btnconfigpointsetvis")
        self.btnconfigpointsetvis.setGeometry(QtCore.QRect(100, 650, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfigpointsetvis.setIcon(icon)
        # pointset list
        self.cbblistpointset = QtWidgets.QComboBox(MainWindow)
        self.cbblistpointset.setObjectName("cbblistpointset")
        self.cbblistpointset.setGeometry(QtCore.QRect(10, 675, 190, 20))
        # add to canvas
        self.btnaddpointset2canvas = QtWidgets.QPushButton(MainWindow)
        self.btnaddpointset2canvas.setObjectName("btnaddpointset2canvas")
        self.btnaddpointset2canvas.setGeometry(QtCore.QRect(210, 675, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/add.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnaddpointset2canvas.setIcon(icon)
        # pointset on canvas
        self.twgpointsetoncanvas = QtWidgets.QTableWidget(MainWindow)
        self.twgpointsetoncanvas.setObjectName("twgpointsetoncanvas")
        self.twgpointsetoncanvas.setGeometry(QtCore.QRect(10, 700, 220, 150))
        self.twgpointsetoncanvas.setColumnCount(4)
        self.twgpointsetoncanvas.setRowCount(0)
        self.twgpointsetoncanvas.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgpointsetoncanvas.horizontalHeader().hide()
        self.twgpointsetoncanvas.verticalHeader().hide()
        self.twgpointsetoncanvas.setColumnWidth(0, 18)
        self.twgpointsetoncanvas.setColumnWidth(1, 102)
        self.twgpointsetoncanvas.setColumnWidth(2, 70)
        self.twgpointsetoncanvas.setColumnWidth(3, 30)
        #
        # main canvas
        self.wgtcanvas = QtWidgets.QWidget(MainWindow)
        self.wgtcanvas.setObjectName("wdtcanvas")
        self.wgtcanvas.setGeometry(QtCore.QRect(240, 90, 1120, 840))
        #
        # survey box
        self.btnsrvbox = QtWidgets.QPushButton(MainWindow)
        self.btnsrvbox.setObjectName("btnsrvbox")
        self.btnsrvbox.setGeometry(QtCore.QRect(1370, 90, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/box.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnsrvbox.setIcon(icon)
        #
        # xyz axis
        self.btnxyzaxis = QtWidgets.QPushButton(MainWindow)
        self.btnxyzaxis.setObjectName("btnxyzaxis")
        self.btnxyzaxis.setGeometry(QtCore.QRect(1370, 120, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/xyz.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnxyzaxis.setIcon(icon)
        #
        # snapshot
        self.btnsnapshot = QtWidgets.QPushButton(MainWindow)
        self.btnsnapshot.setObjectName("btnsnapshot")
        self.btnsnapshot.setGeometry(QtCore.QRect(1370, 150, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/camera.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnsnapshot.setIcon(icon)
        #
        # home
        self.btngohome = QtWidgets.QPushButton(MainWindow)
        self.btngohome.setObjectName("btngohome")
        self.btngohome.setGeometry(QtCore.QRect(240, 60, 20, 20))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/home.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btngohome.setIcon(icon)
        #
        # view angle
        self.cbbviewfrom = QtWidgets.QComboBox(MainWindow)
        self.cbbviewfrom.setObjectName("cbbviewfrom")
        self.cbbviewfrom.setGeometry(QtCore.QRect(270, 60, 90, 20))
        #
        # z scale
        self.ldtzscale = QtWidgets.QLineEdit(MainWindow)
        self.ldtzscale.setObjectName("ldtzscale")
        self.ldtzscale.setGeometry(QtCore.QRect(370, 60, 50, 20))
        self.ldtzscale.setAlignment(QtCore.Qt.AlignCenter)
        # ------------------------ end of canvas -------------------------------------------

        self.retranslateGUI(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateGUI(self, MainWindow):
        self.dialog = MainWindow
        #
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GAEIO"+" <"+self.projname+">"))
        self.menufile.setTitle(_translate("MainWindow", "&File"))
        self.menumanage.setTitle(_translate("MainWindow", "Manage"))
        self.menutool.setTitle(_translate("MainWindow", "Toolbox"))
        self.menuvis.setTitle(_translate("MainWindow", "Visualization"))
        self.menuutil.setTitle(_translate("MainWindow", "Utilities"))
        self.menuhelp.setTitle(_translate("MainWindow", "&Help"))
        #
        # ------------------------- File menu ------------------------
        # Project
        self.actionnewproject.setText(_translate("MainWindow", "New Project"))
        self.actionopenproject.setText(_translate("MainWindow", "Open Project"))
        self.actionsaveproject.setText(_translate("MainWindow", "Save Project"))
        self.actionsaveasproject.setText(_translate("MainWindow", "Save Project as"))
        # Import and export
        # . import
        self.menuimport.setTitle(_translate("MainWindow", "Import"))
        # .. survey
        self.menuimportsurvey.setTitle(_translate("MainWindow", "Survey"))
        self.actionimportsurveymanual.setText(_translate("MainWindow", "Create"))
        self.actionimportsurveysegy.setText(_translate("MainWindow", "SEG-Y"))
        self.actionimportsurveynpy.setText(_translate("MainWindow", "NumPy"))
        # .. seismic
        self.menuimportseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionimportseissegy.setText(_translate("MainWindow", "SEG-Y"))
        self.menuimportseisnpy.setTitle(_translate("MainWindow", "Numpy"))
        self.actionimportseisnpydictall.setText(_translate("MainWindow", "Dictionary (all in one)"))
        self.actionimportseisnpydictone.setText(_translate("MainWindow", "Dictionary (individual)"))
        self.actionimportseisnpymat.setText(_translate("MainWindow", "2/3D Matrix"))
        self.actionimportseisnpymat.setToolTip("Import Seismic from NumPy Matrix")
        self.actionimportseisimageset.setText(_translate("MainWindow", "ImageSet"))
        # .. pre-stack seismic
        self.menuimportpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionimportpsseissegy.setText(_translate("MainWindow", "SEG-Y"))
        self.menuimportpsseisnpy.setTitle(_translate("MainWindow", "NumPy"))
        self.actionimportpsseisnpydictall.setText(_translate("MainWindow", "Dictionary (all in one)"))
        self.actionimportpsseisnpydictone.setText(_translate("MainWindow", "Dictionary (individual)"))
        self.actionimportpsseisnpymat.setText(_translate("MainWindow", "2/3D Matrix"))
        self.actionimportpsseisimageset.setText(_translate("MainWindow", "ImageSet"))
        # .. horizon
        self.menuimporthorizon.setTitle(_translate("MainWindow", "Horizon"))
        self.actionimporthorizonfile.setText(_translate("MainWindow", "Ascii File"))
        self.menuimporthorizonnpy.setTitle(_translate("MainWindow", "Numpy"))
        self.actionimporthorizonnpydictall.setText(_translate("MainWindow", "Dictionary (all in one)"))
        self.actionimporthorizonnpydictone.setText(_translate("MainWindow", "Dictionary (individual)"))
        self.actionimporthorizonnpymat.setText(_translate("MainWindow", "2D Matrix"))
        # .. pointset
        self.menuimportpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionimportpointsetfile.setText(_translate("MainWindow", "Ascii File"))
        self.menuimportpointsetnpy.setTitle(_translate("MainWindow", "Numpy"))
        self.actionimportpointsetnpydictall.setText(_translate("MainWindow", "Dictionary (all in one)"))
        self.actionimportpointsetnpydictone.setText(_translate("MainWindow", "Dictionary (individual)"))
        self.actionimportpointsetnpymat.setText(_translate("MainWindow", "2D Matrix"))
        #  . export
        self.menuexport.setTitle(_translate("MainWindow", "Export"))
        # .. survey
        self.actionexportsurvey.setText(_translate("MainWindow", "Survey"))
        # .. seismic
        self.menuexportseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionexportseissegy.setText(_translate("MainWindow", "SEG-Y"))
        self.actionexportseisnpy.setText(_translate("MainWindow", "NumPy"))
        self.actionexportseisimageset.setText(_translate("MainWindow", "ImageSet"))
        # .. pre-stack seismic
        self.menuexportpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionexportpsseisnpy.setText(_translate("MainWindow", "NumPy"))
        # .. horizon
        self.menuexporthorizon.setTitle(_translate("MainWindow", "Horizon"))
        self.actionexporthorizonfile.setText(_translate("MainWindow", "Ascii File"))
        self.actionexporthorizonnpy.setText(_translate("MainWindow", "NumPy"))
        # .. pointset
        self.menuexportpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionexportpointsetfile.setText(_translate("MainWindow", "Ascii File"))
        self.actionexportpointsetnpy.setText(_translate("MainWindow", "NumPy"))
        # Quit
        self.actionquit.setText(_translate("MainWindow", "Quit"))
        # Shortcuts
        self.actionnewproject.setShortcut(QtGui.QKeySequence('Ctrl+N'))
        self.actionopenproject.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        self.actionsaveproject.setShortcut(QtGui.QKeySequence('Ctrl+S'))
        self.actionimportseisnpymat.setShortcut(QtGui.QKeySequence('Ctrl+M'))
        self.actionimportpsseisnpydictone.setShortcut(QtGui.QKeySequence('Ctrl+G'))
        self.actionimporthorizonnpydictone.setShortcut(QtGui.QKeySequence('Ctrl+H'))
        self.actionimportpointsetnpydictone.setShortcut(QtGui.QKeySequence('Ctrl+P'))
        self.actionquit.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        # ----------------------- End of File menu -------------------------
        #
        # ------------------- Manage menu ----------------------------
        # Survey
        self.actionmanagesurvey.setText(_translate("MainWindow", "Survey"))
        self.actionmanagesurvey.setToolTip("Manage Seismic Survey")
        # Seismic
        self.actionmanageseis.setText(_translate("MainWindow", "Seismic"))
        self.actionmanageseis.setToolTip("Manage Seismic")
        # Pre-stack seismic
        self.actionmanagepsseis.setText(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionmanagepsseis.setToolTip("Manage Pre-stack Seismic")
        # Horizon
        self.actionmanagehorizon.setText(_translate("MainWindow", "Horizon"))
        self.actionmanagehorizon.setToolTip("Manage Horizon")
        # PointSet
        self.actionmanagepointset.setText(_translate("MainWindow", "PointSet"))
        self.actionmanagepointset.setToolTip("Manage PointSet")
        # Shortcuts
        self.actionmanagesurvey.setShortcut(QtGui.QKeySequence('Shift+V'))
        self.actionmanageseis.setShortcut(QtGui.QKeySequence('Shift+M'))
        self.actionmanagepsseis.setShortcut(QtGui.QKeySequence('Shift+G'))
        self.actionmanagehorizon.setShortcut(QtGui.QKeySequence('Shift+H'))
        self.actionmanagepointset.setShortcut(QtGui.QKeySequence('Shift+P'))
        # ------------------ End of Manage menu -----------------------------
        #
        # -------------------- Tool menu ----------------------------
        # Data conversion
        self.menudataconversion.setTitle(_translate("MainWindow", "Data conversion"))
        # . seismic
        self.menuconvertseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionconvertseis2psseis.setText(_translate("MainWindow", "--> Pre-stack"))
        self.actionconvertseis2pointset.setText(_translate("MainWindow", "--> PointSet"))
        # . pre-stack seismic
        self.menuconvertpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionconvertpsseis2seis.setText(_translate("MainWindow", "--> Seismic"))
        # . horizon
        self.menuconverthorizon.setTitle(_translate("MainWindow", "Horizon"))
        self.actionconverthorizon2pointset.setText(_translate("MainWindow", "--> PointSet"))
        # . pointset
        self.menuconvertpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionconvertpointset2seis.setText(_translate("MainWindow", "--> Seismic"))
        self.actionconvertpointset2horizon.setText(_translate("MainWindow", "--> Horizon"))
        # Attribute engine
        self.menuattribengine.setTitle(_translate("MainWindow", "Seismic attribute"))
        # . mathematics
        self.menumathattrib.setTitle(_translate("MainWindow", "Mathematical"))
        self.actioncalcmathattribsingle.setText(_translate("MainWindow", "from Single property"))
        self.actioncalcmathattribmultiple.setText(_translate("MainWindow", "between Multiple properties"))
        # . instantaneous
        self.actioncalcinstanattrib.setText(_translate("MainWindow", "Instantaneous"))
        # --------------------------- end of Tool menu ----------------------------
        #
        # ---------------------- Visualization menu --------------------------
        # 1D
        self.menu1dwindow.setTitle(_translate("MainWindow", "1D window"))
        # . seismic
        self.menu1dwindowseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionplotvis1dseisz.setText(_translate("MainWindow", "Waveform"))
        self.actionplotvis1dseisz.setToolTip("1D Window: Seismic Waveform")
        self.actionplotvis1dseisfreq.setText(_translate("MainWindow", "Spectrum"))
        self.actionplotvis1dseisfreq.setToolTip("1D Window: Seismic Spectrum")
        # 2D
        self.menu2dwindow.setTitle(_translate("MainWindow", "2D window"))
        # . seismic
        self.menu2dwindowseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionplotvis2dseisinl.setText(_translate("MainWindow", "Inline"))
        self.actionplotvis2dseisinl.setToolTip("2D Window: Seismic Inline")
        self.actionplotvis2dseisxl.setText(_translate("MainWindow", "Crossline"))
        self.actionplotvis2dseisxl.setToolTip("2D Window: Seismic Crossline")
        self.actionplotvis2dseisz.setText(_translate("MainWindow", "Time/depth"))
        self.actionplotvis2dseisz.setToolTip("2D Window: Seismic Time/depth")
        # . pre-stack seismic
        self.menu2dwindowpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionplotvis2dpsseisshot.setText(_translate("MainWindow", "Gather"))
        self.actionplotvis2dpsseisshot.setToolTip("2D Window: Pre-stack Gather")
        # . pointset
        self.menu2dwindowpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionplotvis2dpointsetcrossplt.setText(_translate("MainWindow", "Cross-plot"))
        self.actionplotvis2dpointsetcrossplt.setToolTip("2D Window: PointSet Cross-plot")
        # 3D
        self.menu3dwindow.setTitle(_translate("MainWindow", "3D window"))
        # . seismic
        self.menu3dwindowseis.setTitle(_translate("MainWindow", 'Seismic'))
        self.actionplotvis3dseisinlxlz.setText(_translate("MainWindow", "IL/XL/Z"))
        # Shortcut
        self.actionplotvis1dseisz.setShortcut(QtGui.QKeySequence('Alt+W'))
        self.actionplotvis1dseisfreq.setShortcut(QtGui.QKeySequence('Alt+Q'))
        self.actionplotvis2dseisinl.setShortcut(QtGui.QKeySequence('Alt+I'))
        self.actionplotvis2dseisxl.setShortcut(QtGui.QKeySequence('Alt+X'))
        self.actionplotvis2dseisz.setShortcut(QtGui.QKeySequence('Alt+Z'))
        self.actionplotvis2dpsseisshot.setShortcut(QtGui.QKeySequence('Alt+G'))
        self.actionplotvis2dpointsetcrossplt.setShortcut(QtGui.QKeySequence('Alt+P'))
        self.actionplotvis3dseisinlxlz.setShortcut(QtGui.QKeySequence('Alt+M'))
        # ----------------------------- End of Visualization meu -----------------------
        #
        # --------------------- Utilities menu -------------------------
        # Settings
        self.menusettings.setTitle(_translate("MainWindow", 'Settings'))
        self.actionsettingsgui.setText(_translate("MainWindow", "Interface"))
        self.actionsettingsgeneral.setText(_translate("MainWindow", "General"))
        self.actionsettingsvisual.setText(_translate("MainWindow", "Visual"))
        self.actionsettingsviewer.setText(_translate("MainWindow", "Viewer"))
        # Shortcut
        self.actionsettingsgui.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F8))
        self.actionsettingsgeneral.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F9))
        self.actionsettingsvisual.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F10))
        self.actionsettingsviewer.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F11))
        # ---------------------- End of Utilities menu -----------------------
        #
        # --------------------- Help menu ----------------------------
        self.actionmanual.setText(_translate("MainWindow", "Manual"))
        self.actionsupport.setText(_translate("MainWindow", "Online support"))
        self.actionabout.setText(_translate("MainWindow", "About"))
        # Shortcut
        self.actionmanual.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1))
        # ----------------------- End of Help menu ------------------------
        #
        # ----------------------- Tool bar ----------------------------
        self.toolbarleft.setVisible(False)
        # self.toolbarleft.setVisible(self.settings['Gui']['Toolbar']['Left'])
        self.toolbarright.setVisible(self.settings['Gui']['Toolbar']['Right'])
        self.toolbartop.setVisible(self.settings['Gui']['Toolbar']['Top'])
        self.toolbarbottom.setVisible(self.settings['Gui']['Toolbar']['Bottom'])
        # ---------------------- End of Tool bar -------------------------------
        #
        # Events
        # ----------------------- File menu ----------------------
        # Project
        self.actionnewproject.triggered.connect(self.doNewProject)
        self.actionopenproject.triggered.connect(self.doOpenProject)
        self.actionsaveproject.triggered.connect(self.doSaveProject)
        self.actionsaveasproject.triggered.connect(self.doSaveasProject)
        # Import
        # . survey
        self.actionimportsurveymanual.triggered.connect(self.doImportSurveyManual)
        self.actionimportsurveysegy.triggered.connect(self.doImportSurveySegy)
        self.actionimportsurveynpy.triggered.connect(self.doImportSurveyNpy)
        # . seismic
        self.actionimportseissegy.triggered.connect(self.doImportSeisSegy)
        self.actionimportseisnpydictall.triggered.connect(self.doImportSeisNpyDictAll)
        self.actionimportseisnpydictone.triggered.connect(self.doImportSeisNpyDictOne)
        self.actionimportseisnpymat.triggered.connect(self.doImportSeisNpyMat)
        self.actionimportseisimageset.triggered.connect(self.doImportSeisImageSet)
        # . pre-stack seismic
        self.actionimportpsseissegy.triggered.connect(self.doImportPsSeisSegy)
        self.actionimportpsseisnpydictall.triggered.connect(self.doImportPsSeisNpyDictAll)
        self.actionimportpsseisnpydictone.triggered.connect(self.doImportPsSeisNpyDictOne)
        self.actionimportpsseisnpymat.triggered.connect(self.doImportPsSeisNpyMat)
        self.actionimportpsseisimageset.triggered.connect(self.doImportPsSeisImageSet)
        # . horizon
        self.actionimporthorizonfile.triggered.connect(self.doImportHorizonFile)
        self.actionimporthorizonnpydictall.triggered.connect(self.doImportHorizonNpyDictAll)
        self.actionimporthorizonnpydictone.triggered.connect(self.doImportHorizonNpyDictOne)
        self.actionimporthorizonnpymat.triggered.connect(self.doImportHorizonNpyMat)
        # . pointset
        self.actionimportpointsetfile.triggered.connect(self.doImportPointSetFile)
        self.actionimportpointsetnpydictall.triggered.connect(self.doImportPointSetNpyDictAll)
        self.actionimportpointsetnpydictone.triggered.connect(self.doImportPointSetNpyDictOne)
        self.actionimportpointsetnpymat.triggered.connect(self.doImportPointSetNpyMat)
        # Export
        # . survey
        self.actionexportsurvey.triggered.connect(self.doExportSurvey)
        # . seismic
        self.actionexportseissegy.triggered.connect(self.doExportSeisSegy)
        self.actionexportseisnpy.triggered.connect(self.doExportSeisNpy)
        self.actionexportseisimageset.triggered.connect(self.doExportSeisImageSet)
        # . pre-stack seismic
        self.actionexportpsseisnpy.triggered.connect(self.doExportPsSeisNpy)
        # . horizon
        self.actionexporthorizonfile.triggered.connect(self.doExportHorizonFile)
        self.actionexporthorizonnpy.triggered.connect(self.doExportHorizonNpy)
        # . pointset
        self.actionexportpointsetfile.triggered.connect(self.doExportPointSetFile)
        self.actionexportpointsetnpy.triggered.connect(self.doExportPointSetNpy)
        # Quit
        self.actionquit.triggered.connect(self.doQuit)
        # -------------------------- end of FIle menu ---------------------
        #
        # ---------------------------- Manage menu --------------------------
        self.actionmanagesurvey.triggered.connect(self.doManageSurvey)
        self.actionmanageseis.triggered.connect(self.doManageSeis)
        self.actionmanagepsseis.triggered.connect(self.doManagePsSeis)
        self.actionmanagehorizon.triggered.connect(self.doManageHorizon)
        self.actionmanagepointset.triggered.connect(self.doManagePointSet)
        # ----------------------- end of Manage menu -------------------------
        #
        # ------------------------ Tool menu
        # Data conversion
        self.actionconvertseis2psseis.triggered.connect(self.doConvertSeis2PsSeis)
        self.actionconvertseis2pointset.triggered.connect(self.doConvertSeis2PointSet)
        self.actionconvertpsseis2seis.triggered.connect(self.doConvertPsSeis2Seis)
        self.actionconverthorizon2pointset.triggered.connect(self.doConvertHorizon2PointSet)
        self.actionconvertpointset2seis.triggered.connect(self.doConvertPointSet2Seis)
        self.actionconvertpointset2horizon.triggered.connect(self.doConvertPointSet2Horizon)
        # Attribute engine
        self.actioncalcmathattribsingle.triggered.connect(self.doCalcMathAttribSingle)
        self.actioncalcmathattribmultiple.triggered.connect(self.doCalcMathAttribMultiple)
        self.actioncalcinstanattrib.triggered.connect(self.doCalcInstanAttrib)
        # -------------------------- End of Tool menu ---------------------------
        #
        # ------------------------- Visualization menu -----------------------------
        # 1D
        self.actionplotvis1dseisz.triggered.connect(self.doPlotVis1DSeisZ)
        self.actionplotvis1dseisfreq.triggered.connect(self.doPlotVis1DSeisFreq)
        # 2D
        self.actionplotvis2dseisinl.triggered.connect(self.doPlotVis2DSeisInl)
        self.actionplotvis2dseisxl.triggered.connect(self.doPlotVis2DSeisXl)
        self.actionplotvis2dseisz.triggered.connect(self.doPlotVis2DSeisZ)
        self.actionplotvis2dpsseisshot.triggered.connect(self.doPlotVis2DPsSeisShot)
        self.actionplotvis2dpointsetcrossplt.triggered.connect(self.doPlotVis2DPointSetCrossplt)
        # 3D
        self.actionplotvis3dseisinlxlz.triggered.connect(self.doPlotVis3DSeisInlXlZ)
        # ---------------------- end of Visualization menu ---------------------------
        #
        # -------------------------- Utilities menu -------------------------
        self.actionsettingsgui.triggered.connect(self.doSettingsGUI)
        self.actionsettingsgeneral.triggered.connect(self.doSettingsGeneral)
        self.actionsettingsvisual.triggered.connect(self.doSettingsVisual)
        self.actionsettingsviewer.triggered.connect(self.doSettingsViewer)
        # ------------------------ end of Utilities menu ---------------------
        #
        # ------------------------ Help menu -------------------------
        self.actionmanual.triggered.connect(self.doManual)
        self.actionsupport.triggered.connect(self.doSupport)
        self.actionabout.triggered.connect(self.doAbout)
        # ---------------------- end of Help menu ----------------------
        #
        # self.bkimage.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/background.png")).
        #                        scaled(700, 300, QtCore.Qt.KeepAspectRatio))
        # self.bkimage.setAlignment(QtCore.Qt.AlignCenter)
        #
        # ---------------------- main canvas -----------------------------
        #
        # seismic
        self.lblseis.setText(_translate("MainWindow", "Seismic:"))
        # seismic configuration
        self.btnconfigseisvis.setText(_translate("MainWindow", ""))
        self.btnconfigseisvis.setToolTip("Visualization")
        self.btnconfigseisvis.clicked.connect(self.clickBtnConfigSeisVis)
        # add seismic to canvas
        self.btnaddseis2canvas.setText(_translate("MainWindow", ""))
        self.btnaddseis2canvas.setToolTip("Add to canvas")
        self.btnaddseis2canvas.clicked.connect(self.clickBtnAddSeis2Canvas)
        #
        # horizon
        self.lblhorizon.setText(_translate("MainWindow", "Horizon:"))
        # horizon configuration
        self.btnconfighorizonvis.setText(_translate("MainWindow", ""))
        self.btnconfighorizonvis.setToolTip("Visualization")
        self.btnconfighorizonvis.clicked.connect(self.clickBtnConfigHorizonVis)
        # add horizon to canvas
        self.btnaddhorizon2canvas.setText(_translate("MainWindow", ""))
        self.btnaddhorizon2canvas.setToolTip("Add to canvas")
        self.btnaddhorizon2canvas.clicked.connect(self.clickBtnAddHorizon2Canvas)
        #
        # pointset
        self.lblpointset.setText(_translate("MainWindow", "PointSet:"))
        # point configuration
        self.btnconfigpointsetvis.setText(_translate("MainWindow", ""))
        self.btnconfigpointsetvis.setToolTip("Visualization")
        self.btnconfigpointsetvis.clicked.connect(self.clickBtnConfigPointSetVis)
        # add pointset to canvas
        self.btnaddpointset2canvas.setText(_translate("MainWindow", ""))
        self.btnaddpointset2canvas.setToolTip("Add to canvas")
        self.btnaddpointset2canvas.clicked.connect(self.clickBtnAddPointSet2Canvas)
        #
        # main canvas
        self.canvas = scene.SceneCanvas(keys='interactive', title='Canvas', bgcolor=[0.5, 0.5, 0.5],
                                        size=(1130, 850), app='pyqt5', parent=self.wgtcanvas)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.TurntableCamera(elevation=30, azimuth=135)
        #
        # survey box
        self.btnsrvbox.setText(_translate("MainWindow", ""))
        self.btnsrvbox.setToolTip("Survey box")
        self.btnsrvbox.setDefault(False)
        self.btnsrvbox.clicked.connect(self.clickBtnSrvBox)
        #
        # xyz axis
        self.btnxyzaxis.setText(_translate("MainWindow", ""))
        self.btnxyzaxis.setToolTip("XYZ axis")
        self.btnxyzaxis.setDefault(False)
        self.btnxyzaxis.clicked.connect(self.clickBtnXYZAxis)
        #
        # snapshot
        self.btnsnapshot.setText(_translate("MainWindow", ""))
        self.btnsnapshot.setToolTip("Snapshot")
        self.btnsnapshot.setDefault(False)
        self.btnsnapshot.clicked.connect(self.clickBtnSnapshot)
        #
        # home
        self.btngohome.setText(_translate("MainWindow", ""))
        self.btngohome.setDefault(True)
        self.btngohome.setToolTip("Home view")
        self.btngohome.clicked.connect(self.clickBtnGoHome)
        #
        # view angle
        self.cbbviewfrom.addItems(['Inline', 'Crossline', 'Top'])
        self.cbbviewfrom.setItemIcon(0, QtGui.QIcon(
            QtGui.QPixmap(os.path.join(self.iconpath, "icons/visinl.png")).scaled(30, 30)))
        self.cbbviewfrom.setItemIcon(1, QtGui.QIcon(
            QtGui.QPixmap(os.path.join(self.iconpath, "icons/visxl.png")).scaled(30, 30)))
        self.cbbviewfrom.setItemIcon(2, QtGui.QIcon(
            QtGui.QPixmap(os.path.join(self.iconpath, "icons/visz.png")).scaled(30, 30)))
        self.cbbviewfrom.setCurrentIndex(0)
        self.cbbviewfrom.currentIndexChanged.connect(self.changeCbbViewFrom)
        #
        # z scale
        self.ldtzscale.setText(_translate("MainWindow", "1.0"))
        self.ldtzscale.textChanged.connect(self.changeLdtZScale)
        #
        self.updateSurveyVis()
        self.updateSeisVis()
        self.updateHorizonVis()
        self.updatePointSetVis()
        # ------------------ end of main canvas ----------------------------------------


    def doNewProject(self):
        self.projname = 'New project'
        self.projpath = ''
        self.survinfo = {}
        self.seisdata = {}
        self.psseisdata = {}
        self.horizondata = {}
        self.faultpatchdata = {}
        self.pointsetdata = {}
        self.welllogdata = {}
        #
        self.settings = core_set.Settings
        #
        self.canvas = None
        self.view = None
        self.canvasproperties = {}
        self.canvascomponents = {}
        self.seisvisconfig = {}
        self.horizonvisconfig = {}
        self.pointsetvisconfig = {}
        #
        self.dialog.setWindowTitle("GAEIO" + " <" + self.projname + ">")
        #
        self.setSettings(self.settings)
        #
        self.updateSurveyVis()
        self.updateSeisVis()
        self.updateHorizonVis()
        self.updatePointSetVis()


    def doOpenProject(self):
        self.refreshMsgBox()

        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Project NumPy', self.settings['General']['RootPath'],
                                        filter="Project Numpy files (*.proj.npy);; All files (*.*)")
        #
        # clear windon before opening it to remove all same component from previous projects
        if os.path.exists(_file[0]):
            self.doNewProject()
        #
        self.projpath = os.path.split(_file[0])[0]
        _projname = os.path.basename(_file[0])
        self.projname = _projname.replace('.proj.npy', '')
        if os.path.exists(os.path.join(self.projpath, self.projname+'.proj.npy')) is False \
                or os.path.exists(os.path.join(self.projpath, self.projname+'.proj.data')) is False:
            vis_msg.print("ERROR in doOpenProj: No Project selected", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No Project NumPy')
            return
        print("doOpenProj: Import Project: " + os.path.join(self.projpath, self.projname+'proj.npy'))
        #
        try:
            _proj = np.load(os.path.join(self.projpath, self.projname+'.proj.npy'), allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in doOpenProj: Non-dictionary Project NumPy selected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Open Project',
                                           'Non-dictionary Project NumPy selected')
            return
        #
        # Survey
        if 'survinfo' in _proj.keys():
            self.survinfo = _proj['survinfo']
            if os.path.exists(os.path.join(self.projpath,
                                           self.projname + '.proj.data/Survey/' + 'survey' + '.srv.npy')):
                try:
                    _survinfo = np.load(os.path.join(self.projpath,
                                                     self.projname + '.proj.data/Survey/' + 'survey' + '.srv.npy'),
                                        allow_pickle=True).item()
                except ValueError:
                    _survinfo = {}
                if checkSurvInfo(_survinfo):
                    self.survinfo = _survinfo
        else:
            self.survinfo = {}
        #
        # Seismic
        if 'survinfo' in _proj.keys() and 'seisdata' in _proj.keys():
            self.seisdata = {}
            for key in _proj['seisdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname+'.proj.data/Seismic/'+key+'.seis.npy')):
                    try:
                        _seisdata = np.load(os.path.join(self.projpath,
                                                              self.projname + '.proj.data/Seismic/' + key + '.seis.npy'))
                    except ValueError:
                        _seisdata = []
                    if checkSeisData(_seisdata, self.survinfo):
                        self.seisdata[key] = _seisdata
        else:
            self.seisdata = {}
        #
        # Pre-stack seismic
        if 'psseisdata' in _proj.keys():
            self.psseisdata = {}
            for key in _proj['psseisdata'].keys():
                _psseisdata = {}
                for shot in _proj['psseisdata'][key].keys():
                    _psseisdata[shot] = {}
                    if os.path.exists(os.path.join(self.projpath,
                                                   self.projname + '.proj.data/PsSeismic/' +
                                                   key +'_shot_' + shot + '.psseis.npy')):
                        try:
                            _psseisdata[shot] = \
                                np.load(os.path.join(self.projpath, self.projname + '.proj.data/PsSeismic/' +
                                                     key + '_shot_' + shot + '.psseis.npy'), allow_pickle=True).item()
                        except ValueError:
                            _psseisdata[shot] = {}
                if checkPsSeisData(_psseisdata):
                    self.psseisdata[key] = _psseisdata
        else:
            self.psseisdata = {}
        #
        # Horizon
        if 'horizondata' in _proj.keys():
            self.horizondata = {}
            for _key in _proj['horizondata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname + '.proj.data/Horizon/' + _key + '.hrz.npy')):
                    try:
                        _horizondata = np.load(os.path.join(self.projpath,
                                                            self.projname + '.proj.data/Horizon/' + _key + '.hrz.npy'),
                                               allow_pickle=True).item()
                    except ValueError:
                        _horizondata = {}
                    if checkHorizonData(_horizondata):
                        self.horizondata[_key] = _horizondata
        else:
            self.horizondata = {}
        #
        # FaultPatch
        if 'faultpatchdata' in _proj.keys():
            self.faultpatchdata = {}
            for _key in _proj['faultpatchdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname + '.proj.data/FaultPatch/' + _key + '.ftp.npy')):
                    try:
                        _faultdata = np.load(os.path.join(self.projpath,
                                                          self.projname + '.proj.data/FaultPatch/' + _key + '.ftp.npy'),
                                             allow_pickle=True).item()
                    except ValueError:
                        _faultdata = {}
                    if checkFaultPatchData(_faultdata):
                        self.faultpatchdata[key] = _faultdata
        else:
            self.faultpatchdata = {}
        # PointSet
        if 'pointsetdata' in _proj.keys():
            self.pointsetdata = {}
            for key in _proj['pointsetdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname+'.proj.data/PointSet/'+key+'.pts.npy')):
                    try:
                        _pointsetdata = np.load(os.path.join(self.projpath,
                                                             self.projname + '.proj.data/PointSet/' + key + '.pts.npy'),
                                                allow_pickle=True).item()
                    except ValueError:
                        _pointsetdata = {}
                    if checkPointSetData(_pointsetdata):
                        self.pointsetdata[key] = _pointsetdata
        else:
            self.pointsetdata = {}
        # WellLog
        if 'welllogdata' in _proj.keys():
            self.welllogdata = {}
            for key in _proj['welllogdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname + '.proj.data/WellLog/' + key + '.wlg.npy')):
                    try:
                        _welllogdata = np.load(os.path.join(self.projpath,
                                                            self.projname + '.proj.data/WellLog/' + key + '.wlg.npy'),
                                               allow_pickle=True).item()
                    except ValueError:
                        _welllogdata = {}
                    if checkWellLogData(_welllogdata):
                        self.welllogdata[key] = _welllogdata
        else:
            self.welllogdata = {}
        # Settings
        if 'settings' in _proj.keys():
            if os.path.exists(os.path.join(self.projpath,
                                           self.projname + '.proj.data/Settings/' + 'settings' + '.npy')):
                try:
                    _settings = np.load(os.path.join(self.projpath,
                                                     self.projname + '.proj.data/Settings/' + 'settings' + '.npy'),
                                        allow_pickle=True).item()
                except ValueError:
                    _settings = {}
                if checkSettings(_settings):
                    self.settings = _settings
        # else:
        #     self.settings = {}
        #
        self.dialog.setWindowTitle("GAEIO" + " <" + self.projname + ">")
        self.settings['General']['RootPath'] = self.projpath
        #
        self.setSettings(self.settings)
        #
        # initialize canvas
        self.updateSurveyVis()
        self.updateSeisVis()
        self.updateHorizonVis()
        self.updatePointSetVis()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Open Project",
                                          "Project " + self.projname + " loaded successfully")


    def doSaveProject(self):
        self.refreshMsgBox()
        #
        if len(self.projpath) > 1:
            saveProject(survinfo=self.survinfo, seisdata=self.seisdata,
                        psseisdata=self.psseisdata,
                        horizondata=self.horizondata,
                        faultpatchdata=self.faultpatchdata,
                        pointsetdata=self.pointsetdata,
                        welllogdata=self.welllogdata,
                        settings=self.settings,
                        savepath=self.projpath, savename=self.projname)
            #
            QtWidgets.QMessageBox.information(self.msgbox,
                                              "Save Project",
                                              "Project " + self.projname + " saved successfully")
        else:
            self.doSaveasProject()


    def doSaveasProject(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Project NumPy', self.settings['General']['RootPath'],
                                        filter="Project NumPy files (*.proj.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.projpath = os.path.split(_file[0])[0]
            _name = os.path.split(_file[0])[1]
            self.projname = _name.replace('.proj.npy', '')
            #
            self.dialog.setWindowTitle("GAEIO" + " <" + self.projname + ">")
            self.settings['General']['RootPath'] = self.projpath
            #
            saveProject(survinfo=self.survinfo, seisdata=self.seisdata,
                        psseisdata=self.psseisdata,
                        horizondata=self.horizondata,
                        faultpatchdata=self.faultpatchdata,
                        pointsetdata=self.pointsetdata,
                        welllogdata=self.welllogdata,
                        settings=self.settings,
                        savepath=self.projpath, savename=self.projname)
            #
            QtWidgets.QMessageBox.information(self.msgbox,
                                              "Save Project",
                                              "Project " + self.projname + " saved successfully")


    def doImportSurveyManual(self):
        _importsurvey = QtWidgets.QDialog()
        _gui = gui_importsurveymanual()
        _gui.survinfo = self.survinfo
        _gui.setupGUI(_importsurvey)
        _importsurvey.exec_()
        self.survinfo = _gui.survinfo
        _importsurvey.show()
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSurveySegy(self):
        _importsurvey = QtWidgets.QDialog()
        _gui = gui_importsurveysegy()
        _gui.survinfo = self.survinfo
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsurvey)
        _importsurvey.exec_()
        self.survinfo = _gui.survinfo
        _importsurvey.show()
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSurveyNpy(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Survey NumPy', self.settings['General']['RootPath'],
                                        filter="Survey Numpy files (*.srv.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            vis_msg.print("ERROR in ImportSurveyNpy: No NumPy selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportSurveyNpy: Import Survey Numpy: " + _file[0])
        try:
            _survinfo = np.load(_file[0], allow_pickle=True).item()
            #
            if checkSurvInfo(_survinfo) is False:
                vis_msg.print("ERROR in ImportSurveyNpy: No survey NumPy selected for import", type='error')
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import NumPy',
                                               'No NumPy selected for import')
                return
            #
            self.survinfo = _survinfo
        except ValueError:
            vis_msg.print("ERROR in ImportSurveyNpy: Numpy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import NumPy',
                                           'Numpy dictionary expected')
            return
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Survey NumPy",
                                          "Survey imported successfully")
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSeisSegy(self):
        _importsegy = QtWidgets.QDialog()
        _gui = gui_importseissegy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsegy)
        _importsegy.exec_()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _importsegy.show()
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSeisNpyDictAll(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Seismic NumPy Dictionary (all in one)',
                                        self.settings['General']['RootPath'],
                                        filter="Seismic NumPy files (*.seis.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            vis_msg.print("ERROR in ImportSeisNpyDictAll: No NumPy Dictionary selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportSeisNpyDictAll: Import Seismic Numpy Dictionary (all in one): " + _file[0])
        try:
            _npydata = np.load(_file[0], allow_pickle=True).item()
            if ('SeisInfo' not in _npydata.keys())\
                    or (seis_ays.checkSeisInfo(_npydata['SeisInfo']) is False):
                vis_msg.print("ERROR in ImportSeisNpyDictAll: NumPy dictionary contains no information about seismic survey",
                              type='error')
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import Seismic NumPy Dictionary (all in one)',
                                               'NumPy dictionary contains no information about seismic')
                return
            _survinfo = _npydata['SeisInfo']
            _seisdata = {}
            if 'SeisData' in _npydata.keys() and type(_npydata['SeisData']) is dict:
                for key in _npydata['SeisData'].keys():
                    if checkSeisData(_npydata['SeisData'][key], _survinfo):
                        _seisdata[key] = _npydata['SeisData'][key]
        except ValueError:
            vis_msg.print("ERROR in ImportSeisNpyDictAll: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic NumPy Dictionary (all in one)',
                                           'NumPy dictionary expected')
            return
        #
        # check z sign
        if _survinfo['ZStep'] >= 0:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic Numpy Dictionary (all in one)',
                                                       'Warning: positive z wii be reversed. Continue?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            _survinfo['ZStart'] = - _survinfo['ZStart']
            _survinfo['ZStep'] = - _survinfo['ZStep']
            _survinfo['ZEnd'] = - _survinfo['ZEnd']
            _survinfo['ZRange'] = - _survinfo['ZRange']
        #
        # add new data to seisdata
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys() and checkSeisData(self.seisdata[key], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic NumPy Dictionary (all in one)',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seisdata[key] = _seisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Seismic NumPy Dictionary (all in one)",
                                          "NumPy dictionary imported successfully")
        #
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSeisNpyDictOne(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Seismic NumPy Dictionary (individual)',
                                         self.settings['General']['RootPath'],
                                         filter="Seismic NumPy files (*.seis.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR in ImportSeisNpyDict: No NumPy Dictionary selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        try:
            _seisdata = {}
            for _i in range(len(_file[0])):
                _npydata = np.load(_file[0][_i], allow_pickle=True).item()
                _filename = (os.path.basename(_file[0][_i])).replace('.seis.npy', '')
                #
                print("ImportSeisNpyMat: Import %d of %d Seismic Numpy Dictionary (individual): %s"
                      % (_i + 1, len(_file[0]), _filename))
                #
                if ('SeisInfo' not in _npydata.keys()) \
                        or (seis_ays.checkSeisInfo(_npydata['SeisInfo']) is False):
                    vis_msg.print(
                        "ERROR in ImportSeisNpyDict: NumPy dictionary contains no information about seismic survey",
                        type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import Seismic NumPy Dictionary (individual)',
                                                   'NumPy dictionary contains no information about seismic')
                    return
                _survinfo = _npydata['SeisInfo']
                if 'SeisData' in _npydata.keys():
                    if checkSeisData(_npydata['SeisData'], _survinfo):
                        _seisdata[_filename] = _npydata['SeisData']
                #
        except ValueError:
            vis_msg.print("ERROR in ImportSeisNpyDict: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic NumPy Dictionary (individual)',
                                           'NumPy dictionary expected')
            return
        #
        # check z sign
        if _survinfo['ZStep'] >= 0:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic Numpy Dictionary (individual)',
                                                       'Warning: positive z wii be reversed. Continue?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            _survinfo['ZStart'] = - _survinfo['ZStart']
            _survinfo['ZStep'] = - _survinfo['ZStep']
            _survinfo['ZEnd'] = - _survinfo['ZEnd']
            _survinfo['ZRange'] = - _survinfo['ZRange']
        #
        # add new data to seisdata
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys() and checkSeisData(self.seisdata[key], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic NumPy Dictionary',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seisdata[key] = _seisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Seismic NumPy Dictionary",
                                          "NumPy dictionary imported successfully")
        #
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSeisNpyMat(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Seismic NumPy 2/3D Matrix',
                                         self.settings['General']['RootPath'],
                                         filter="Seismic NumPy files (*.seis.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR in ImportSeisNpyMat: No NumPy 2/3D Matrix selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportSeisNpyMat: Import %d Seismic Numpy 2/3D Matrix" %len(_file[0]))
        try:
            _seisdata = {}
            for _i in range(len(_file[0])):
                _npydata = np.load(_file[0][_i])
                _filename = (os.path.basename(_file[0][_i])).replace('.seis.npy', '')
                #
                print("ImportSeisNpyMat: Import %d of %d Seismic Numpy 2/3D Matrix: %s"
                      % (_i + 1, len(_file[0]), _filename))
                #
                if np.ndim(_npydata) <= 1 or np.ndim(_npydata) >= 4:
                    vis_msg.print("ERROR in ImportSeisNpyMat: NumPy matrix shall be 2D or 3D", type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import Seismic NumPy 2/3D Matrix',
                                                   'NumPy matrix shall be 2D or 3D')
                    return
                if np.ndim(_npydata) == 2:
                    if np.shape(_npydata)[1] < 4:
                        vis_msg.print("ERROR in ImportSeisNpyMat: 2D NumPy matrix shall contain at least 4 columns",
                                      type='error')
                        QtWidgets.QMessageBox.critical(self.msgbox,
                                                       'Import Seismic NumPy 2/3D Matrix',
                                                       '2D NumPy matrix shall contain at least 4 columns')
                        return
                    _survinfo = seis_ays.getSeisInfoFrom2DMat(_npydata)
                    _npydata = np.transpose(np.reshape(_npydata[:, 3:4], [_survinfo['ILNum'],
                                                                          _survinfo['XLNum'],
                                                                          _survinfo['ZNum']]), [2, 1, 0])
                if np.ndim(_npydata) == 3:
                    if checkSurvInfo(self.survinfo) \
                            and self.survinfo['ZNum'] == np.shape(_npydata)[0] \
                            and self.survinfo['XLNum'] == np.shape(_npydata)[1] \
                            and self.survinfo['ILNum'] == np.shape(_npydata)[2]:
                        _survinfo = self.survinfo
                    else:
                        _survinfo = seis_ays.createSeisInfoFrom3DMat(_npydata)
                    _npydata = _npydata
                #
                if checkSeisData(_npydata, _survinfo):
                    _seisdata[_filename] = _npydata
        except ValueError:
            vis_msg.print("ERROR in ImportSeisNpy: NumPy 2/3D matrix expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic NumPy 2/3D Matrix',
                                           'NumPy matrix expected')
            return
        #
        # check z sign
        if _survinfo['ZStep'] >= 0:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic Numpy 2/3D Matrix',
                                                       'Warning: positive z wii be reversed. Continue?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            _survinfo['ZStart'] = - _survinfo['ZStart']
            _survinfo['ZStep'] = - _survinfo['ZStep']
            _survinfo['ZEnd'] = - _survinfo['ZEnd']
            _survinfo['ZRange'] = - _survinfo['ZRange']
        #
        # add new data to seisdata
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys() and checkSeisData(self.seisdata[key], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic NumPy 2/3D Matrix',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seisdata[key] = _seisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Seismic NumPy 2/3D Matrix",
                                          str(len(_file[0])) + " NumPy matrix imported successfully")
        #
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportSeisImageSet(self):
        _importimage = QtWidgets.QDialog()
        _gui = gui_importseisimageset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importimage)
        _importimage.exec_()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _importimage.show()
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doImportPsSeisSegy(self):
        _importsegy = QtWidgets.QDialog()
        _gui = gui_importpsseissegy()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsegy)
        _importsegy.exec_()
        self.psseisdata = _gui.psseisdata
        _importsegy.show()


    def doImportPsSeisNpyDictAll(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Pre-stack Seismic NumPy Dictionary (all in one)', self.settings['General']['RootPath'],
                                        filter="Pre-stack Seismic NumPy files (*.psseis.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            vis_msg.print("ERROR: doImportPsSeisNpyDictAll: No NumPy dictionary selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("doImportPsSeisNpyDictAll: Import Numpy Dictionary (all in one): " + _file[0])
        try:
            _psseisdata = np.load(_file[0], allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in ImportPsSeisNpyDictAll: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic NumPy Dictionary (all in one)',
                                           'NumPy dictionary expected')
            return
        #
        # add new data to psseisdata
        for key in _psseisdata.keys():
            if key in self.psseisdata.keys() and checkPsSeisData(self.psseisdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic NumPy',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.psseisdata[key] = _psseisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Pre-stack Seismic NumPy Dictionary (all in one)",
                                          "NumPy dictionary imported successfully")
        #
        return


    def doImportPsSeisNpyDictOne(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Pre-stack Seismic NumPy Dictionary (individual)',
                                         self.settings['General']['RootPath'],
                                         filter="Pre-stack Seismic NumPy files (*.psseis.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR: doImportPsSeisNpyDictOne: No NumPy dictionary (individual) selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        #
        try:
            #
            _psseisdata = {}
            for _i in range(len(_file[0])):
                _filename = (os.path.basename(_file[0][_i])).replace('.psseis.npy', '')
                print("ImportPsSeisNpyDictOne: Import %d of %d Pre-stack Seismic Numpy Dictionary (individual): %s"
                      % (_i + 1, len(_file[0]), _filename))
                _psseisdata[_filename] = {}
                _psseisdata[_filename]['0'] = np.load(_file[0][_i], allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in ImportPsSeisNpyDictOne: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic NumPy Dictionary (individual)',
                                           'NumPy dictionary expected')
            return
        #
        # add new data to psseisdata
        for key in _psseisdata.keys():
            if key in self.psseisdata.keys() and checkPsSeisData(self.psseisdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic NumPy Dictionary (individual)',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.psseisdata[key] = _psseisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Pre-stack Seismic NumPy Dictionary (individual)",
                                          str(len(_file[0])) + " NumPy dictionary imported successfully")
        #
        return


    def doImportPsSeisNpyMat(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Pre-stack Seismic NumPy 2/3D Matrix',
                                         self.settings['General']['RootPath'],
                                         filter="Pre-stack Seismic NumPy files (*.psseis.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR: doImportPsSeisNpyMat: No NumPy 2/3D Matrix selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        try:
            _psseisdata = {}
            for _i in range(len(_file[0])):
                _filename = (os.path.basename(_file[0][_i])).replace('.psseis.npy', '')
                print("doImportPsSeisNpyMat: Import %d of %d Pre-stack Seismic Numpy 2/3D Matrix: %s"
                      % (_i + 1, len(_file[0]), _filename))
                _npydata = np.load(_file[0][_i])
                if np.ndim(_npydata) == 2:
                    _npydata = np.expand_dims(_npydata, axis=2)
                #
                _psseisdata[_filename] = {}
                _psseisdata[_filename]['0'] = {}
                _psseisdata[_filename]['0']['ShotData'] = _npydata
                _psseisdata[_filename]['0']['ShotInfo'] = psseis_ays.createShotInfoFromShotData(_npydata)
        except ValueError:
            vis_msg.print("ERROR in doImportPsSeisNpyMat: NumPy Matrix expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic NumPy 2/3D Matrix',
                                           'NumPy matrix expected')
            return
        #
        # add new data to psseisdata
        for key in _psseisdata.keys():
            if key in self.psseisdata.keys() and checkPsSeisData(self.psseisdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic NumPy 2/3D Matrix',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.psseisdata[key] = _psseisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Pre-stack Seismic NumPy 2/3D Matrix",
                                          str(len(_file[0])) + " NumPy matrix imported successfully")
        #
        return


    def doImportPsSeisImageSet(self):
        _importimage = QtWidgets.QDialog()
        _gui = gui_importpsseisimageset()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importimage)
        _importimage.exec_()
        self.psseisdata = _gui.psseisdata
        _importimage.show()


    def doImportHorizonFile(self):
        _import = QtWidgets.QDialog()
        _gui = gui_importhorizonfile()
        _gui.horizondata = self.horizondata.copy()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_import)
        _import.exec()
        self.horizondata = _gui.horizondata.copy()
        _import.show()
        #
        self.updateHorizonVis()


    def doImportHorizonNpyDictAll(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Horizon NumPy Dictionary (all in one)',
                                        self.settings['General']['RootPath'],
                                        filter="Horizon NumPy files (*.hrz.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            vis_msg.print("ERROR in ImportHorizonNpyDictAll: No NumPy Dictionary selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportHorizonNpyDictAll: Import Numpy Dictionary (all in one): " + _file[0])
        try:
            _horizondata = np.load(_file[0], allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in ImportHorizonNpyDictAll: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import HOrizon NumPy Dictionary (all in one)',
                                           'NumPy dictionary expected')
            return
        #
        # add new data to horizondata
        for key in _horizondata.keys():
            if key in self.horizondata.keys() and checkHorizonData(_horizondata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Horizon NumPy',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.horizondata[key] = _horizondata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Horizon NumPy Dictionary (all in one)",
                                          "NumPy dictionary (all in one) imported successfully")
        #
        self.updateHorizonVis()


    def doImportHorizonNpyDictOne(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Horizon NumPy Dictionary (individual)',
                                         self.settings['General']['RootPath'],
                                         filter="Horizon NumPy files (*.hrz.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR in ImportHorizonNpyDictOne: No NumPy dictionary (individual) selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        try:
            #
            _horizondata = {}
            for _i in range(len(_file[0])):
                _filename = (os.path.basename(_file[0][_i])).replace('.hrz.npy', '')
                print("ImportHorizonNpyDictOne: Import %d of %d Horizon Numpy Dictionary (individual): %s"
                      % (_i + 1, len(_file[0]), _filename))
                _horizondata[_filename] = np.load(_file[0][_i], allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in ImportHorizonNpyDictOne: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Horizon NumPy Dictionary (individual)',
                                           'NumPy dictionary expected')
            return
        #
        # add new data to pointsetdata
        for key in _horizondata.keys():
            if key in self.horizondata.keys() and checkHorizonData(_horizondata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Horizon NumPy Dictionary (individual)',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.horizondata[key] = _horizondata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Horizon NumPy Dictionary",
                                          str(len(_file[0])) + " NumPy dictionary imported successfully")
        #
        self.updateHorizonVis()


    def doImportHorizonNpyMat(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Horizon NumPy 2D Matrix',
                                         self.settings['General']['RootPath'],
                                         filter="Horizon NumPy files (*.hrz.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR in ImportHorizonNpyMat: No NumPy matrix selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        try:
            _horizondata = {}
            for _i in range(len(_file[0])):
                _filename = (os.path.basename(_file[0][_i])).replace('.hrz.npy', '')
                print("ImportHorizonNpyMat: Import %d of %d Horizon Numpy 2D Matrix: %s"
                      % (_i + 1, len(_file[0]), _filename))
                _npydata = np.load(_file[0][_i])
                if np.ndim(_npydata) != 2:
                    vis_msg.print("ERROR in ImportHorizonNpyMat: NumPy matrix shall be 2D", type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import Horizon NumPy 2D matrix',
                                                   'NumPy matrix shall be 2D')
                    return
                _ncol = np.shape(_npydata)[1]
                if _ncol < 3:
                    vis_msg.print("ERROR in ImportHorizonNpyMat: 2D NumPy matrix shall contain at least 3 columns",
                                  type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import Horizon NumPy 2D matrix',
                                                   '2D NumPy matrix shall contain at least 3 columns')
                    return
                _pointsetdata = {}
                _pointsetdata['Inline'] = _npydata[:, 0:1]
                _pointsetdata['Crossline'] = _npydata[:, 1:2]
                _pointsetdata['Z'] = _npydata[:, 2:3]
                for _i in range(_ncol - 3):
                    _pointsetdata['property_' + str(_i + 1)] = _npydata[:, _i + 3:_i + 4]
                #
                _horizondata[_filename] = point_ays.convertPointSet2Horizon(pointset=_pointsetdata,
                                                                            property_list=list(_pointsetdata.keys()))
        except ValueError:
            vis_msg.print("ERROR in ImportHorizonNpyMat: NumPy Matrix expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Horizon NumPy 2D Matrix',
                                           'NumPy matrix expected')
            return
        #
        # add new data to pointsetdata
        for key in _horizondata.keys():
            if key in self.horizondata.keys() and checkHorizonData(_horizondata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Horizon NumPy 2D Matrix',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.horizondata[key] = _horizondata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Horizon NumPy 2D Matrix",
                                          str(len(_file[0])) + " NumPy matrix imported successfully")
        #
        self.updateHorizonVis()


    def doImportPointSetFile(self):
        _importpoint = QtWidgets.QDialog()
        _gui = gui_importpointsetfile()
        _gui.pointsetdata = self.pointsetdata.copy()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importpoint)
        _importpoint.exec()
        self.pointsetdata = _gui.pointsetdata.copy()
        _importpoint.show()
        #
        self.updatePointSetVis()


    def doImportPointSetNpyDictAll(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select PointSet NumPy Dictionary (all in one)', self.settings['General']['RootPath'],
                                        filter="PointSet NumPy files (*.pts.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            vis_msg.print("ERROR in ImportPointSetNpyDictAll: No NumPy Dictionary selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportPointSetNpyDictAll: Import Numpy Dictionary (all in one): " + _file[0])
        try:
            _pointsetdata = np.load(_file[0], allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in ImportPointSetNpyDictAll: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet NumPy Dictionary (all in one)',
                                           'NumPy dictionary expected')
            return
        #
        # add new data to pointsetdata
        print(_pointsetdata.keys())
        for key in _pointsetdata.keys():
            if key in self.pointsetdata.keys() and checkPointSetData(_pointsetdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import PointSet NumPy',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.pointsetdata[key] = _pointsetdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import PointSet NumPy Dictionary (all in one)",
                                          "NumPy dictionary (all in one) imported successfully")
        #
        self.updatePointSetVis()


    def doImportPointSetNpyDictOne(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select PointSet NumPy Dictionary (individual)',
                                         self.settings['General']['RootPath'],
                                         filter="PointSet NumPy files (*.pts.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR in ImportPointSetNpyDictOne: No NumPy dictionary (individual) selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        try:
            #
            _pointsetdata = {}
            for _i in range(len(_file[0])):
                _filename = (os.path.basename(_file[0][_i])).replace('.pts.npy', '')
                print("ImportPointSetNpyDictOne: Import %d of %d PointSet Numpy Dictionary (individual): %s"
                      % (_i + 1, len(_file[0]), _filename))
                _pointsetdata[_filename] = np.load(_file[0][_i], allow_pickle=True).item()
        except ValueError:
            vis_msg.print("ERROR in ImportPointSetNpyDictOne: NumPy dictionary expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet NumPy Dictionary (individual)',
                                           'NumPy dictionary expected')
            return
        #
        # add new data to pointsetdata
        for key in _pointsetdata.keys():
            if key in self.pointsetdata.keys() and checkPointSetData(_pointsetdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import PointSet NumPy Dictionary (individual)',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.pointsetdata[key] = _pointsetdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import PointSet NumPy Dictionary",
                                          str(len(_file[0])) + " NumPy dictionary imported successfully")
        #
        self.updatePointSetVis()


    def doImportPointSetNpyMat(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select PointSet NumPy 2D Matrix', self.settings['General']['RootPath'],
                                         filter="PointSet NumPy files (*.pts.npy);; All files (*.*)")
        if len(_file[0]) < 1:
            vis_msg.print("ERROR in ImportPointSetNpyMat: No NumPy matrix selected for import", type='error')
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        try:
            _pointsetdata = {}
            for _i in range(len(_file[0])):
                _filename = (os.path.basename(_file[0][_i])).replace('.pts.npy', '')
                print("ImportPointSetNpyMat: Import %d of %d PointSet Numpy 2D Matrix: %s"
                      % (_i + 1, len(_file[0]), _filename))
                _npydata = np.load(_file[0][_i])
                if np.ndim(_npydata) != 2:
                    vis_msg.print("ERROR in ImportPointSetNpyMat: NumPy matrix shall be 2D", type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import PointSet NumPy 2D matrix',
                                                   'NumPy matrix shall be 2D')
                    return
                _ncol = np.shape(_npydata)[1]
                if _ncol < 3:
                    vis_msg.print("ERROR in ImportPointSetNpyMat: 2D NumPy matrix shall contain at least 3 columns",
                                  type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import PointSet NumPy 2D matrix',
                                                   '2D NumPy matrix shall contain at least 3 columns')
                    return
                _pointsetdata[_filename] = {}
                _pointsetdata[_filename]['Inline'] = _npydata[:, 0:1]
                _pointsetdata[_filename]['Crossline'] = _npydata[:, 1:2]
                _pointsetdata[_filename]['Z'] = _npydata[:, 2:3]
                for _i in range(_ncol - 3):
                    _pointsetdata[_filename]['property_' + str(_i + 1)] = _npydata[:, _i + 3:_i + 4]
        except ValueError:
            vis_msg.print("ERROR in ImportPointSetNpyMat: NumPy Matrix expected", type='error')
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet NumPy 2D Matrix',
                                           'NumPy matrix expected')
            return
        #
        # add new data to pointsetdata
        for key in _pointsetdata.keys():
            if key in self.pointsetdata.keys() and checkPointSetData(_pointsetdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import PointSet NumPy 2D Matrix',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.pointsetdata[key] = _pointsetdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import PointSet NumPy 2D Matrix",
                                          str(len(_file[0])) + " NumPy matrix imported successfully")
        #
        self.updatePointSetVis()


    def doExportSurvey(self):
        _exportsurvey = QtWidgets.QDialog()
        _gui = gui_exportsurvey()
        _gui.survinfo = self.survinfo
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportsurvey)
        _exportsurvey.exec_()
        _exportsurvey.show()


    def doExportSeisSegy(self):
        _exportsegy = QtWidgets.QDialog()
        _gui = gui_exportseissegy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportsegy)
        _exportsegy.exec_()
        _exportsegy.show()


    def doExportSeisNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportseisnpy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doExportSeisImageSet(self):
        _exportimage = QtWidgets.QDialog()
        _gui = gui_exportseisimageset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportimage)
        _exportimage.exec_()
        _exportimage.show()


    def doExportPsSeisNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportpsseisnpy()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doExportHorizonFile(self):
        _exportfile = QtWidgets.QDialog()
        _gui = gui_exporthorizonfile()
        _gui.horizondata = self.horizondata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportfile)
        _exportfile.exec_()
        _exportfile.show()


    def doExportHorizonNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exporthorizonnpy()
        _gui.horizondata = self.horizondata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doExportPointSetFile(self):
        _exportfile = QtWidgets.QDialog()
        _gui = gui_exportpointsetfile()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportfile)
        _exportfile.exec_()
        _exportfile.show()


    def doExportPointSetNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportpointsetnpy()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doQuit(self):
        self.refreshMsgBox()
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'GAEIO', 'Are you sure to quit GAEIO?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            return


    def doManageSurvey(self):
        _managesurvey = QtWidgets.QDialog()
        _gui = gui_managesurvey()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.setupGUI(_managesurvey)
        _managesurvey.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _managesurvey.show()
        #
        self.updateSurveyVis()
        self.updateSeisVis()


    def doManageSeis(self):
        _manageseis = QtWidgets.QDialog()
        _gui = gui_manageseis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_manageseis)
        _manageseis.exec()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _manageseis.show()
        #
        self.updateSeisVis()


    def doManagePsSeis(self):
        _managepsseis = QtWidgets.QDialog()
        _gui = gui_managepsseis()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_managepsseis)
        _managepsseis.exec()
        self.psseisdata = _gui.psseisdata
        _managepsseis.show()


    def doManageHorizon(self):
        _manage = QtWidgets.QDialog()
        _gui = gui_managehorizon()
        _gui.horizondata = self.horizondata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_manage)
        _manage.exec()
        self.horizondata = _gui.horizondata
        _manage.show()
        #
        self.updateHorizonVis()


    def doManagePointSet(self):
        _managepoint = QtWidgets.QDialog()
        _gui = gui_managepointset()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_managepoint)
        _managepoint.exec()
        self.pointsetdata = _gui.pointsetdata
        _managepoint.show()
        #
        self.updatePointSetVis()


    def doConvertSeis2PointSet(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertseis2pointset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointsetdata = self.pointsetdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.pointsetdata = _gui.pointsetdata
        _convert.show()
        #
        self.updatePointSetVis()


    def doConvertHorizon2PointSet(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_converthorizon2pointset()
        _gui.horizondata = self.horizondata
        _gui.pointsetdata = self.pointsetdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.pointsetdata = _gui.pointsetdata
        _convert.show()
        #
        self.updatePointSetVis()


    def doConvertPointSet2Seis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpointset2seis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointsetdata = self.pointsetdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.seisdata = _gui.seisdata
        _convert.show()
        #
        self.updateSeisVis()


    def doConvertPointSet2Horizon(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpointset2horizon()
        _gui.horizondata = self.horizondata
        _gui.pointsetdata = self.pointsetdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.horizondata = _gui.horizondata
        _convert.show()
        #
        self.updateHorizonVis()


    def doConvertSeis2PsSeis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertseis2psseis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.psseisdata = self.psseisdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.psseisdata = _gui.psseisdata
        _convert.show()


    def doConvertPsSeis2Seis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpsseis2seis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.psseisdata = self.psseisdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _convert.show()
        #
        self.updateSeisVis()


    def doCalcMathAttribSingle(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcmathattribsingle()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()
        #
        self.updateSeisVis()


    def doCalcMathAttribMultiple(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcmathattribmultiple()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()
        #
        self.updateSeisVis()


    def doCalcInstanAttrib(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcinstanattrib()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()
        #
        self.updateSeisVis()


    def doPlotVis1DSeisZ(self):
        _plot1dz = QtWidgets.QDialog()
        _gui = gui_plotvis1dseisz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.playerconfiginl = self.settings['Viewer']['Player']
        _gui.playerconfigxl = {}
        _gui.playerconfigxl['First'] = 'G'
        _gui.playerconfigxl['Previous'] = 'H'
        _gui.playerconfigxl['Backward'] = 'E'
        _gui.playerconfigxl['Pause'] = 'P'
        _gui.playerconfigxl['Forward'] = 'R'
        _gui.playerconfigxl['Next'] = 'J'
        _gui.playerconfigxl['Last'] = 'K'
        _gui.playerconfigxl['Interval'] = _gui.playerconfiginl['Interval']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot1dz)
        _plot1dz.exec()
        _plot1dz.show()


    def doPlotVis1DSeisFreq(self):
        _plot1d = QtWidgets.QDialog()
        _gui = gui_plotvis1dseisfreq()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot1d)
        _plot1d.exec()
        _plot1d.show()


    def doPlotVis2DSeisInl(self):
        _plot2dinl = QtWidgets.QDialog()
        _gui = gui_plotvis2dseisinl()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dinl)
        _plot2dinl.exec()
        _plot2dinl.show()


    def doPlotVis2DSeisXl(self):
        _plot2dxl = QtWidgets.QDialog()
        _gui = gui_plotvis2dseisxl()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dxl)
        _plot2dxl.exec()
        _plot2dxl.show()


    def doPlotVis2DSeisZ(self):
        _plot2dz = QtWidgets.QDialog()
        _gui = gui_plotvis2dseisz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dz)
        _plot2dz.exec()
        _plot2dz.show()


    def doPlotVis2DPsSeisShot(self):
        _plot2d = QtWidgets.QDialog()
        _gui = gui_plotvis2dpsseisshot()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2d)
        _plot2d.exec()
        _plot2d.show()


    def doPlotVis2DPointSetCrossplt(self):
        _cplt = QtWidgets.QDialog()
        _gui = gui_plotvis2dpointsetcrossplt()
        _gui.pointsetdata = self.pointsetdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_cplt)
        _cplt.exec()
        _cplt.show()


    def doPlotVis3DSeisInlXlZ(self):
        _plot3d = QtWidgets.QDialog()
        _gui = gui_plotvis3dseisinlxlz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.viewerconfig = self.settings['Viewer']['Viewer3D']['ViewFrom']
        _gui.viewerconfig['Home'] = self.settings['Viewer']['Viewer3D']['GoHome']
        _gui.playerconfiginl = self.settings['Viewer']['Player']
        _gui.playerconfigxl = {}
        _gui.playerconfigxl['First'] = 'G'
        _gui.playerconfigxl['Previous'] = 'H'
        _gui.playerconfigxl['Backward'] = 'E'
        _gui.playerconfigxl['Pause'] = 'P'
        _gui.playerconfigxl['Forward'] = 'R'
        _gui.playerconfigxl['Next'] = 'J'
        _gui.playerconfigxl['Last'] = 'K'
        _gui.playerconfigxl['Interval'] = _gui.playerconfiginl['Interval']
        _gui.playerconfigz = {}
        _gui.playerconfigz['First'] = 'C'
        _gui.playerconfigz['Previous'] = 'V'
        _gui.playerconfigz['Backward'] = 'T'
        _gui.playerconfigz['Pause'] = 'P'
        _gui.playerconfigz['Forward'] = 'Y'
        _gui.playerconfigz['Next'] = 'B'
        _gui.playerconfigz['Last'] = 'N'
        _gui.playerconfigz['Interval'] = _gui.playerconfiginl['Interval']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot3d)
        _plot3d.exec()
        _plot3d.show()


    def doSettingsGUI(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsgui()
        _gui.mainwindow = self
        _gui.settings = self.settings['Gui']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Gui'] = _gui.settings
        _settings.show()


    def doSettingsGeneral(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsgeneral()
        _gui.settings = self.settings['General']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['General'] = _gui.settings
        _settings.show()


    def doSettingsVisual(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsvisual()
        _gui.settings = self.settings['Visual']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Visual'] = _gui.settings
        _settings.show()


    def doSettingsViewer(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsviewer()
        _gui.settings = self.settings['Viewer']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Viewer'] = _gui.settings
        _settings.show()


    def doManual(self):
        self.refreshMsgBox()
        webbrowser.open("https://cognitivegeo.wixsite.com/gaeio/manual")


    def doSupport(self):
        webbrowser.open("https://cognitivegeo.wixsite.com/gaeio/support")


    def doAbout(self):
        _about = QtWidgets.QDialog()
        _gui = gui_about()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_about)
        _about.exec()
        _about.show()


    def setSettings(self, settings):
        _dialog = QtWidgets.QDialog()
        #
        _gui = gui_settingsgui()
        _gui.mainwindow = self
        _gui.settings = settings['Gui']
        _gui.setupGUI(_dialog)
        #
        _gui = gui_settingsgeneral()
        _gui.settings = settings['General']
        _gui.setupGUI(_dialog)
        #
        _gui = gui_settingsvisual()
        _gui.settings = settings['Visual']
        _gui.setupGUI(_dialog)
        #
        _gui = gui_settingsviewer()
        _gui.settings = settings['Viewer']
        _gui.setupGUI(_dialog)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def updateSeisVis(self):
        self.cbblistseis.clear()
        # update configuration
        _config = {}
        _all_available_seis = []
        if type(self.seisdata) is dict and len(self.seisdata.keys()) > 0:
            for _seis in sorted(self.seisdata.keys()):
                if checkSeisData(self.seisdata[_seis], self.survinfo):
                    _all_available_seis.append(_seis)
                    self.cbblistseis.addItem(_seis)
                    _config[_seis] = {}
                    if _seis in self.seisvisconfig.keys():
                        _config[_seis] = self.seisvisconfig[_seis]
                    else:
                        _config[_seis]['Colormap'] = self.settings['Visual']['Image']['Colormap']
                        _config[_seis]['Flip'] = False
                        _config[_seis]['Opacity'] = '100%'
                        _config[_seis]['Interpolation'] = self.settings['Visual']['Image']['Interpolation']
                        _config[_seis]['Maximum'] = basic_data.max(self.seisdata[_seis])
                        _config[_seis]['Minimum'] = basic_data.min(self.seisdata[_seis])
        self.seisvisconfig = _config
        # update canvas by removing non-existing seismic
        if type(self.canvascomponents) is dict and 'Seismic' in self.canvascomponents.keys() and\
                type(self.canvasproperties) is dict and 'Seismic' in self.canvasproperties.keys():
            _idx_pop = []
            for _idx in range(len(self.canvasproperties['Seismic'])):
                if self.canvasproperties['Seismic'][_idx]['Name'] not in _all_available_seis:
                    _idx_pop.append(_idx)
                else:
                    self.canvascomponents['Seismic'][_idx].parent = None
                    _visual = self.createVisualSeis(self.canvasproperties['Seismic'][_idx]['Name'],
                                                    self.canvasproperties['Seismic'][_idx]['Orientation'],
                                                    self.canvasproperties['Seismic'][_idx]['Number'])
                    if _visual is None:
                        _idx_pop.append(_idx)
                    else:
                        if self.canvasproperties['Seismic'][_idx]['Visible']:
                            _visual.parent = self.view.scene
                    self.canvascomponents['Seismic'][_idx] = _visual
            for _idx in range(len(_idx_pop)):
                self.canvasproperties['Seismic'].pop(_idx_pop[_idx] - _idx)
                if self.canvascomponents['Seismic'][_idx_pop[_idx] - _idx] is not None:
                    self.canvascomponents['Seismic'][_idx_pop[_idx] - _idx].parent = None
                self.canvascomponents['Seismic'].pop(_idx_pop[_idx] - _idx)
        else:
            self.canvasproperties['Seismic'] = []
            self.canvascomponents['Seismic'] = []
        #
        self.updateTwgSeisOnCanvas()


    def updateHorizonVis(self):
        self.cbblisthorizon.clear()
        #
        # save all existing properties
        _all_existing_property = {}
        if type(self.horizonvisconfig) is dict:
            for _hrz in self.horizonvisconfig.keys():
                for _prop in self.horizonvisconfig[_hrz]['Property'].keys():
                    _all_existing_property[_prop] = self.horizonvisconfig[_hrz]['Property'][_prop]
        #
        # update configuration
        _config = {}
        _all_available_horizon = []
        if type(self.horizondata) is dict and len(self.horizondata.keys()) > 0:
            for _hrz in sorted(self.horizondata.keys()):
                if checkHorizonData(self.horizondata[_hrz]):
                    self.cbblisthorizon.addItem(_hrz)
                    _all_available_horizon.append(_hrz)
                    _config[_hrz] = {}
                    if type(self.horizonvisconfig) is dict and _hrz in self.horizonvisconfig.keys():
                        _config[_hrz] = self.horizonvisconfig[_hrz]
                    else:
                        _config[_hrz]['Color'] = self.settings['Visual']['Line']['Color']
                        _config[_hrz]['Opacity'] = '100%'
                    # reset property
                    _config[_hrz]['Property'] = {}
                    for _prop in self.horizondata[_hrz]['HorizonData'].keys():
                        if _prop in _all_existing_property.keys():
                            _d = _all_existing_property[_prop]
                        else:
                            _d = {}
                            _d['Colormap'] = 'Frequency'
                            _d['Flip'] = False
                            _data = np.reshape(self.horizondata[_hrz]['HorizonData'][_prop], [-1])
                            # remove nan
                            _data = _data[~np.isnan(_data)]
                            _d['Maximum'] = basic_data.max(_data)
                            _d['Minimum'] = basic_data.min(_data)
                        _config[_hrz]['Property'][_prop] = _d
        self.horizonvisconfig = _config
        # update canvas by removing non-existing horizon and upating existing horizon
        if type(self.canvascomponents) is dict and 'Horizon' in self.canvascomponents.keys() and \
                type(self.canvasproperties) is dict and 'Horizon' in self.canvasproperties.keys():
            _idx_pop = []
            for _idx in range(len(self.canvasproperties['Horizon'])):
                if self.canvasproperties['Horizon'][_idx]['Name'] not in _all_available_horizon:
                    _idx_pop.append(_idx)
                else:
                    self.canvascomponents['Horizon'][_idx].parent = None
                    _visual = self.createVisualHorizon(self.canvasproperties['Horizon'][_idx]['Name'],
                                                       self.canvasproperties['Horizon'][_idx]['Property'])
                    if _visual is None:
                        _idx_pop.append(_idx)
                    else:
                        if self.canvasproperties['Horizon'][_idx]['Visible']:
                            _visual.parent = self.view.scene
                    self.canvascomponents['Horizon'][_idx] = _visual
            for _idx in range(len(_idx_pop)):
                self.canvasproperties['Horizon'].pop(_idx_pop[_idx] - _idx)
                if self.canvascomponents['Horizon'][_idx_pop[_idx] - _idx] is not None:
                    self.canvascomponents['Horizon'][_idx_pop[_idx] - _idx].parent = None
                self.canvascomponents['Horizon'].pop(_idx_pop[_idx] - _idx)
        else:
            self.canvasproperties['Horizon'] = []
            self.canvascomponents['Horizon'] = []
        #
        self.updateTwgHorizonOnCanvas()


    def updatePointSetVis(self):
        self.cbblistpointset.clear()
        # update configuration
        _config = {}
        _all_available_pointset = []
        if type(self.pointsetdata) is dict and len(self.pointsetdata.keys()) > 0:
            for _point in sorted(self.pointsetdata.keys()):
                if checkPointSetData(self.pointsetdata[_point]):
                    self.cbblistpointset.addItem(_point)
                    _all_available_pointset.append(_point)
                    _config[_point] = {}
                    if _point in self.pointsetvisconfig.keys():
                        _config[_point] = self.pointsetvisconfig[_point]
                    else:
                        _config[_point]['Marker'] = '+'  # self.settings['Visual']['Line']['MarkerStyle']
                        _config[_point]['Color'] = self.settings['Visual']['Line']['Color']
                        _config[_point]['Size'] = self.settings['Visual']['Line']['MarkerSize']
        self.pointsetvisconfig = _config
        # update canvas by removing non-existing pointset and upating existing pointset
        if type(self.canvascomponents) is dict and 'PointSet' in self.canvascomponents.keys() and \
                type(self.canvasproperties) is dict and 'PointSet' in self.canvasproperties.keys():
            _idx_pop = []
            for _idx in range(len(self.canvasproperties['PointSet'])):
                if self.canvasproperties['PointSet'][_idx]['Name'] not in _all_available_pointset:
                    _idx_pop.append(_idx)
                else:
                    self.canvascomponents['PointSet'][_idx].parent = None
                    _visual = self.createVisualPointSet(self.canvasproperties['PointSet'][_idx]['Name'])
                    if _visual is None:
                        _idx_pop.append(_idx)
                    else:
                        if self.canvasproperties['PointSet'][_idx]['Visible']:
                            _visual.parent = self.view.scene
                    self.canvascomponents['PointSet'][_idx] = _visual
            for _idx in range(len(_idx_pop)):
                self.canvasproperties['PointSet'].pop(_idx_pop[_idx] - _idx)
                if self.canvascomponents['PointSet'][_idx_pop[_idx] - _idx] is not None:
                    self.canvascomponents['PointSet'][_idx_pop[_idx] - _idx].parent = None
                self.canvascomponents['PointSet'].pop(_idx_pop[_idx] - _idx)
        else:
            self.canvasproperties['PointSet'] = []
            self.canvascomponents['PointSet'] = []
        #
        self.updateTwgPointSetOnCanvas()


    def updateSurveyVis(self):
        #
        if self.canvas is None:
            self.canvas = scene.SceneCanvas(keys='interactive', title='Canvas', bgcolor=[0.5, 0.5, 0.5],
                                            size=(1130, 850), app='pyqt5', parent=self.wgtcanvas)
        if self.view is None:
            self.view = self.canvas.central_widget.add_view()
            self.view.camera = scene.TurntableCamera(elevation=30, azimuth=135)
        #
        # survey box
        if 'Survey_Box' in self.canvascomponents.keys():
            for _i in self.canvascomponents['Survey_Box']:
                _i.parent = None
        if 'Survey_Box' not in self.canvasproperties.keys():
            self.canvasproperties['Survey_Box'] = True
        self.canvascomponents['Survey_Box'] = self.createVisualSrvBox()
        if len(self.canvascomponents['Survey_Box']) == 12:
            for _i in self.canvascomponents['Survey_Box']:
                if self.canvasproperties['Survey_Box'] is True:
                    _i.parent = self.view.scene
                else:
                    _i.parent = None
        else:
            self.canvasproperties['Survey_Box'] = True
        #
        # xyz axis
        if 'XYZ_Axis' in self.canvascomponents.keys() and self.canvascomponents['XYZ_Axis'] is not None:
            self.canvascomponents['XYZ_Axis'].parent = None
        if 'XYZ_Axis' not in self.canvasproperties.keys():
            self.canvasproperties['XYZ_Axis'] = True
        self.canvascomponents['XYZ_Axis'] = self.createVisualXYZAxis()
        if self.canvascomponents['XYZ_Axis'] is not None:
            if self.canvasproperties['XYZ_Axis'] is True:
                self.canvascomponents['XYZ_Axis'].parent = self.view.scene
            else:
                self.canvascomponents['XYZ_Axis'].parent = None
        else:
            self.canvasproperties['XYZ_Axis'] = True
        #
        # z scale
        if 'Z_Scale' not in self.canvasproperties.keys():
            self.ldtzscale.setText('1.0')
        _zscale = basic_data.str2float(self.ldtzscale.text())
        if _zscale is not False and _zscale > 0.0:
            if 'Z_Scale' not in self.canvasproperties.keys():
                self.canvasproperties['Z_Scale'] = _zscale
        #
        # set camara range and angle
        self.setCameraRange()
        self.view.camera.elevation = 30
        self.view.camera.azimuth = 135
        #
        self.canvas.show()


    def clickBtnConfigSeisVis(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configseisvis()
        _gui.seisvisconfig = self.seisvisconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.seisvisconfig = _gui.seisvisconfig
        _config.show()
        #
        # update seismic
        for _i in range(len(self.canvascomponents['Seismic'])):
            self.canvascomponents['Seismic'][_i].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][_i]['Name'],
                                         self.canvasproperties['Seismic'][_i]['Orientation'],
                                         self.canvasproperties['Seismic'][_i]['Number'])
            if self.canvasproperties['Seismic'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][_i] = _vis


    def clickBtnAddSeis2Canvas(self):
        _all_seis = []
        for _seis in sorted(self.seisdata.keys()):
            if checkSeisData(self.seisdata[_seis], self.survinfo):
                _all_seis.append(_seis)
        if len(_all_seis) > 0 and \
                checkSeisData(self.seisdata[_all_seis[self.cbblistseis.currentIndex()]],
                              self.survinfo):
            ##### property
            _seis = {}
            _seis['Visible'] = False
            _seis['Name'] = _all_seis[self.cbblistseis.currentIndex()]
            _seis['Orientation'] = 'Inline'
            _seis['Number'] = self.survinfo['ILStart']
            _seis['Remove'] = False
            #
            self.canvasproperties['Seismic'].append(_seis)
            #
            _nseis = len(self.canvasproperties['Seismic'])
            # add one more row
            self.twgseisoncanvas.setRowCount(_nseis)
            # visible
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_seis['Visible'])
            _item.stateChanged.connect(partial(self.changeCbxVisSeisOnCanvas, idx=_nseis - 1))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 0, _item)
            # name
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_seis['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.twgseisoncanvas.setItem(_nseis - 1, 1, _item)
            # orientation
            _item = QtWidgets.QComboBox()
            _item.addItems(['Inline', 'Xline', 'Z'])
            _item.setCurrentIndex(list.index(['Inline', 'Crossline', 'Z'], _seis['Orientation']))
            _item.currentIndexChanged.connect(partial(self.changeCbbOrtSeisOnCanvas, idx=_nseis - 1))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 2, _item)
            # number
            _item = QtWidgets.QComboBox()
            _slices = []
            if _seis['Orientation'] == 'Inline':
                _slices = [str(_no) for _no in self.survinfo['ILRange']]
            if _seis['Orientation'] == 'Crossline':
                _slices = [str(_no) for _no in self.survinfo['XLRange']]
            if _seis['Orientation'] == 'Z':
                _slices = [str(_no) for _no in self.survinfo['ZRange']]
            _item.addItems(_slices)
            _item.setCurrentIndex(list.index(_slices, str(_seis['Number'])))
            _item.currentIndexChanged.connect(partial(self.changeCbbNoSeisOnCanvas, idx=_nseis - 1))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 3, _item)
            # remove
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/no.png")),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial(self.clickBtnRmSeisOnCanvas, idx=_nseis - 1))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 4, _item)
            #
            ### component
            _vis = self.createVisualSeis(_seis['Name'], _seis['Orientation'], _seis['Number'])
            if _seis['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'].append(_vis)


    def changeCbxVisSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
           self.canvasproperties['Seismic'][idx]['Visible'] = self.twgseisoncanvas.cellWidget(idx, 0).isChecked()
           #
           if self.twgseisoncanvas.cellWidget(idx, 0).isChecked():
               self.canvascomponents['Seismic'][idx].parent = self.view.scene
           else:
               self.canvascomponents['Seismic'][idx].parent = None
           #
           # print(idx)
           # print(self.canvasproperties['Seismic'][idx])


    def changeCbbOrtSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            self.twgseisoncanvas.cellWidget(idx, 3).clear()
            _ort = ""
            _no = 0
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 0:
                self.twgseisoncanvas.cellWidget(idx, 3).addItems([str(_no) for _no in self.survinfo['ILRange']])
                self.twgseisoncanvas.cellWidget(idx, 3).setCurrentIndex(0)
                _ort = 'Inline'
                _no = self.survinfo['ILRange'][0]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 1:
                self.twgseisoncanvas.cellWidget(idx, 3).addItems([str(_no) for _no in self.survinfo['XLRange']])
                self.twgseisoncanvas.cellWidget(idx, 3).setCurrentIndex(0)
                _ort = 'Crossline'
                _no = self.survinfo['XLRange'][0]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 2:
                self.twgseisoncanvas.cellWidget(idx, 3).addItems([str(_no) for _no in self.survinfo['ZRange']])
                self.twgseisoncanvas.cellWidget(idx, 3).setCurrentIndex(0)
                _ort = 'Z'
                _no = self.survinfo['ZRange'][0]
            #
            self.canvasproperties['Seismic'][idx]['Orientation'] = _ort
            self.canvasproperties['Seismic'][idx]['Number'] = _no
            #
            self.canvascomponents['Seismic'][idx].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][idx]['Name'], _ort, _no)
            if self.canvasproperties['Seismic'][idx]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][idx] = _vis


    def changeCbbNoSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            _no = 0
            _ort = ''
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 0:
                _ort = 'Inline'
                _no = self.survinfo['ILRange'][self.twgseisoncanvas.cellWidget(idx, 3).currentIndex()]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 1:
                _ort = 'Crossline'
                _no = self.survinfo['XLRange'][self.twgseisoncanvas.cellWidget(idx, 3).currentIndex()]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 2:
                _ort = 'Z'
                _no = self.survinfo['ZRange'][self.twgseisoncanvas.cellWidget(idx, 3).currentIndex()]
            #
            self.canvasproperties['Seismic'][idx]['Number'] = _no
            #
            self.canvascomponents['Seismic'][idx].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][idx]['Name'], _ort, _no)
            if self.canvasproperties['Seismic'][idx]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][idx] = _vis


    def clickBtnRmSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            self.canvasproperties['Seismic'].pop(idx)
            self.canvascomponents['Seismic'][idx].parent = None
            self.canvascomponents['Seismic'].pop(idx)
            self.updateTwgSeisOnCanvas()


    def updateTwgSeisOnCanvas(self):
        self.twgseisoncanvas.clear()
        #
        _seis = self.canvasproperties['Seismic']
        #
        self.twgseisoncanvas.setRowCount(len(_seis))
        for _i in range(len(_seis)):
            # visible
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_seis[_i]['Visible'])
            _item.stateChanged.connect(partial(self.changeCbxVisSeisOnCanvas, idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 0, _item)
            # name
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_seis[_i]['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.twgseisoncanvas.setItem(_i, 1, _item)
            # orientation
            _item = QtWidgets.QComboBox()
            _item.addItems(['Inline', 'Xline', 'Z'])
            _item.setCurrentIndex(list.index(['Inline', 'Crossline', 'Z'], _seis[_i]['Orientation']))
            _item.currentIndexChanged.connect(partial(self.changeCbbOrtSeisOnCanvas, idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 2, _item)
            # number
            _item = QtWidgets.QComboBox()
            _slices = []
            if _seis[_i]['Orientation'] == 'Inline':
                _slices = [str(_no) for _no in self.survinfo['ILRange']]
            if _seis[_i]['Orientation'] == 'Crossline':
                _slices = [str(_no) for _no in self.survinfo['XLRange']]
            if _seis[_i]['Orientation'] == 'Z':
                _slices = [str(_no) for _no in self.survinfo['ZRange']]
            _item.addItems(_slices)
            _item.setCurrentIndex(list.index(_slices, str(_seis[_i]['Number'])))
            _item.currentIndexChanged.connect(partial(self.changeCbbNoSeisOnCanvas, idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 3, _item)
            # remove
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/no.png")),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial(self.clickBtnRmSeisOnCanvas, idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 4, _item)


    def clickBtnConfigHorizonVis(self):
        _config = QtWidgets.QDialog()
        _gui = gui_confighorizonvis()
        _gui.horizonvisconfig = self.horizonvisconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.horizonvisconfig = _gui.horizonvisconfig
        _config.show()
        #
        # update horizon
        for _i in range(len(self.canvascomponents['Horizon'])):
            self.canvascomponents['Horizon'][_i].parent = None
            _vis = self.createVisualHorizon(self.canvasproperties['Horizon'][_i]['Name'],
                                            self.canvasproperties['Horizon'][_i]['Property'])
            if self.canvasproperties['Horizon'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Horizon'][_i] = _vis
    
    
    def clickBtnAddHorizon2Canvas(self):
        _all_horizon = []
        for _horizon in sorted(self.horizondata.keys()):
            if checkHorizonData(self.horizondata[_horizon]):
                _all_horizon.append(_horizon)
        if len(_all_horizon) > 0 and \
                checkHorizonData(self.horizondata[_all_horizon[self.cbblisthorizon.currentIndex()]]):
            ##### property
            _horizon = {}
            _horizon['Visible'] = False
            _horizon['Name'] = _all_horizon[self.cbblisthorizon.currentIndex()]
            _horizon['Property'] = '---'
            _horizon['Remove'] = False
            #
            self.canvasproperties['Horizon'].append(_horizon)
            #
            _nhorizon = len(self.canvasproperties['Horizon'])
            # add one more row
            self.twghorizononcanvas.setRowCount(_nhorizon)
            # visible
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_horizon['Visible'])
            _item.stateChanged.connect(partial(self.changeCbxVisHorizonOnCanvas, idx=_nhorizon - 1))
            self.twghorizononcanvas.setCellWidget(_nhorizon - 1, 0, _item)
            # name
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_horizon['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.twghorizononcanvas.setItem(_nhorizon - 1, 1, _item)
            # property
            _all_property = list(sorted(self.horizondata[_horizon['Name']]['HorizonData'].keys()))
            # add one additional
            _all_property.insert(0, '---')
            _item = QtWidgets.QComboBox()
            _item.addItems(_all_property)
            _item.setCurrentIndex(list.index(_all_property, _horizon['Property']))
            _item.currentIndexChanged.connect(partial(self.changeCbbPropHorizonOnCanvas, idx=_nhorizon - 1))
            self.twghorizononcanvas.setCellWidget(_nhorizon - 1, 2, _item)
            # remove
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/no.png")),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial(self.clickBtnRmHorizonOnCanvas, idx=_nhorizon - 1))
            self.twghorizononcanvas.setCellWidget(_nhorizon - 1, 3, _item)
            #
            ### component
            _vis = self.createVisualHorizon(_horizon['Name'], _horizon['Property'])
            if _horizon['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Horizon'].append(_vis)


    def changeCbxVisHorizonOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Horizon']):
           self.canvasproperties['Horizon'][idx]['Visible'] = self.twghorizononcanvas.cellWidget(idx, 0).isChecked()
           #
           if self.twghorizononcanvas.cellWidget(idx, 0).isChecked():
               self.canvascomponents['Horizon'][idx].parent = self.view.scene
           else:
               self.canvascomponents['Horizon'][idx].parent = None


    def changeCbbPropHorizonOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Horizon']):
            _horizon = self.canvasproperties['Horizon'][idx]['Name']
            _all_property = list(sorted(self.horizondata[_horizon]['HorizonData'].keys()))
            # add one additional
            _all_property.insert(0, '---')
            #
            self.canvasproperties['Horizon'][idx]['Property'] = \
                _all_property[self.twghorizononcanvas.cellWidget(idx, 2).currentIndex()]
            #
            self.canvascomponents['Horizon'][idx].parent = None
            _vis = self.createVisualHorizon(self.canvasproperties['Horizon'][idx]['Name'],
                                            self.canvasproperties['Horizon'][idx]['Property'])
            if self.canvasproperties['Horizon'][idx]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Horizon'][idx] = _vis


    def clickBtnRmHorizonOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Horizon']):
            self.canvasproperties['Horizon'].pop(idx)
            self.canvascomponents['Horizon'][idx].parent = None
            self.canvascomponents['Horizon'].pop(idx)
            self.updateTwgHorizonOnCanvas()


    def updateTwgHorizonOnCanvas(self):
        self.twghorizononcanvas.clear()
        #
        _horizon = self.canvasproperties['Horizon']
        #
        self.twghorizononcanvas.setRowCount(len(_horizon))
        for _i in range(len(_horizon)):
            # visible
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_horizon[_i]['Visible'])
            _item.stateChanged.connect(partial(self.changeCbxVisHorizonOnCanvas, idx=_i))
            self.twghorizononcanvas.setCellWidget(_i, 0, _item)
            # name
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_horizon[_i]['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.twghorizononcanvas.setItem(_i, 1, _item)
            # property
            _all_property = list(sorted(self.horizondata[_horizon[_i]['Name']]['HorizonData'].keys()))
            # add one additional
            _all_property.insert(0, '---')
            _item = QtWidgets.QComboBox()
            _item.addItems(_all_property)
            _item.setCurrentIndex(list.index(_all_property, _horizon[_i]['Property']))
            _item.currentIndexChanged.connect(partial(self.changeCbbPropHorizonOnCanvas, idx=_i))
            self.twghorizononcanvas.setCellWidget(_i, 2, _item)
            # remove
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/no.png")),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial(self.clickBtnRmHorizonOnCanvas, idx=_i))
            self.twghorizononcanvas.setCellWidget(_i, 3, _item)


    def clickBtnConfigPointSetVis(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configpointsetvis()
        _gui.pointsetvisconfig = self.pointsetvisconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.pointsetvisconfig = _gui.pointsetvisconfig
        _config.show()
        #
        # update pointset
        for _i in range(len(self.canvascomponents['PointSet'])):
            self.canvascomponents['PointSet'][_i].parent = None
            _vis = self.createVisualPointSet(self.canvasproperties['PointSet'][_i]['Name'])
            if self.canvasproperties['PointSet'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['PointSet'][_i] = _vis


    def clickBtnAddPointSet2Canvas(self):
        _all_pointset = []
        for _point in sorted(self.pointsetdata.keys()):
            if checkPointSetData(self.pointsetdata[_point]):
                _all_pointset.append(_point)
        if len(_all_pointset) > 0 and \
                checkPointSetData(self.pointsetdata[_all_pointset[self.cbblistpointset.currentIndex()]]):
            ##### property
            _point = {}
            _point['Visible'] = False
            _point['Name'] = _all_pointset[self.cbblistpointset.currentIndex()]
            _point['Property'] = '---'
            _point['Remove'] = False
            #
            self.canvasproperties['PointSet'].append(_point)
            #
            _npoint = len(self.canvasproperties['PointSet'])
            # add one more row
            self.twgpointsetoncanvas.setRowCount(_npoint)
            # visible
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_point['Visible'])
            _item.stateChanged.connect(partial(self.changeCbxVisPointSetOnCanvas, idx=_npoint - 1))
            self.twgpointsetoncanvas.setCellWidget(_npoint - 1, 0, _item)
            # name
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_point['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.twgpointsetoncanvas.setItem(_npoint - 1, 1, _item)
            # property
            _all_property = list(sorted(self.pointsetdata[_point['Name']].keys()))
            # add one additional
            _all_property.insert(0, '---')
            _item = QtWidgets.QComboBox()
            _item.addItems(_all_property)
            _item.setCurrentIndex(list.index(_all_property, _point['Property']))
            _item.setEnabled(False)
            _item.currentIndexChanged.connect(partial(self.changeCbbPropPointSetOnCanvas, idx=_npoint - 1))
            self.twgpointsetoncanvas.setCellWidget(_npoint - 1, 2, _item)
            # remove
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/no.png")),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial(self.clickBtnRmPointSetOnCanvas, idx=_npoint - 1))
            self.twgpointsetoncanvas.setCellWidget(_npoint - 1, 3, _item)
            #
            ### component
            _vis = self.createVisualPointSet(_point['Name'])
            if _point['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['PointSet'].append(_vis)


    def changeCbxVisPointSetOnCanvas(self, idx):
        if idx < len(self.canvasproperties['PointSet']):
           self.canvasproperties['PointSet'][idx]['Visible'] = self.twgpointsetoncanvas.cellWidget(idx, 0).isChecked()
           #
           if self.twgpointsetoncanvas.cellWidget(idx, 0).isChecked():
               self.canvascomponents['PointSet'][idx].parent = self.view.scene
           else:
               self.canvascomponents['PointSet'][idx].parent = None

    def changeCbbPropPointSetOnCanvas(self, idx):
        print('Not used yet')


    def clickBtnRmPointSetOnCanvas(self, idx):
        if idx < len(self.canvasproperties['PointSet']):
            self.canvasproperties['PointSet'].pop(idx)
            self.canvascomponents['PointSet'][idx].parent = None
            self.canvascomponents['PointSet'].pop(idx)
            self.updateTwgPointSetOnCanvas()


    def updateTwgPointSetOnCanvas(self):
        self.twgpointsetoncanvas.clear()
        #
        _point = self.canvasproperties['PointSet']
        #
        self.twgpointsetoncanvas.setRowCount(len(_point))
        for _i in range(len(_point)):
            # visible
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_point[_i]['Visible'])
            _item.stateChanged.connect(partial(self.changeCbxVisPointSetOnCanvas, idx=_i))
            self.twgpointsetoncanvas.setCellWidget(_i, 0, _item)
            # name
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_point[_i]['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.twgpointsetoncanvas.setItem(_i, 1, _item)
            # property
            _all_property = list(sorted(self.pointsetdata[_point[_i]['Name']].keys()))
            # add one additional
            _all_property.insert(0, '---')
            _item = QtWidgets.QComboBox()
            _item.addItems(_all_property)
            _item.setCurrentIndex(list.index(_all_property,
                                             _point[_i]['Property']))
            _item.setEnabled(False)
            _item.currentIndexChanged.connect(partial(self.changeCbbPropPointSetOnCanvas, idx=_i))
            self.twgpointsetoncanvas.setCellWidget(_i, 2, _item)
            # remove
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/no.png")),
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial(self.clickBtnRmPointSetOnCanvas, idx=_i))
            self.twgpointsetoncanvas.setCellWidget(_i, 3, _item)

    def clickBtnSrvBox(self):
        if len(self.canvascomponents['Survey_Box']) == 12:
            if self.canvasproperties['Survey_Box'] is True:
                for _i in self.canvascomponents['Survey_Box']:
                    _i.parent = None
                self.canvasproperties['Survey_Box'] = False
            else:
                for _i in self.canvascomponents['Survey_Box']:
                    _i.parent = self.view.scene
                self.canvasproperties['Survey_Box'] = True


    def clickBtnXYZAxis(self):
        if self.canvascomponents['XYZ_Axis'] is not None:
            if self.canvasproperties['XYZ_Axis'] is True:
                self.canvascomponents['XYZ_Axis'].parent = None
                self.canvasproperties['XYZ_Axis'] = False
            else:
                self.canvascomponents['XYZ_Axis'].parent = self.view.scene
                self.canvasproperties['XYZ_Axis'] = True


    def clickBtnSnapshot(self):
        res = self.canvas.render()[:, :, 0:3]
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save canvas', self.settings['General']['RootPath'],
                                        filter="Portable Network Graphic file (PNG) (*.PNG);;All files (*.*)")
        if len(_file[0]) > 0:
            vispy_io.write_png(_file[0], res)


    def clickBtnGoHome(self):
        self.setCameraRange()
        self.view.camera.elevation = 30
        self.view.camera.azimuth = 135


    def changeCbbViewFrom(self):
        if self.cbbviewfrom.currentIndex() == 0:
            self.view.camera.elevation = 0
            self.view.camera.azimuth = 0
        if self.cbbviewfrom.currentIndex() == 1:
            self.view.camera.elevation = 0
            self.view.camera.azimuth = 90
        if self.cbbviewfrom.currentIndex() == 2:
            self.view.camera.elevation = 90
            self.view.camera.azimuth = 0


    def changeLdtZScale(self):
        #
        _zscale = basic_data.str2float(self.ldtzscale.text())
        if _zscale is not False and _zscale > 0.0:
            self.canvasproperties['Z_Scale'] = _zscale
        # update seismic
        if type(self.canvascomponents) is dict and 'Seismic' in self.canvascomponents.keys() and \
                type(self.canvasproperties) is dict and 'Seismic' in self.canvasproperties.keys():
            for _i in range(len(self.canvascomponents['Seismic'])):
                self.canvascomponents['Seismic'][_i].parent = None
                _vis = self.createVisualSeis(self.canvasproperties['Seismic'][_i]['Name'],
                                             self.canvasproperties['Seismic'][_i]['Orientation'],
                                             self.canvasproperties['Seismic'][_i]['Number'])
                if self.canvasproperties['Seismic'][_i]['Visible']:
                    _vis.parent = self.view.scene
                self.canvascomponents['Seismic'][_i] = _vis
        #
        # update horizon
        if type(self.canvascomponents) is dict and 'Horizon' in self.canvascomponents.keys() and \
                type(self.canvasproperties) is dict and 'Horizon' in self.canvasproperties.keys():
            for _i in range(len(self.canvascomponents['Horizon'])):
                self.canvascomponents['Horizon'][_i].parent = None
                _vis = self.createVisualHorizon(self.canvasproperties['Horizon'][_i]['Name'],
                                                self.canvasproperties['Horizon'][_i]['Property'])
                if self.canvasproperties['Horizon'][_i]['Visible']:
                    _vis.parent = self.view.scene
                self.canvascomponents['Horizon'][_i] = _vis
        #
        # update pointset
        if type(self.canvascomponents) is dict and 'PointSet' in self.canvascomponents.keys() and \
                type(self.canvasproperties) is dict and 'PointSet' in self.canvasproperties.keys():
            for _i in range(len(self.canvascomponents['PointSet'])):
                self.canvascomponents['PointSet'][_i].parent = None
                _vis = self.createVisualPointSet(self.canvasproperties['PointSet'][_i]['Name'])
                if self.canvasproperties['PointSet'][_i]['Visible']:
                    _vis.parent = self.view.scene
                self.canvascomponents['PointSet'][_i] = _vis
        #
        # update survey box
        _srvbox = self.createVisualSrvBox()
        if len(_srvbox) == 12:
            # remove old one
            if type(self.canvascomponents) is dict and 'Survey_Box' in self.canvascomponents.keys():
                for _i in self.canvascomponents['Survey_Box']:
                    _i.parent = None
            if type(self.canvasproperties) is dict and 'Survey_Box' not in self.canvasproperties.keys():
                self.canvasproperties['Survey_Box'] = True
            # plot new one
            self.canvascomponents['Survey_Box'] = _srvbox
            for _i in self.canvascomponents['Survey_Box']:
                if self.canvasproperties['Survey_Box'] is True:
                    _i.parent = self.view.scene
                else:
                    _i.parent = None
        #
        # update xyz axis
        _xyzaxis = self.createVisualXYZAxis()
        if _xyzaxis is not None:
            # remove old one
            if type(self.canvascomponents) is dict and 'XYZ_Axis' in self.canvascomponents.keys():
                self.canvascomponents['XYZ_Axis'].parent = None
            if type(self.canvasproperties) is dict and 'XYZ_Axis' not in self.canvasproperties.keys():
                self.canvasproperties['XYZ_Axis'] = True
            # plot new one
            self.canvascomponents['XYZ_Axis'] = _xyzaxis
            if self.canvasproperties['XYZ_Axis'] is True:
                self.canvascomponents['XYZ_Axis'].parent = self.view.scene
            else:
                self.canvascomponents['XYZ_Axis'].parent = None
        #
        # set camara range
        self.setCameraRange()


    def createVisualSeis(self, seis, ort, no):
        if checkSurvInfo(self.survinfo) is False:
            return None
        if type(self.seisdata) is not dict or seis not in self.seisdata.keys():
            return None
        if checkSeisData(self.seisdata[seis], self.survinfo) is False:
            return None
        if ort != 'Inline' and ort != 'Crossline' and ort != 'Z':
            return None
        #
        _xlstart = self.survinfo['XLStart']
        _xlend = self.survinfo['XLEnd']
        _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
        _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
        _inlstart = self.survinfo['ILStart']
        _inlend = self.survinfo['ILEnd']
        _inlstep = self.survinfo['ILStep']
        _inlnum = self.survinfo['ILNum']
        if _inlnum == 1:
            _inlstep = 1
        _xlstep = self.survinfo['XLStep']
        _xlnum = self.survinfo['XLNum']
        if _xlnum == 1:
            _xlstep = 1
        _zstep = self.survinfo['ZStep'] * self.canvasproperties['Z_Scale']
        _znum = self.survinfo['ZNum']
        if _znum == 1:
            _zstep = 1
        #
        _inlrange = self.survinfo['ILRange']
        _xlrange = self.survinfo['XLRange']
        _zrange = self.survinfo['ZRange'] * self.canvasproperties['Z_Scale']
        #
        if ort == 'Z':
            no = no * self.canvasproperties['Z_Scale']
        #
        if ort == 'Inline' and (no not in _inlrange):
            return None
        if ort == 'Crossline' and (no not in _xlrange):
             return None
        if ort == 'Z' and (no not in _zrange):
            return None
        #
        _data = np.zeros([2, 2])
        _cmp = vis_cmap.makeColorMap(cmapname=self.seisvisconfig[seis]['Colormap'],
                                     flip=self.seisvisconfig[seis]['Flip'],
                                     opacity=self.seisvisconfig[seis]['Opacity'])
        _cmp = Colormap(_cmp.colors)
        _interp = self.seisvisconfig[seis]['Interpolation'].lower()
        if _interp is None or _interp == 'None' or _interp == 'none':
            _interp = 'nearest'
        _vis = scene.visuals.Image(_data, parent=None, cmap=_cmp,
                                   clim=(self.seisvisconfig[seis]['Minimum'], self.seisvisconfig[seis]['Maximum']),
                                   interpolation=_interp)
        _tr = scene.transforms.MatrixTransform()
        if ort == 'Inline':
            _idx = np.round((no - _inlstart) / _inlstep).astype(np.int32)
            _data = self.seisdata[seis][:, :, _idx]
            _tr.scale((abs(_xlstep), abs(_zstep)))
            _tr.rotate(-90, (1, 0, 0))
            _tr.translate((_xlstart, no, _zstart))
            _tr.translate((-0.5 * _xlstep, 0, -0.5 * _zstep))
        if ort == 'Crossline':
            _idx = np.round((no - _xlstart) / _xlstep).astype(np.int32)
            _data = self.seisdata[seis][:, _idx, :]
            _tr.scale((abs(_inlstep), abs(_zstep)))
            _tr.rotate(-90, (1, 0, 0))
            _tr.rotate(90, (0, 0, 1))
            _tr.translate((no, _inlstart, _zstart))
            _tr.translate((0, -0.5*_inlstep, -0.5*_zstep))
        if ort == 'Z':
            _idx = np.round((no - _zstart) / _zstep).astype(np.int32)
            _data = self.seisdata[seis][_idx, :, :]
            _tr.scale((abs(_inlstep), abs(_xlstep)))
            _tr.rotate(90, (0, 0, 1))
            _tr.rotate(180, (0, 1, 0))
            _tr.translate((_xlstart, _inlstart, no))
            _tr.translate((-0.5*_xlstep, -0.5*_inlstep, 0))
        _vis.set_data(_data)
        _vis.transform = _tr
        #
        return _vis


    def createVisualHorizon(self, horizon, property):
        if type(self.horizondata) is not dict or horizon not in self.horizondata.keys():
            return None
        if checkHorizonData(self.horizondata[horizon]) is False:
            return None
        if property != '---' and property not in self.horizondata[horizon]['HorizonData'].keys():
            return None
        if property != '---' and property not in self.horizonvisconfig[horizon]['Property'].keys():
            return None
        #
        _x = self.horizondata[horizon]['HorizonInfo']['XLRange']
        _y = self.horizondata[horizon]['HorizonInfo']['ILRange']
        _z = self.horizondata[horizon]['HorizonData']['Z']
        _z = np.transpose(_z, [1, 0])
        #
        # apply z scale
        _z *= self.canvasproperties['Z_Scale']
        #
        # set color
        # color map matrix
        _cmap = vis_cmap.makeColorMap(cmapname='Seismic', flip=False,
                                      opacity=self.horizonvisconfig[horizon]['Opacity'],
                                      return_array=True)
        _vmin = basic_data.min(_z)
        _vmax = basic_data.max(_z)
        _values = _z
        if property == '---':
            # (constant)
            _color_selected = mplt_color.to_rgb(self.horizonvisconfig[horizon]['Color'].lower())
            _cmap[:, 0] = 0.0 * _cmap[:, 0] + _color_selected[0]
            _cmap[:, 1] = 0.0 * _cmap[:, 1] + _color_selected[1]
            _cmap[:, 2] = 0.0 * _cmap[:, 2] + _color_selected[2]
        else:
            _cmap = vis_cmap.makeColorMap(cmapname=self.horizonvisconfig[horizon]['Property'][property]['Colormap'],
                                          flip=self.horizonvisconfig[horizon]['Property'][property]['Flip'],
                                          opacity=self.horizonvisconfig[horizon]['Opacity'],
                                          return_array=True)
            _vmin = self.horizonvisconfig[horizon]['Property'][property]['Minimum']
            _vmax = self.horizonvisconfig[horizon]['Property'][property]['Maximum']
            _values = self.horizondata[horizon]['HorizonData'][property]
            _values = np.transpose(_values, [1, 0])
        #
        # apply colormap matrix
        _c = vis_cmap.applyColorMap(values=np.reshape(_values, [-1]), cmapmat=_cmap,
                                    vmin=_vmin, vmax=_vmax)
        #
        _c = _c.flatten().tolist()
        _c = list(map(lambda a, b, c, d:(a, b, c, d), _c[0::4], _c[1::4], _c[2::4], _c[3::4]))
        #
        _vis = scene.visuals.SurfacePlot(colors=_c)
        _vis.set_data(x=_x, y=_y, z=_z)
        _vis.mesh_data.set_vertex_colors(_c)
        # _vis.transform = scene.transforms.MatrixTransform()
        #
        return _vis


    def createVisualPointSet(self, point):
        if type(self.pointsetdata) is not dict or point not in self.pointsetdata.keys():
            return None
        if checkPointSetData(self.pointsetdata[point]) is False:
            return None
        #
        _data = basic_mdt.exportMatDict(self.pointsetdata[point], ['Crossline', 'Inline', 'Z'])
        #
        # apply z scale
        _data[:, 2] *= self.canvasproperties['Z_Scale']
        #
        _vis = scene.visuals.Markers()
        _vis.set_data(_data,
                      size=self.pointsetvisconfig[point]['Size'],
                      face_color=self.pointsetvisconfig[point]['Color'].lower(),
                      edge_color=None,
                      symbol=self.pointsetvisconfig[point]['Marker'],
                      scaling=False)
        #
        return _vis


    def createVisualSrvBox(self):
        _srvlines = []
        if checkSurvInfo(self.survinfo):
            _xlstart = self.survinfo['XLStart']
            _xlend = self.survinfo['XLEnd']
            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
            _inlstart = self.survinfo['ILStart']
            _inlend = self.survinfo['ILEnd']
            _inlstep = self.survinfo['ILStep']
            _inlnum = self.survinfo['ILNum']
            if _inlnum == 1:
                _inlstep = 1
            _xlstep = self.survinfo['XLStep']
            _xlnum = self.survinfo['XLNum']
            if _xlnum == 1:
                _xlstep = 1
            _zstep = self.survinfo['ZStep'] * self.canvasproperties['Z_Scale']
            _znum = self.survinfo['ZNum']
            if _znum == 1:
                _zstep = 1
            #
            for p in ([_xlstart-0.5*_xlstep, _inlstart-0.5*_inlstep, _zend+0.5*_zstep, _xlend+0.5*_xlstep, _inlstart-0.5*_inlstep, _zend+0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlstart-0.5*_inlstep, _zend+0.5*_zstep, _xlstart-0.5*_xlstep, _inlend+0.5*_inlstep, _zend+0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlstart-0.5*_inlstep, _zend+0.5*_zstep, _xlstart-0.5*_xlstep, _inlstart-0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlend+0.5*_inlstep, _zstart-0.5*_zstep, _xlend+0.5*_xlstep, _inlend+0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlend+0.5*_xlstep, _inlstart-0.5*_inlstep, _zstart-0.5*_zstep, _xlend+0.5*_xlstep, _inlend+0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlend+0.5*_xlstep, _inlend+0.5*_inlstep, _zend+0.5*_zstep, _xlend+0.5*_xlstep, _inlend+0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlend+0.5*_xlstep, _inlstart-0.5*_inlstep, _zend+0.5*_zstep, _xlend+0.5*_xlstep, _inlend+0.5*_inlstep, _zend+0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlend+0.5*_inlstep, _zend+0.5*_zstep, _xlend+0.5*_xlstep, _inlend+0.5*_inlstep, _zend+0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlend+0.5*_inlstep, _zend+0.5*_zstep, _xlstart-0.5*_xlstep, _inlend+0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlstart-0.5*_inlstep, _zstart-0.5*_zstep, _xlstart-0.5*_xlstep, _inlend+0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlend+0.5*_xlstep, _inlstart-0.5*_inlstep, _zend+0.5*_zstep, _xlend+0.5*_xlstep, _inlstart-0.5*_inlstep, _zstart-0.5*_zstep],
                      [_xlstart-0.5*_xlstep, _inlstart-0.5*_inlstep, _zstart-0.5*_zstep, _xlend+0.5*_xlstep, _inlstart-0.5*_inlstep, _zstart-0.5*_zstep]):
                _line = scene.visuals.Line(pos=np.array([[p[0], p[1], p[2]], [p[3], p[4], p[5]]]),
                                           color='black', parent=None)
                _srvlines.append(_line)
        #
        return _srvlines


    def createVisualXYZAxis(self):
        _xyz = None
        if checkSurvInfo(self.survinfo):
            _xlstart = self.survinfo['XLStart']
            _xlend = self.survinfo['XLEnd']
            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
            _inlstart = self.survinfo['ILStart']
            _inlend = self.survinfo['ILEnd']
            _inlstep = self.survinfo['ILStep']
            _inlnum = self.survinfo['ILNum']
            if _inlnum == 1:
                _inlstep = 1
            _xlstep = self.survinfo['XLStep']
            _xlnum = self.survinfo['XLNum']
            if _xlnum == 1:
                _xlstep = 1
            _zstep = self.survinfo['ZStep'] * self.canvasproperties['Z_Scale']
            _znum = self.survinfo['ZNum']
            if _znum == 1:
                _zstep = 1
            _x0 = 0.5 * (_xlstart + _xlend)  # _xlstart
            _y0 = 0.5 * (_inlstart + _inlend)  # _inlend + _inlend - _inlstart
            _z0 = 0.5 * (_zstart + _zend)  # _zend + _zend - _zstart
            _len = np.max(np.abs(np.array([_xlstep, _inlstep, _zstep])))
            _xyz = scene.visuals.XYZAxis(parent=None,
                                         pos=np.array([[_x0, _y0, _z0], [_x0 + _len, _y0, _z0],
                                                       [_x0, _y0, _z0], [_x0, _y0 + _len, _z0],
                                                       [_x0, _y0, _z0], [_x0, _y0, _z0 - _len]]))
        #
        return _xyz


    def setCameraRange(self):
        if checkSurvInfo(self.survinfo):
            _xlstart = self.survinfo['XLStart']
            _xlend = self.survinfo['XLEnd']
            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
            _inlstart = self.survinfo['ILStart']
            _inlend = self.survinfo['ILEnd']
            #
            self.view.camera.set_range((_xlstart, _xlend), (_inlstart, _inlend), (_zend, _zstart))
        else:
            self.view.camera.set_range((0, 100), (0, 100), (0, -100))


class qt_mainwindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'GAEIO', 'Are you sure to quit GAEIO?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()


def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)


def checkSeisData(seisdata, survinfo={}):
    return seis_ays.isSeis3DMatConsistentWithSeisInfo(seisdata, survinfo)


def checkPsSeisData(psseisdata):
    return psseis_ays.checkPsSeis(psseisdata)


def checkHorizonData(horizondata):
    return True


def checkFaultPatchData(faultpatchdata):
    return True


def checkPointSetData(pointsetdata):
    return point_ays.checkPointSet(pointsetdata)


def checkWellLogData(welllogdata):
    return True


def checkSettings(setting):
    if (type(setting) is not dict) or (len(setting.keys()) < 1):
        return False
    if 'Gui' not in setting.keys() \
            or 'General' not in setting.keys() \
            or 'Visual' not in setting.keys() \
            or 'Viewer' not in setting.keys():
        return False
    if core_set.checkSettings(gui=setting['Gui'], general=setting['General'],
                              visual=setting['Visual'], viewer=setting['Viewer']) is False:
        return False
    #
    return True


def saveProject(survinfo={}, seisdata={}, psseisdata={}, horizondata={}, faultpatchdata={},
                pointsetdata={}, welllogdata={}, settings={},
                savepath='', savename='gpy'):
    _proj = {}
    _proj['survinfo'] = survinfo
    _proj['seisdata'] = {}
    _proj['psseisdata'] = {}
    _proj['horizondata'] = {}
    _proj['faultpatchdata'] = {}
    _proj['pointsetdata'] = {}
    _proj['welllogdata'] = {}
    _proj['settings'] = settings
    #
    if os.path.exists(os.path.join(savepath, savename + '.proj.data')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data'))
    #
    # save survey
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Survey')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Survey'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Survey'))
    np.save(os.path.join(savepath, savename + '.proj.data/Survey/' + 'survey' + '.srv.npy'), survinfo)
    #
    # save seismic data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Seismic')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Seismic'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Seismic'))
    for key in seisdata.keys():
        _proj['seisdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/Seismic/' + key + '.seis.npy'), seisdata[key])
    #
    # save psseismic data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/PsSeismic')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/PsSeismic'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/PsSeismic'))
    for key in psseisdata.keys():
        _proj['psseisdata'][key] = {}
        for shot in psseisdata[key].keys():
            _proj['psseisdata'][key][shot] = {}
            np.save(os.path.join(savepath, savename + '.proj.data/PsSeismic/' + key + '_shot_' + shot + '.psseis.npy'),
                    psseisdata[key][shot])
    #
    # save horizon data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Horizon')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Horizon'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Horizon'))
    for key in horizondata.keys():
        _proj['horizondata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/Horizon/' + key + '.hrz.npy'), horizondata[key])
    #
    # save faultpatch data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/FaultPatch')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/FaultPatch'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/FaultPatch'))
    for key in faultpatchdata.keys():
        _proj['faultpatchdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/FaultPatch/' + key + '.ftp.npy'), faultpatchdata[key])
    #
    # save pointset data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/PointSet')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/PointSet'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/PointSet'))
    for key in pointsetdata.keys():
        _proj['pointsetdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/PointSet/' + key + '.pts.npy'), pointsetdata[key])
    #
    # save welllog data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/WellLog')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/WellLog'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/WellLog'))
    for key in welllogdata.keys():
        _proj['welllogdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/WellLog/' + key + '.wlg.npy'), welllogdata[key])
    # save settings
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Settings')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Settings'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Settings'))
    np.save(os.path.join(savepath, savename + '.proj.data/Settings/' + 'settings' + '.npy'), settings)
    #
    np.save(os.path.join(savepath, savename + '.proj.npy'), _proj)


def start(startpath=os.path.dirname(__file__)[:-8]):
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    MainWindow = qt_mainwindow()
    gui = mainwindow()
    gui.settings['General']['RootPath'] = startpath
    gui.setupGUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start()
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # gui = gui_mainwindow()
    # gui.setupGUI(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())


