import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand):
    functionPattern = 'function'
    visibilityPattern = 'private'
    pointerPattern = '->'

    def run(self, edit):
        privateObjects = self.getOcorrences()
        print('de')
        for key, value in privateObjects.items():
            self.view.add_regions("mark", [value], "mark", "dot", sublime.HIDDEN | sublime.PERSISTENT)


    def getRegionLines(self):
        return list(self.view.lines(sublime.Region(0,self.view.size())))

    def getLineText(self):
        textList = []
        lines = self.getRegionLines()
        for line in lines:
            textList.append(self.view.substr(line))
        return textList

    def getFunctionNames(self):
        functionName = {}
        coordinates =  self.view.lines(sublime.Region(0,self.view.size()))

        for coordinate in coordinates:
            lineContent =  self.view.substr(coordinate)
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

    def getOcorrences( self ):
        frequency = {}
        text =  self.view.substr(sublime.Region(0,100000))
        
        objects = self.getPrivateObjects()
        for key, value in objects.items():
            match =  re.findall( self.pointerPattern+key, text)
            if len(match) == 0:
                frequency[key] = value

        return frequency    

