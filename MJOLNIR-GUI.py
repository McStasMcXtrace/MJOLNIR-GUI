

try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass


from MJOLNIR import _tools # Usefull tools useful across MJOLNIR
import numpy as np
import matplotlib.pyplot as plt

from os import path


plt.ion()


from PyQt5 import QtWidgets, QtCore, QtGui

from MJOLNIR_GUI_ui import Ui_MainWindow  
from MJOLNIR_Data import GuiDataFile,GuiDataSet
from DataModels import DataSetModel,DataFileModel
import sys




# Naming convention: WhereInGui_description_type
# Append _function if it is a function
# E.g.: View3D_plot_button and View3D_plot_button_function

#Headlines so far are:
#DataSet, View3D, QELine, QPlane, Cut1D,



class mywindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
    
        self.ui.setupUi(self)
        
        self.currentDataSetIndex = 0

        self.dataSets = []
        

        self.setupDataSet() # Setup datasets with buttons and call functions
        self.setupDataFile() # Setup datafiles
        self.setupDebugDataSet()
        
        ##############################################################################
        # View3D
        ##############################################################################       
        self.ui.View3D_plot_button.clicked.connect(self.View3D_plot_button_function)
        self.ui.View3D_setCAxis_button.clicked.connect(self.View3D_setCAxis_button_function)
        self.ui.View3D_SetTitle_button.clicked.connect(self.View3D_SetTitle_button_function)

        ##############################################################################
        # QELine
        ##############################################################################
        self.ui.QELine_plot_button.clicked.connect(self.QELine_plot_button_function)
        self.ui.QELine_setCAxis_button.clicked.connect(self.QELine_setCAxis_button_function)
        self.ui.QELine_SetTitle_button.clicked.connect(self.QELine_SetTitle_button_function)

        ##############################################################################
        # QPlane
        ##############################################################################
        self.ui.QPlane_plot_button.clicked.connect(self.QPlane_plot_button_function)
        self.ui.QPlane_setCAxis_button.clicked.connect(self.QPlane_setCAxis_button_function)
        self.ui.QPlane_SetTitle_button.clicked.connect(self.QPlane_SetTitle_button_function)
        
        
        
        # self.V=None
        
        
    def DataSet_convertData_button_function(self):
        #The loading should be moved to a different button        
        #fileList,_ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","hdf Files (*.hdf);;All Files (*)")

        binning=int(self.ui.DataSet_binning_comboBox.currentText())
        ds = self.DataSetModel.getCurrentDataSet()
        ds.convertDataFile(binning=binning,saveFile=False)
        
        
    def View3D_plot_button_function(self):

        # Check if we already have data, otherwise convert current data.
        ds = self.DataSetModel.getCurrentDataSet()
        if len(ds.convertedFiles)==0:
            self.DataSet_convertData_button_function()
        
        QXBin=float(self.ui.View3D_QXBin_lineEdit.text())
        QYBin=float(self.ui.View3D_QYBin_lineEdit.text())
        EBin =float(self.ui.View3D_EBin_lineEdit.text())
        
        self.V = ds.View3D(QXBin,QYBin,EBin)
        
        self.View3D_setCAxis_button_function()
        
    def View3D_setCAxis_button_function(self):
        if not hasattr(self, 'V'):
            self.View3D_plot_button_function()
            
        CAxisMin=float(self.ui.View3D_CAxisMin_lineEdit.text())
        CAxisMax=float(self.ui.View3D_CAxisMax_lineEdit.text())
        
        self.V.set_clim(CAxisMin,CAxisMax)
        
    def View3D_SetTitle_button_function(self):        
        TitleText=self.ui.View3D_SetTitle_lineEdit.text()        
        self.V.set_title(TitleText)
        
        ##############################################################################
        # QELine
        ##############################################################################
    def QELine_plot_button_function(self):
        print('This button has not been implemented yet')

    def QELine_setCAxis_button_function(self):
        
        CAxisMin=float(self.ui.QELine_CAxisMin_lineEdit.text())
        CAxisMax=float(self.ui.QELine_CAxisMax_lineEdit.text())
        
        # self.V.set_clim(CAxisMin,CAxisMax)
        
        print('This button has not been implemented yet')

    def QELine_SetTitle_button_function(self):
        TitleText=self.ui.QELine_SetTitle_lineEdit.text()        
        print('This button has not been implemented yet')


        ##############################################################################
        # QPlane
        ##############################################################################        
    def QPlane_plot_button_function(self):
        print('This button has not been implemented yet')

    def QPlane_setCAxis_button_function(self):
        print('This button has not been implemented yet')        
        CAxisMin=float(self.ui.QPlane_CAxisMin_lineEdit.text())
        CAxisMax=float(self.ui.QPlane_CAxisMax_lineEdit.text())

    def QPlane_SetTitle_button_function(self):
        TitleText=self.ui.QPlane_SetTitle_lineEdit.text()        
        print('This button has not been implemented yet')
        

    def setupDataSet(self): # Set up main features for Gui regarding the dataset widgets
        self.ui.DataSet_convertData_button.clicked.connect(self.DataSet_convertData_button_function)
        self.ui.DataSet_NewDataSet_button.clicked.connect(self.DataSet_NewDataSet_button_function)
        self.ui.DataSet_DeleteDataSet_button.clicked.connect(self.DataSet_DeleteDataSet_button_function)
        self.ui.DataSet_AddFiles_button.clicked.connect(self.DataSet_AddFiles_button_function)

        self.DataSetModel = DataSetModel(dataSets=self.dataSets,DataSet_DataSets_listView=self.ui.DataSet_DataSets_listView)
        self.ui.DataSet_DataSets_listView.setModel(self.DataSetModel)

        self.ui.DataSet_DataSets_listView.clicked.connect(self.selectedDataSetChanged)
        self.ui.DataSet_DataSets_listView.doubleClicked.connect(self.DataSet_DoubleClick_Selection_function)

    def setupDataFile(self): # Set up main features for Gui regarding the datafile widgets
        self.DataFileModel = DataFileModel(DataSet_filenames_listView=self.ui.DataSet_filenames_listView,dataSetModel=self.DataSetModel,DataSet_DataSets_listView=self.ui.DataSet_DataSets_listView)
        self.ui.DataSet_filenames_listView.setModel(self.DataFileModel)
        self.ui.DataSet_filenames_listView.clicked.connect(self.selectedDataFileChanged)
        self.ui.DataSet_DeleteFiles_button.clicked.connect(self.DataSet_DeleteFiles_button_function)

        self.ui.DataSet_DataSets_listView.doubleClicked.connect(self.DataFile_DoubleClick_Selection_function)
        

    def setupDebugDataSet(self):

        files = ['/home/lass/Dropbox/PhD/CAMEAData/camea2018n000494.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000495.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000496.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000497.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000498.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000499.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000500.hdf']
        dfs = []
        for f in files:
            dfs.append(GuiDataFile(f))

        ds = GuiDataSet(dfs,name='set1')
        self.DataSetModel.append(ds)

        files = ['/home/lass/Dropbox/PhD/CAMEAData/camea2018n000494.hdf', '/home/lass/Dropbox/PhD/CAMEAData/camea2018n000495.hdf']
        dfs = []
        for f in files:
            dfs.append(GuiDataFile(f))

        ds2 = GuiDataSet(dfs,name='set2')
        self.DataSetModel.append(ds2)
        #for index in range(len(self.dataSets)):
        #    item = self.ui.DataSet_filenames_listView.item(index)
        #    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)


    @property
    def currentDataFileIndex(self):
        return self._currentDataFileIndex

    @currentDataFileIndex.getter
    def currentDataFileIndex(self):
        return self._currentDataFileIndex

    @currentDataFileIndex.setter
    def currentDataFileIndex(self,index):
        self._currentDataFileIndex = index


    @property
    def currentDataSetIndex(self):
        return self._currentDataSetIndex

    @currentDataSetIndex.getter
    def currentDataSetIndex(self):
        return self._currentDataSetIndex

    @currentDataSetIndex.setter
    def currentDataSetIndex(self,index):
        self._currentDataSetIndex = index

    def selectedDataSetChanged(self,*args,**kwargs):
        self.DataFileModel.updateCurrentDataSetIndex()

    def selectedDataFileChanged(self,*args,**kwargs):
        self.DataFileModel.layoutChanged.emit()


    def DataSet_NewDataSet_button_function(self):
        ds = GuiDataSet(name='Added')
        self.DataSetModel.append(ds)

    def DataSet_DeleteDataSet_button_function(self):
        self.DataSetModel.delete(self.ui.DataSet_DataSets_listView.selectedIndexes()[0])
        


    def DataSet_DeleteFiles_button_function(self):
        self.DataFileModel.delete()


    def DataSet_DoubleClick_Selection_function(self,index,*args,**kwargs):
        self.ui.DataSet_DataSets_listView.edit(index,'Hej')

    def DataFile_DoubleClick_Selection_function(self,index,*args,**kwargs):
        self.ui.DataSet_filenames_listView.edit(index)

    def DataSet_AddFiles_button_function(self):
        currentFolder = self.ui.DataSet_path_lineEdit.text()
        if path.exists(currentFolder):
            folder=currentFolder
        else:
            folder = ""
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", folder,"HDF (*.hdf);;All Files (*)")
        self.DataFileModel.add(files)
        

def run():
    app = QtWidgets.QApplication(sys.argv)

    application = mywindow()

    application.show()

    sys.exit(app.exec_())

run()