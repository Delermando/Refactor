import sublime, sublime_plugin, pprint

class DevHelper(sublime_plugin.TextCommand, sublime.View):
    def run(self, edit):
        #self.view.set_name("Dev Helper! Hello Word")
        #self.view.insert(edit, 0, "Alo")
        #print(str(self.view.name()))
        braces = False
        sels = self.view.sel()
        for sel in sels:
            if self.view.substr(sel).find('{') != -1:
                braces = True

        if not braces:
            new_sels = []
            for sel in sels:
                new_sels.append( self.view.find('\}', sel.end()))
            sels.clear()
            for sel in sels:
                sels.add(sel)
            self.view.run_command("expand_selection", {"to":"brackets"})