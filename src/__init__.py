"""
Copyright (c) 2022 - Graphic Art Quest (Wayfind Entertainment LLC)

Copyright (C) 2018 - 2022 Alan North
alannorth@gmail.com

Original project blender-debugger-for-vscode Created by Alan North
https://github.com/AlansCodeLog/blender-debugger-for-vscode

Fork and expansion into Blender Scripting Assistant by M. Scott Lassiter.
https://graphicartquest.com/author/scott-lassiter/

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
"""

bl_info = {
    'name': "Blender Scripting Assistant",
    'author': "M. Scott Lassiter, Alan North",
    'version': (1, 1, 1),
    'blender': (3, 3, 0), # Debugpy doesn't seem to work on previous versions. Unable to import it...
    'description': "A comprehensive set of scripting and debugging tools for creating Blender add-ons.",
    'location': "View 3D > Sidebar > Scripting Assistant Tab",
    'warning': "",
    'doc_url': "https://github.com/GraphicArtQuest/Blender-Scripting-Assistant", 
    'tracker_url': "https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/issues/new/choose",
    'category': 'Development',
}

import bpy

from .directory_monitor import monitor
from .hot_swap import reload_modules

from .preferences import DebuggerPreferences
from .ui import ScriptingAssistantPanel, DebugServerPanel, HotSwapPanel

from .operators.debugger_check import DebuggerCheck
from .operators.debug_server_start import DebugServerStart
from .operators.monitor_start import MonitorStart
from .operators.monitor_stop import MonitorStop
from .operators.open_addon_preferences import OpenAddonPreferences
from .operators.open_blender_addon_directory import OpenAddonDirectory
from .operators.open_monitor_source_directory import OpenMonitoredSourceDirectory
from .operators.toggle_blender_terminal import ToggleBlenderTerminal

debugger_classes = (
    # Panels
    ScriptingAssistantPanel,
    DebugServerPanel,
    HotSwapPanel,

    # Operators
    DebuggerCheck,
    DebugServerStart,
    MonitorStart,
    MonitorStop,
    OpenAddonPreferences,
    OpenAddonDirectory,
    OpenMonitoredSourceDirectory,
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
