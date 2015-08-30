import re
class Tools(object):
    userInputKey = 'userInput'    

    def __init__(self,sublime,view,edit):
        self.view = view   
        self.edit = edit
        self.sublime = sublime
        self.window = sublime.active_window()

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

    def insertContentByPosition(self,position,content):
        return self.view.insert(self.edit, position, content)

    def getViewSize(self):
        return self.view.size()

    def removeContentByCoordinate(self, coordinate):
        return self.view.erase(self.edit, coordinate)

    def removeContentByCoordinates(self, regions):
        for region in regions:
            self.removeContentByCoordinate(region) 

    def getAllDocumentCoordinates(self):
        return self.sublime.Region(0,self.getViewSize())

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

    def executeFunctionFromClassWithThreeParams(self, classe, functionName, param1, param2, param3):
        getattr(classe, functionName)( param1, param2, param3 )

    def executeFunctionFromClassToInputPanel(self, classe, functionName, pattern, userSelection,userInput):
        return self.executeFunctionFromClassWithThreeParams(classe, functionName, pattern, userSelection,userInput)

    def getPrivateObjects(self,classRegex,functionRegex,variablesRegex):
        return  dict(list(self.getVariablesNames(variablesRegex).items()) + list(self.getFunctionNames(classRegex,functionRegex).items()))

    def showInputPanel(self, label, classe, functionName, pattern, userSelection):
        self.window.show_input_panel(label, '', lambda userInput: self.executeFunctionFromClassToInputPanel(classe, functionName, pattern, userSelection, userInput), None, None)
        
    def getParamsFromString(self, string):
        return string.split()

    def setUserInput(self, userInput):
        self.setSetting(self.userInputKey, userInput)
        
    def setSetting(self, key, value):
        self.view.settings().set(key, value)

    def getSetting(self, key):
        return self.view.settings().get(key)


    def formatUserFunctionArgs(self,args):
        argsList = self.getParamsFromString(args)
        if len(argsList) == 2:
            return args
        elif len(argsList) > 2:
            pass
        else:
            pass

    def insertFunction(self, pattern, userSelection, userInput):
        pass
        #contentList = self.getParamsFromString(userInput)
        #contentList  += (userSelection,)
        #newFunctionContent = (pattern %  tuple(contentList))
        #self.insertContentByPosition(self.getViewSize(),newFunctionContent)
        Tools.insertContentByPosition(Tools,1,'dede')