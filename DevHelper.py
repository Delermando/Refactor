import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand):
    functionPattern = 'function'
    visibilityPattern = 'private'
    pointerPattern = '->'
    functionRegex = visibilityPattern + '[\s\n]+' +functionPattern+'[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = visibilityPattern + '[\s\n]+\$+(\S+)'

    def run(self, edit):
        privateObjects = self.getNotUsedObjectsFromContent(
            self.getContentByRegion(sublime.Region(0,self.view.size())), 
            self.getPrivateObjects()
        )
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
            match = self.match(regex, self.getContentByRegion(coordinate))
            if match:
                result[self.sanitize(match.group())] = coordinate
        return result

    def getFunctionNames(self):
        return self.findObjectOcorrences(self.getLinesCoordinates(), self.functionRegex)    

    def getVariablesNames(self):
        return self.findObjectOcorrences(self.getLinesCoordinates(), self.variablesRegex)    

    def sanitize(self, string):
        remove = ['(', ' ', ';', '$', self.visibilityPattern, self.functionPattern]
        for item in remove:
            string = string.replace(item, '')
        return string

    def getPrivateObjects(self):
        return  dict(list(self.getVariablesNames().items()) + list(self.getFunctionNames().items()))

    def getNotUsedObjectsFromContent( self, content, objects ):
        frequency = {}
        for key, value in objects.items():
            match =  re.findall( self.pointerPattern + key, content )
            if len(match) == 0:
                frequency[key] = value

        return frequency    
