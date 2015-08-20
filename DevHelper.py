import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand):
    functionPattern = 'function'
    visibilityPattern = 'private'
    pointerPattern = '->'

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

    def getContentByRegion(self, coordinates):
        return self.view.substr(coordinates)

    def getFunctionNames(self):
        functionName = {}
        coordinates =  self.getLinesCoordinates()

        for coordinate in coordinates:
            lineContent =  self.getContentByRegion(coordinate)
            regex = self.visibilityPattern + '[\s\n]+' +self.functionPattern+'[\s\n]+(\S+)[\s\n]*\('
            match = re.search( regex, lineContent )
            if match:
                functionName[self.sanitize(match.group())] = coordinate

        return functionName    

    def getVariablesNames(self):
        functionName = {}
        coordinates =  self.view.lines(sublime.Region(0,self.view.size()))

        for coordinate in coordinates:
            lineContent =  self.view.substr(coordinate)
            regex = self.visibilityPattern + '[\s\n]+\$+(\S+)';
            match = re.search( regex, lineContent )
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

