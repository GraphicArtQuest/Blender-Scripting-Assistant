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
   'name': 'Debugger for VS Code',
   'author': 'Alan North, M. Scott Lassiter',
   'version': (2, 2, 0),
   'blender': (3, 3, 0), # Haven't verified on anything lower than 3.3
   "description": "Starts debugging server for VS Code.",
   'location': 'In search (Edit > Operator Search) type "Debug"',
   "warning": "",
   "doc_url": "https://github.com/AlansCodeLog/blender-debugger-for-vscode", 
   "tracker_url": "https://github.com/AlansCodeLog/blender-debugger-for-vscode/issues",
   'category': 'Development',
}

import bpy

from .preferences import DebuggerPreferences
from .ui import DebuggerPanel, DebugServerPanel

from .operators.debugger_check import DebuggerCheck
from .operators.debug_server_start import DebugServerStart
from .operators.toggle_blender_terminal import ToggleBlenderTerminal

debugger_classes = (
   # Panels
   DebuggerPanel,
   DebugServerPanel,

   # Operators
   DebuggerCheck,
   DebugServerStart,
   ToggleBlenderTerminal,

   # Preferences
   DebuggerPreferences
)

def register():
   for cls in debugger_classes:
      bpy.utils.register_class(cls)

def unregister(): 
   for cls in debugger_classes:
      bpy.utils.unregister_class(cls)

if __name__ == "__main__":
   register()
