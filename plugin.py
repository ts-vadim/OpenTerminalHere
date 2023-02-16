import sublime
import sublime_plugin

import os
import json


_SETTINGS_FILE = "OpenTerminalHere.sublime-settings"


class OpenTerminalHereCommand(sublime_plugin.ApplicationCommand):
	def run(self, dirs):
		settings = sublime.load_settings(_SETTINGS_FILE)
		platform = sublime.platform()

		config = settings.get("config", {})
		terminal_name = config.get(platform, None)
		commands = settings.get("commands", {})
		raw_command = commands.get(terminal_name, "")

		if not config:
			self._report_edit_settings("Field 'config' is missing.")
			return
		if not commands:
			self._report_edit_settings("Field 'commands' is missing.")
			return
		if platform not in config or not terminal_name:
			self._report_edit_settings("Field 'config." + platform + "' is missing")
			return
		if terminal_name not in commands:
			self._report_edit_settings("Field 'commands." + terminal_name + "' is missing")
			return

		for d in dirs:
			variables = {
				"specified_folder": d
			}
			window = sublime.active_window()
			variables.update(window.extract_variables())

			processed_command = sublime.expand_variables(
				raw_command, 
				variables
			)

			print("OpenTerminalHere: executing '" + processed_command + "'")
			os.system(processed_command)

	def is_visible(self, dirs):
		return len(dirs) > 0

	def _report_edit_settings(self, msg):
		dialog_result = sublime.ok_cancel_dialog(
			msg,
			ok_title="Edit Settings",
			title="OpenTerminalHere Configuration Error"
		)
		if dialog_result == sublime.DIALOG_YES:
			sublime.run_command(
				"edit_settings", 
				{
					"base_file": os.path.join(
						sublime.packages_path(),
						"OpenTerminalHere",
						_SETTINGS_FILE
					)
				}
			)
