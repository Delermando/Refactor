
class Tools(object):
    
    def getNotUsedObjectsFromContent(pointer, content, objects ):
        frequency = {}
        for key, value in objects.items():
            match =  re.findall( pointer + key, content )
            if len(match) == 0:
                frequency[key] = value 
        return frequency   

    def getContentByRegion(view, coordinate):
        return view.substr(coordinate)

    def getAllDocumentCoordinates(sublime, view):
        return sublime.Region(0,view.size())

    def sanitizeClass(string):
        return string.split()[1]

    def sanitizeFunction(string):
        return string.split()[2].replace('(','')

    def sanitizeVariable(string):
        string =  string.split()[1].replace('$','')
        return string.replace(';','')

    def match(regex, content):
        return re.search( regex, content )
        
    def draw( objects):
        print('-----------------Object Not Used--------------------------')
        for key, value in objects:    
            print(self.pointer + key)
            self.markLine(value)            
        print('----------------------------------------------------------')
