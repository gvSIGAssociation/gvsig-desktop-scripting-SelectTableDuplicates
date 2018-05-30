# encoding: utf-8

import gvsig

import thread

from gvsig import currentView
from gvsig import getResource

from java.io import File
from org.gvsig.app import ApplicationLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from org.gvsig.andami import PluginsLocator
from org.gvsig.app.project.documents.table import TableManager

from gvsig import currentTable

from selectduplicates import selectDuplicates

def getWindowOfTable(self):
    application = ApplicationLocator.getManager()
    projectManager = application.getProjectManager()
    tableManager = projectManager.getDocumentManager(TableManager.TYPENAME)
    return tableManager.getMainWindow(self,None)


class SelectTableDuplicatesExtension(ScriptingExtension):
  def __init__(self):
    self.__inprocess = False
    
  def canQueryByAction(self):
    return True

  def isEnabled(self,action):
    if self.__inprocess:
      return False
    table = currentTable()
    tablePanel = getWindowOfTable(table)
    columns = tablePanel.getSelectedColumnsDescriptors()
    if columns == None or len(columns)<1 or len(columns)>1:
      return False
    return True
    
  def isVisible(self,action):
    table = currentTable()
    return table != None
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "selection-table-select-duplicates":
      table = currentTable()
      tablePanel = getWindowOfTable(table)
      columns = tablePanel.getSelectedColumnsDescriptors()
      if columns == None or len(columns)<1 or len(columns)>1:
        return 
      columnName = tablePanel.getSelectedColumnsDescriptors()[0].getName()
      self.__inprocess = True
      thread.start_new_thread(self.process, (table.getFeatureStore(), columnName))

  def process(self, store, columnName):
    selectDuplicates(store, columnName)
    self.__inprocess = False
    
def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  moduleId = "SelectTableDuplicates"
  actionName = "selection-table-select-duplicates"
  tooltip_key =  i18n.getTranslation("_Select_table_duplicates")
  menu_entry = "Selection/_Select_table_duplicates"
  
  extension = SelectTableDuplicatesExtension()

  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()

  #
  # Registramos los iconos en el tema de iconos
  icon = File(getResource(__file__,"images",actionName + ".png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting." + moduleId, "action", actionName, None, icon)

  action = actionManager.createAction(
    extension,
    actionName,    # Action name
    tooltip_key,   # Text
    actionName,    # Action command
    actionName,    # Icon name
    None,          # Accelerator
    302000000,     # Position
    i18n.getTranslation(tooltip_key)    # Tooltip
  )
  action = actionManager.registerAction(action)

  # Añadimos la entrada en el menu herramientas
  application.addMenu(action, menu_entry)
  # Añadimos la accion como un boton en la barra de herramientas.
  #application.addTool(action, "view")

def main(*args):
  selfRegister()
  