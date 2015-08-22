import sublime, sublime_plugin, pprint
import re

class MarkNotUsedObejctsInFunction(sublime_plugin.TextCommand):

    def run(self, edit):
        print(self.view.size())