import re
class Tools(object):
    
    def __init__(self,sublime,view,edit):
        self.view = view   
        self.edit = edit
        self.sublime = sublime

    def getNotUsedObjectsFromContent(self,pointer, content, objects ):
        frequency = {}
        for key, value in objects.items():
            match =  re.findall( pointer + key, content )
            if len(match) == 0:
                frequency[key] = value 
        return frequency   

    def getContentByCoordinate(self,coordinate):
        return self.view.substr(coordinate)

    def getContentByCoordinates(self, regions):
        content = ''
        for region in regions:
            content += self.getContentByCoordinate(region) + '\n'
        return content

    def removeContentByCoordinate(self, coordinate):
        self.view.erase(self.edit, coordinate)

    def removeContentByCoordinates(self, regions):
        for region in regions:
            self.removeContentByCoordinate(region) 

    def getAllDocumentCoordinates(self):
        return self.sublime.Region(0,self.view.size())

    def sanitizeClass(self,string):
        return string.split()[1]

    def sanitizeFunction(self,string):
        return string.split()[2].replace('(','')

    def sanitizeVariable(self,string):
        string =  string.split()[1].replace('$','')
        return string.replace(';','')

    def match(self, regex, content):
        return re.search( regex, content )

    def draw(self, objects,pointer):
        print('-----------------Object Not Used--------------------------')
        for key, value in objects:    
            print(pointer + key)
            self.markLine(value)            
        print('----------------------------------------------------------')

    def getClassName(self,classRegex,coordinates, content):
        result = {}
        match = self.match(classRegex, content)
        if match:
            result = self.sanitizeClass( match.group())
        return result

    def getLinesCoordinates(self):
        return list(self.view.lines(self.sublime.Region(0,self.view.size())))
    
    def getSelectedRegion(self):
        return self.view.sel()

    def markLine(self,region):
        self.view.add_regions("mark", [region], "mark", "dot", self.sublime.HIDDEN | self.sublime.PERSISTENT)


    def findVariableOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            match = self.match(regex, self.getContentByCoordinate(coordinate))
            if match:
                result[self.sanitizeVariable(match.group())] = coordinate
        return result

    def getVariablesNames(self,variablesRegex):
        return self.findVariableOcorrences(self.getLinesCoordinates(), variablesRegex)   

    def findFunctionsOcorrences(self, coordinates, regex):
        result = {}
        for coordinate in coordinates:
            match = self.match(regex, self.getContentByCoordinate(coordinate))
            if match:
                result[self.sanitizeFunction(match.group())] = coordinate
        return result


    def getFunctionNames(self,classRegex, functionRegex):
        functions = self.findFunctionsOcorrences(self.getLinesCoordinates(), functionRegex)    
        className = self.getClassName(
            classRegex,
            self.getLinesCoordinates(), 
            self.getContentByCoordinate(self.getAllDocumentCoordinates())
        )

        if len(functions) > 0 and className in functions:
            del functions[className]

        return functions 

    def getPrivateObjects(self,classRegex,functionRegex,variablesRegex):
        return  dict(list(self.getVariablesNames(variablesRegex).items()) + list(self.getFunctionNames(classRegex,functionRegex).items()))


