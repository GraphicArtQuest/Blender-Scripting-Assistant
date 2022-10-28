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

# from .bundler import bundle
# from .directory_monitor import monitor
from .debug_server import DebugServerStart
from .operators.toggle_blender_terminal import ToggleBlenderTerminal
from .operators.debugger_check import DebuggerCheck

classes = (
   DebuggerPanel,
   DebugServerPanel,
   DebuggerPreferences,
   DebuggerCheck,
   DebugServerStart,
   ToggleBlenderTerminal
)



# def update_watch_For_Updates(self, context):
# # Runs when the "Watch for Updates" checkbox changes

#    bpy.context.preferences.addons['BlenderDebugger'].preferences.watch_For_Updates = self.watch_For_Updates

#    if self.watch_For_Updates:
#       print ('Commenced polling for updates to the debug folder.')
#       start_Polling_For_Updates()
#    else:
#       # bpy.context.preferences.addons['BlenderDebugger'].preferences.watch_For_Updates = False
#       # You have to stop this timer when turning off update polling, or else
#       #     you just accumulate more and more timers until you close Blender.
#       pollTimer.cancel()
#       print ('Secured from polling for updates.')

# def update_Debug_Path(self, context):
# # Runs when the "File or Folder to Debug" changes

#    print('Watch for updates: ' + str(self.watch_For_Updates))
#    print(self.debug_Path)
#    bpy.context.preferences.addons['BlenderDebugger'].preferences.debugpath = self.debug_Path


def register():
   for cls in classes:
      bpy.utils.register_class(cls)
   # bpy.types.Scene.debug_Path = bpy.props.StringProperty(
   #       name="Folder to Debug",
   #       subtype="FILE_PATH",
   #       # update=update_Debug_Path
   #    )
   bpy.types.Scene.watch_For_Updates = bpy.props.BoolProperty(
         name='Watch for Updates',
         default=False,
         # update=update_watch_For_Updates
      )

def unregister(): 
   for cls in classes:
      bpy.utils.unregister_class(cls)
   # del bpy.types.Scene.debug_Path
   del bpy.types.Scene.watch_For_Updates

if __name__ == "__main__":
   register()
