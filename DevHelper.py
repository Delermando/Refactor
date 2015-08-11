import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand):
    functionPattern = 'function'
    visibilityPattern = 'private'

    def run(self, edit):
        print(self.getPrivateObjects())

    def getRegionLines(self):
        return list(self.view.lines(sublime.Region(0,self.view.size())))

    def getLineText(self):
        textList = []
        lines = self.getRegionLines()
        for line in lines:
            textList.append(self.view.substr(line))
        return textList

    def getFunctionNames(self):
        functionName = []
        lines = self.getLineText()
        for line in lines:
            regex = self.visibilityPattern + '[\s\n]+' +self.functionPattern+'[\s\n]+(\S+)[\s\n]*\('
            match = re.search( regex, line )
            if match:
                functionName.append( match.group() )

        return functionName    

    def getVariablesNames(self):
        functionName = []
        lines = self.getLineText()
        for line in lines:
            regex = self.visibilityPattern + '[\s\n]+\$+(\S+)';
            match = re.search( regex, line )
            if match:
                functionName.append(match.group())

        return functionName


    def sanitize(self, string):
        remove = ['(', ' ', ';', '$', self.visibilityPattern, self.functionPattern]
        for item in remove:
            string = string.replace(item, '')

        return string

    def getPrivateObjects(self):
        result = []
        objects = self.getVariablesNames() + self.getFunctionNames()
        for obj in objects:
            result.append( self.sanitize(obj) )

        return result

    def getOcorrences( self ):
        return self.view.substr(sublime.Region(0,1000))
        ocorrences = []
        objects = self.getPrivateObjects()
        text = self.getLineText()
        for obj in objects: 
          return re.findall( obj, text )
          if match:
              ocorrences.append( match.group() )

        return ocorrences    