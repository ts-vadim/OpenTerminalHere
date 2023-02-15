import sublime
import sublime_plugin

import os


_SETTINGS_FILE = "OpenTerminalHere.sublime-settings"

class OpenTerminalHereCommand(sublime_plugin.ApplicationCommand):
    def run(self, dirs):
        settings = sublime.load_settings(_SETTINGS_FILE)
        
        config = settings.get("config")
        available_terminals = settings.get("available_terminals")

        if sublime.platform() not in config:
            print("OpenTerminalHere: Missing settings field "
                "'config." + sublime.platform() + "'.")
            return

        term = config[sublime.platform()]

        if term is None:
            print("OpenTerminalHere: Terminal for '" + sublime.platform() +
                "' is set to 'null' which means disabled.")
            return
        if term not in available_terminals:
            print("OpenTerminalHere: Terminal name '" + term +
                "' does not appear in 'available_terminals." +
                sublime.platform() + "' setting.")
            return
        
        for d in dirs:
            args = available_terminals[term]

            for i, arg in enumerate(args):
                if arg == "<cwd>":
                    args[i] = "\"" + d + "\""
                    break

            command = ' '.join(args)
            print("OpenTerminalHere: executing '" + command + "'")
            os.system(command)

    def is_visible(self, dirs):
        return len(dirs) > 0
