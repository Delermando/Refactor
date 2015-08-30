from .tools import Tools

class Php(object):
    pointer = '->'
    classRegex = '(\s)*class(\s)+(\S+)((\s*)extends|\s)+(\S+)(\s)*{'
    functionRegex = 'private[\s\n]+function[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = 'private[\s\n]+\$+(\S+)'

    def markNotUsedObejcts(sublime,view,edit):
        tools = Tools(sublime,view,edit)

        privateObjects = tools.getNotUsedObjectsFromContent(
            Php.pointer,
            tools.getContentByRegion(tools.getAllDocumentCoordinates()), 
            tools.getPrivateObjects(
                Php.classRegex,
                Php.functionRegex,
                Php.variablesRegex
            )
        )
        tools.draw(
            privateObjects.items(),
            Php.pointer
        )


    def extracCodeToFunction(sublime,view,edit):
        tools = Tools(sublime,view,edit)
        functionContent = tools.getContentByCoordinates(tools.getSelectedRegion())
        tools.removeContentByCoordinate(sublime.Region(0,10))

    

