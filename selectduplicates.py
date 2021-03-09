# encoding: utf-8

import gvsig

import os

from org.gvsig.fmap.dal import DALLocator;
from gvsig import currentTable
from org.gvsig.tools import ToolsLocator

def selectDuplicates(store, attrName):
  mvstore = None
  tempFile = None
  status = ToolsLocator.getTaskStatusManager().createDefaultSimpleTaskStatus("SelectDuplicates")
  status.add()
  status.setAutoremove(True)
  try:
    dataManager = DALLocator.getDataManager()
    dup = dataManager.createLargeMap()
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

def main(*args):
  table = currentTable()
  #print dir(table)
  selectDuplicates(table.getFeatureStore(),"COM")
  