'''
Copyright (C) 2018 Alan North
alannorth@gmail.com

Created by Alan North

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    'name': "Debugger for VS Code",
    'author': "Alan North, M. Scott Lassiter",
    'version': (3, 0, 0),
    'blender': (3, 3, 0), # Debugpy doesn't seem to work on previous versions. Unable to import it...
    'description': "Starts debugging server for VS Code.",
    'location': "View 3D > Sidebar > Debugger Tab",
    'warning': "",
    'doc_url': "https://github.com/AlansCodeLog/blender-debugger-for-vscode", 
    'tracker_url': "https://github.com/AlansCodeLog/blender-debugger-for-vscode/issues",
    'category': 'Development',
}

import bpy

from .directory_monitor import monitor
from .hot_swap import reload_modules

from .preferences import DebuggerPreferences
from .ui import DebuggerPanel, DebugServerPanel, HotSwapPanel

from .operators.debugger_check import DebuggerCheck
from .operators.debug_server_start import DebugServerStart
from .operators.monitor_start import MonitorStart
from .operators.monitor_stop import MonitorStop
from .operators.open_addon_preferences import OpenAddonPreferences
from .operators.toggle_blender_terminal import ToggleBlenderTerminal

debugger_classes = (
    # Panels
    DebuggerPanel,
    DebugServerPanel,
    HotSwapPanel,

    # Operators
    DebuggerCheck,
    DebugServerStart,
    MonitorStart,
    MonitorStop,
    OpenAddonPreferences,
    ToggleBlenderTerminal,

    # Preferences
    DebuggerPreferences
)

def register():
    for cls in debugger_classes:
        bpy.utils.register_class(cls)
    bpy.context.preferences.use_preferences_save = True

    monitor._directory = bpy.context.preferences.addons[__package__].preferences.monitor_path
        # Ensure the directory is set to a valid path at startup; prevents unexpected errors for the first time user
    
    monitor.subscribe("Hotswap", reload_modules)

def unregister(): 
    for cls in debugger_classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
