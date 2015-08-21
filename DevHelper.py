import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand):
    functionPattern = 'function'
    visibilityPattern = 'private'
    pointerPattern = '->'
    functionRegex = visibilityPattern + '[\s\n]+' +functionPattern+'[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = visibilityPattern + '[\s\n]+\$+(\S+)'

    def run(self, edit):
        privateObjects = self.getPrivateObjectsNotUsed()
        self.draw(privateObjects.items())

    def draw(self, objects):
        print('-----------------not used--------------------------')
        for key, value in objects:    
            print(key)
            self.markLine(value)            
        print('---------------------------------------------------')

    def getLinesCoordinates(self):
        return list(self.view.lines(sublime.Region(0,self.view.size())))
    
    def markLine(self,region):
        self.view.add_regions("mark", [region], "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)

    def getContentByRegion(self, coordinate):
        return self.view.substr(coordinate)

    def match(self, regex, content):
        return re.search( regex, content )


    def findObjectOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            lineContent = self.getContentByRegion(coordinate)
            match = self.match(regex, lineContent)
            if match:
                result[self.sanitize(match.group())] = coordinate
        return result

    def getFunctionNames(self):
        return self.findObjectOcorrences(self.getLinesCoordinates(), self.functionRegex)    

    def getVariablesNames(self):
        functionName = {}
        coordinates =  self.view.lines(sublime.Region(0,self.view.size()))

        for coordinate in coordinates:
            lineContent =  self.view.substr(coordinate)
            match = self.match(self.variablesRegex, lineContent)
            if match:
                functionName[self.sanitize(match.group())] = coordinate

        return functionName


    def sanitize(self, string):
        remove = ['(', ' ', ';', '$', self.visibilityPattern, self.functionPattern]
        for item in remove:
            string = string.replace(item, '')

        return string

    def getPrivateObjects(self):
        variables = self.getVariablesNames()
        functions = self.getFunctionNames()
        return  dict(list(variables.items()) + list(functions.items()))

    def getPrivateObjectsNotUsed( self ):
        frequency = {}
        text =  self.view.substr(sublime.Region(0,100000))
        
        objects = self.getPrivateObjects()
        for key, value in objects.items():
            match =  re.findall( self.pointerPattern+key, text)
            if len(match) == 0:
                frequency[key] = value

        return frequency    

