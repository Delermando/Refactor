import sublime, sublime_plugin, pprint
import re
from .tools import Tools
from .php import Php

class MarkNotUsedObejcts(sublime_plugin.TextCommand):
    pointer = '->'
    classRegex = '(\s)*class(\s)+(\S+)((\s*)extends|\s)+(\S+)(\s)*{'
    functionRegex = 'private[\s\n]+function[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = 'private[\s\n]+\$+(\S+)'
    
    def run(self, edit):
        self.Tools = Tools(sublime,self.view)

        allLinesCoordinates = self.Tools.getAllDocumentCoordinates()
        
        privateObjects = self.Tools.getNotUsedObjectsFromContent(
            Php.pointer,
            self.Tools.getContentByRegion(allLinesCoordinates), 
            self.Tools.getPrivateObjects(Php.classRegex,Php.functionRegex,Php.variablesRegex)
        )
        self.Tools.draw(privateObjects.items(),Php.pointer)


 

        
