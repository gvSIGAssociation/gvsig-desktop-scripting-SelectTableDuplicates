# encoding: utf-8

import gvsig

from gvsig.uselib import use_plugin

use_plugin('org.gvsig.h2spatial.app.mainplugin')

import os

from org.h2.mvstore import MVStore 
from gvsig import currentTable
from org.gvsig.tools import ToolsLocator

def selectDuplicates(store, attrName):
  mvstore = None
  tempFile = None
  status = ToolsLocator.getTaskStatusManager().createDefaultSimpleTaskStatus("SelectDuplicates")
  status.add()
  status.setAutoremove(True)
  try:
    foldersManager = ToolsLocator.getFoldersManager()
    tempFile = foldersManager.getUniqueTemporaryFile("selecttabledup")
    mvstore = MVStore.Builder().fileName(tempFile.getAbsolutePath()).open()
    dup = mvstore.openMap("dup")
    dup.clear()
    selection = store.createFeatureSelection()
    status.setRangeOfValues(0,store.getFeatureCount())
    n = 0
    for f in store:
      status.setCurValue(n)
      value = f.get(attrName)
      if dup.has_key(value):
        selection.select(f)
      else:
        dup[value] = True
      n+=1
    store.setSelection(selection)

  finally:
    status.terminate()
    if mvstore!=None:
      mvstore.close()
    if tempFile!=None:
      os.remove(tempFile.getAbsolutePath())

def main(*args):
  table = currentTable()
  #print dir(table)
  selectDuplicates(table.getFeatureStore(),"CALLE_TEXT")
  