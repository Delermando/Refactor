import sublime, sublime_plugin, pprint
from .php import Php

class PhpMarkNotUsedObejcts(sublime_plugin.TextCommand):
    def run(self, edit):
       Php.markNotUsedObejcts(sublime,self.view,edit)
        

class PhpExtractCodeToFunction(sublime_plugin.TextCommand):
    def run(self, edit):
        Php.extracCodeToFunction(sublime, edit, self.view)

