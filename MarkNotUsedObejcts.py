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
        allLinesCoordinates = Tools.getAllDocumentCoordinates(sublime, self.view)
        privateObjects = Tools.getNotUsedObjectsFromContent(
            Php.pointer,
            Tools.getContentByRegion(self.view, allLinesCoordinates), 
            self.getPrivateObjects()
        )
        Tools.draw(privateObjects.items())

    def getLinesCoordinates(self):
        return list(self.view.lines(sublime.Region(0,self.view.size())))
    
    def markLine(self,region):
        self.view.add_regions("mark", [region], "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)

    def getContentByRegion(self, coordinate):
        return self.view.substr(coordinate)


    def findFunctionsOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            match = Tools.match(regex, Tools.getContentByRegion(self.view,coordinate))
            if match:
                result[Tools.sanitizeFunction(match.group())] = coordinate
        return result 

    def findVariableOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            match = Tools.match(regex, Tools.getContentByRegion(self.view,coordinate))
            if match:
                result[Tools.sanitizeVariable(match.group())] = coordinate
        return result

    def getClassName(self,coordinates):
        result = {}
        match = Tools.match(self.classRegex, Tools.getContentByRegion(self.view,sublime.Region(0,self.view.size())))
        if match:
            result = Tools.sanitizeClass( match.group())
        return result

        
    def getFunctionNames(self):
        functions = self.findFunctionsOcorrences(self.getLinesCoordinates(), self.functionRegex)    
        className = self.getClassName(self.getLinesCoordinates())
        if len(functions) > 0 and className in functions:
            del functions[className]

        return functions

    def getVariablesNames(self):
        return self.findVariableOcorrences(self.getLinesCoordinates(), self.variablesRegex)    

    def getPrivateObjects(self):
        return  dict(list(self.getVariablesNames().items()) + list(self.getFunctionNames().items()))

    