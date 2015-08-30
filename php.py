from .tools import Tools

class Php(object):
    pointer = '->'
    classRegex = '(\s)*class(\s)+(\S+)((\s*)extends|\s)+(\S+)(\s)*{'
    functionRegex = 'private[\s\n]+function[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = 'private[\s\n]+\$+(\S+)'
    newFunctionPattern = 'private function %s(%s)\n{\n %s \n}'

    def markNotUsedObejcts(sublime,view,edit):
        tools = Tools(sublime,view, edit)

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


    def extracCodeToFunction(sublime, edit, view):
        tools = Tools(sublime, view,edit)
        functionContent = tools.getContentByCoordinates(tools.getSelectedRegion())
        tools.showInputPanel('Function name:', tools, 'insertFunction', Php.newFunctionPattern, functionContent)

        
        #tools.removeContentByCoordinates(tools.getSelectedRegion())
        #content = (
        #    'teste',
        #    'teste1',
        #    'teste2'
        #)
        #functionPattern = (Php.newFunctionPattern %  content)
        #tools.insertContentByPosition(tools.getViewSize(),'dede')
    