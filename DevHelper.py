import sublime, sublime_plugin, pprint

class DevHelper(sublime_plugin.TextCommand, sublime.View):
	def run(self, edit):
		#self.view.insert(edit, 0, "Alo")
		self.view.set_name("Dev Helper! Hello Word")
		print(str(self.view.name()))