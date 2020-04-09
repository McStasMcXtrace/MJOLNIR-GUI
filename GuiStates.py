from StateMachine import State,AllFalseBut,AllTrue,AllFalse,AllTrueBut

import numpy as np



## enterStateFunction
def AllEnabled(StateMachine):
    names = [item.objectName for item in StateMachine.guiWindow.blockItems]
    enabled = np.ones(len(names))
    #enabledNames = ['DataSet_NewDataSet_button',]
    for item,enable in zip(StateMachine.guiWindow.blockItems,enabled):
        item.setEnabled(enable)


def RawEnabled(StateMachine):
    names = [item.objectName() for item in StateMachine.guiWindow.blockItems]
    enabled = np.ones(len(names))
    enabledNames = ['DataSet_NewDataSet_button','DataSet_DeleteDataSet_button',
    'DataSet_AddFiles_button','DataSet_DeleteFiles_button','DataSet_convertData_button','DataSet_binning_comboBox',
    'View3D_plot_button','QELine_plot_button','QPlane_plot_button']
    
    enabled = AllFalseBut(enabledNames,enabled,names)
    for item,enable in zip(StateMachine.guiWindow.blockItems,enabled):
        item.setEnabled(enable)


def PartialEnabled(StateMachine):
    names = [item.objectName() for item in StateMachine.guiWindow.blockItems]
    enabled = np.ones(len(names))
    enabledNames = ['DataSet_NewDataSet_button','DataSet_DeleteDataSet_button',
    'DataSet_AddFiles_button',
    'View3D_plot_button','QELine_plot_button','QPlane_plot_button']
    
    enabled = AllFalseBut(enabledNames,enabled,names)
    for item,enable in zip(StateMachine.guiWindow.blockItems,enabled):
        item.setEnabled(enable)
    


def EmptyEnabled(StateMachine):
    names = [item.objectName() for item in StateMachine.guiWindow.blockItems]
    enabled = np.ones(len(names))
    enabledNames = ['DataSet_NewDataSet_button','View3D_plot_button','QELine_plot_button','QPlane_plot_button']
    
    enabled = AllFalseBut(enabledNames,enabled,names)
    for item,enable in zip(StateMachine.guiWindow.blockItems,enabled):
        item.setEnabled(enable)
    

## Transition functions

def transitionEmptyPartial(StateMachine): # What is required to transition from empty to partial
    return StateMachine.guiWindow.DataSetModel.rowCount(None)>0

def transitionPartialRaw(StateMachine): # What is required to transition from partial to raw
    count = StateMachine.guiWindow.DataFileModel.rowCount(None)
    if not count is None:
        return count>0 and transitionEmptyPartial(StateMachine)
    else:
        return False

def transitionRawConverted(StateMachine): # What is required to transition from partial to raw
    ds = StateMachine.guiWindow.DataSetModel.getCurrentDataSet()
    if not ds is None:
        return len(ds.convertedFiles)>0
    else:
        return False

### Functions to force transition

def forceTransitionEmptyPartial(StateMachine): # add DataSet
    StateMachine.guiWindow.DataSet_NewDataSet_button_function()
    return transitionEmptyPartial(StateMachine)

def forceTransitionPartialRaw(StateMachine): # add DataFile
    StateMachine.guiWindow.DataSet_AddFiles_button_function()
    return transitionPartialRaw(StateMachine)

def forceTansitionRawConverted(StateMachine): # add DataFile
    StateMachine.guiWindow.DataSet_convertData_button_function()
    return transitionRawConverted(StateMachine)


### States for state machine

# Allows plotting, fitting and all the fun
converted = State('Converted',nextState=None,enterStateFunction=AllEnabled) 

# Has DataSet, DataFiles but not converded yet
raw = State('Raw',enterStateFunction=RawEnabled,transitionRequirement=transitionRawConverted,
                transitionFunction=forceTansitionRawConverted,nextState=converted)

# Has DataSet but no DataFiles
partial = State('Partial',enterStateFunction=PartialEnabled,transitionRequirement=transitionPartialRaw,
                transitionFunction=forceTransitionPartialRaw,nextState=raw)

# Has no DataSet
empty = State('Empty',enterStateFunction=EmptyEnabled,transitionRequirement=transitionEmptyPartial,
                transitionFunction=forceTransitionEmptyPartial,nextState=partial)