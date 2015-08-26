class Php(object):
    pointer = '->'
    classRegex = '(\s)*class(\s)+(\S+)((\s*)extends|\s)+(\S+)(\s)*{'
    functionRegex = 'private[\s\n]+function[\s\n]+(\S+)[\s\n]*\('
    variablesRegex = 'private[\s\n]+\$+(\S+)'