import sublime
import sublime_plugin

import os


class OpenTerminalHereCommand(sublime_plugin.ApplicationCommand):
	def run(self, dirs):
		settings = sublime.load_settings("OpenTerminalHere.sublime-settings")
		if not settings.has("open-terminal-command"):
			print("OpenTerminalHere Could not find setting 'open-terminal-command'.")
			return
		
		command = settings.get("open-terminal-command")
		if command == "":
			print(
				"OpenTerminalHere: Please specify "
				"'open-terminal-command' setting. "
				"Current working directory will be added "
				"to the end of the command."
			)
			return
		for d in dirs:
			os.system(command + "\"" + d + "\"")


	def is_visible(self, dirs):
		return len(dirs) > 0
