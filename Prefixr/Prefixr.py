import sublime, sublime_plugin, pprint

class DeadCodeCommand(sublime_plugin.TextCommand, sublime.View):
	def run(self, edit):
		#self.view.insert(edit, 0, "Alo")
		self.view.set_name("Diogo Alves")
		print(str(self.view.name()))