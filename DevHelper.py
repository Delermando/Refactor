import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand):
    pointer = '->'
    classRegex = '(\s)*class(\s)+(\S+)((\s*)extends|\s)+(\S+)(\s)*{'
    functionRegex = 'private[\s\n]+function[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = 'private[\s\n]+\$+(\S+)'

    def run(self, edit):
        privateObjects = self.getNotUsedObjectsFromContent(
            self.getContentByRegion(sublime.Region(0,self.view.size())), 
            self.getPrivateObjects()
        )
        self.draw(privateObjects.items())

    def draw(self, objects):
        print('-----------------Object Not Used--------------------------')
        for key, value in objects:    
            print(self.pointer + key)
            self.markLine(value)            
        print('----------------------------------------------------------')

    def getLinesCoordinates(self):
        return list(self.view.lines(sublime.Region(0,self.view.size())))
    
    def markLine(self,region):
        self.view.add_regions("mark", [region], "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)

    def getContentByRegion(self, coordinate):
        return self.view.substr(coordinate)

    def match(self, regex, content):
        return re.search( regex, content )

    def findFunctionsOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            match = self.match(regex, self.getContentByRegion(coordinate))
            if match:
                result[self.sanitizeFunction(match.group())] = coordinate
        return result 

    def findVariableOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            match = self.match(regex, self.getContentByRegion(coordinate))
            if match:
                result[self.sanitizeVariable(match.group())] = coordinate
        return result

    def getClassName(self,coordinates):
        result = {}
        match = self.match(self.classRegex, self.getContentByRegion(sublime.Region(0,self.view.size())))
        if match:
            result = self.sanitizeClass( match.group())
        return result

        
    def getFunctionNames(self):
        functions = self.findFunctionsOcorrences(self.getLinesCoordinates(), self.functionRegex)    
        className = self.getClassName(self.getLinesCoordinates())
        if len(functions) > 0 and className in functions:
            del functions[className]

        return functions

    def getVariablesNames(self):
        return self.findVariableOcorrences(self.getLinesCoordinates(), self.variablesRegex)    

    def sanitizeClass(self, string):
        return string.split()[1]

    def sanitizeFunction(self, string):
        return string.split()[2].replace('(','')

    def sanitizeVariable(self, string):
        string =  string.split()[1].replace('$','')
        return string.replace(';','')

    def getPrivateObjects(self):
        return  dict(list(self.getVariablesNames().items()) + list(self.getFunctionNames().items()))


    def getNotUsedObjectsFromContent( self, content, objects ):
        frequency = {}
        for key, value in objects.items():
            match =  re.findall( self.pointer + key, content )
            if len(match) == 0:
                frequency[key] = value

        return frequency   

    

