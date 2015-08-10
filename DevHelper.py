import sublime, sublime_plugin, pprint
import re

class DevHelper(sublime_plugin.TextCommand, sublime.View, sublime.Region):
    functionPattern = 'def'

    def run(self, edit):
        print(self.getFunctionNames())

    def getRegionLines(self):
        return list(self.view.lines(sublime.Region(0,self.view.size())))

    def getLineText(self ):
        textList = []
        lines = self.getRegionLines()
        for line in lines:
            textList.append(self.view.substr(line))
        return textList

    def getFunctionNames(self):
        functionName = []
        lines = self.getLineText()
        for line in lines:
            match = re.search(r'def[\s\n]+(\S+)[\s\n]*\(', line)
            if match:
                functionName.append( self.sanitizeString(match.group()))

        return functionName

    def sanitizeString(self, string):
        string = string.replace(self.functionPattern , '')
        string = string.replace(' ' , '')
        string = string.replace('(' , '')
        return string




