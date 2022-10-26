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

import os
import re
import subprocess
import sys

import bpy

from .bundler import bundle
from .directory_monitor import monitor

last_Tracked_Update = 0

# finds path to debugpy if it exists
def check_for_debugpy():
   pip_info = None
   try:
      pip_info = subprocess.Popen(
          "pip show debugpy",
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE
      )
   except Exception as e:
      print(e)
      pass
   if pip_info is not None:
      pip_info = str(pip_info.communicate()[0], "utf-8")
      pip_info = re.sub("\\\\", "/", pip_info)
      #extract path up to last slash
      match = re.search("Location: (.*)", pip_info)
      #normalize slashes
      if match is not None:
         match = match.group(1)
         if os.path.exists(match+"/debugpy"):
            return match

  # commands to check
   checks = [
       ["where", "python"],
       ["whereis", "python"],
       ["which", "python"],
   ]
   location = None
   for command in checks:
      try:
         location = subprocess.Popen(
             command,
             shell=True,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE
         )
      except Exception:
         continue
      if location is not None:
         location = str(location.communicate()[0], "utf-8")
         #normalize slashes
         location = re.sub("\\\\", "/", location)
         #extract path up to last slash
         match = re.search(".*(/)", location)
         if match is not None:
            match = match.group(1)
            if os.path.exists(match+"lib/site-packages/debugpy"):
               match = match+"lib/site-packages"
               return match

   # check in path just in case PYTHONPATH happens to be set
   # this is not going to work because Blender's sys.path is different
   for path in sys.path:
      path = path.rstrip("/")
      if os.path.exists(path+"/debugpy"):
         return path
      if os.path.exists(path+"/site-packages/debugpy"):
         return path+"/site-packages"
      if os.path.exists(path+"/lib/site-packages/debugpy"):
         return path+"lib/site-packages"
   return "debugpy not Found"

# Preferences
class DebuggerPreferences(bpy.types.AddonPreferences):
   bl_idname = __name__

   path: bpy.props.StringProperty(
      name="Location of debugpy (site-packages folder)",
      subtype="DIR_PATH",
      default=check_for_debugpy()
   )

   timeout: bpy.props.IntProperty(
      name="Timeout",
      default=20
   )

   port: bpy.props.IntProperty(
      name="Port",
      min=0,
      max=65535,
      default=5678
   )

   debugpath: bpy.props.StringProperty(
      name="File or Folder to Debug",
      subtype="FILE_PATH"
   )

   watch_For_Updates: bpy.props.BoolProperty(
      name="Watch for Updates",
      default=False
   )

   def draw(self, context):
      layout = self.layout
      row_path = layout
      row_path.label(text="The addon will try to auto-find the location of debugpy. If no path is found or you would like to use a different path, set it here.")
      row_path.prop(self, "path")

      row_timeout = layout.split()
      row_timeout.prop(self, "timeout")
      row_timeout.label(text="Timeout in seconds for the attach confirmation listener.")

      row_port = layout.split()
      row_port.prop(self, "port")
      row_port.label(text="Port to use. Should match port in VS Code's launch.json.")

      row_debug = layout.box()
      row_debug.prop(self, "debugpath")
      row_debug.prop(self, "watch_For_Updates")


# check if debugger has attached
def check_done(i, modal_limit, prefs):
   if i == 0 or i % 60 == 0:
      print("Waiting... (on port "+str(prefs.port)+")")
   if i > modal_limit:
      print("Attach Confirmation Listener Timed Out")
      return {"CANCELLED"}
   if not debugpy.is_client_connected():
      return {"PASS_THROUGH"}
   print('Debugger is Attached')
   return {"FINISHED"}

class DebuggerPanel(bpy.types.Panel):
   """This is a Tooltip"""
   bl_label = "Debugger"
   bl_idname = "OBJECT_PT_DebugPanel"
   bl_space_type = 'VIEW_3D'
   bl_region_type = 'UI'
   bl_category = 'Debugger'


   def draw(self, context):
      layout = self.layout
      # row=box.row()
      row = layout.box()
      row.label(text="Port to use. Should match port in VS Code's launch.json.")
      row.operator(DebugServerStart.bl_idname, text="Start Debug Server", icon="SCRIPT")
      # row = layout.box()
      # portText = "Port: %p" % bpy.context.preferences.addons['BlenderDebugger'].preferences.port
      portText = str(bpy.context.preferences.addons['BlenderDebugger'].preferences.port)
      row = layout.row()
      row.label(text=portText)
      row.label(text=str(bpy.context.preferences.addons['BlenderDebugger'].preferences.debugpath))
      row = layout.row()
      # row.prop(context.scene, 'add_version')
      # row.prop(context.scene, 'debugFolderPath')
      # row.prop(context.scene, 'debug_Path')
      row = layout.row()
      row.prop(context.scene, 'watch_For_Updates')

      # row_port.prop(self, "port")

class DebuggerCheck(bpy.types.Operator):
   bl_idname = "debug.check_for_debugger"
   bl_label = "Debug: Check if VS Code is Attached"
   bl_description = "Starts modal timer that checks if debugger attached until attached or until timeout"

   _timer = None
   count = 0
   modal_limit = 20*60

   # call check_done
   def modal(self, context, event):
      self.count = self.count + 1
      if event.type == "TIMER":
         prefs = bpy.context.preferences.addons[__name__].preferences
         return check_done(self.count, self.modal_limit, prefs)
      return {"PASS_THROUGH"}

   def execute(self, context):
      # set initial variables
      self.count = 0
      prefs = bpy.context.preferences.addons[__name__].preferences
      self.modal_limit = prefs.timeout*60

      wm = context.window_manager
      self._timer = wm.event_timer_add(0.1, window=context.window)
      wm.modal_handler_add(self)
      return {"RUNNING_MODAL"}

   def cancel(self, context):
      print("Debugger Confirmation Cancelled")
      wm = context.window_manager
      wm.event_timer_remove(self._timer)

class DebugServerStart(bpy.types.Operator):
   bl_idname = "debug.connect_debugger_vscode"
   bl_label = "Debug: Start Debug Server for VS Code"
   bl_description = "Starts debugpy server for debugger to attach to"

   waitForClient: bpy.props.BoolProperty(default=False)

   def execute(self, context):
      #get debugpy and import if exists
      prefs = bpy.context.preferences.addons[__name__].preferences
      debugpy_path = prefs.path.rstrip("/")
      debugpy_port = prefs.port

      #actually check debugpy is still available
      if debugpy_path == "debugpy not found":
         self.report({"ERROR"}, "Couldn't detect debugpy, please specify the path manually in the addon preferences or reload the addon if you installed debugpy after enabling it.")
         return {"CANCELLED"}

      if not os.path.exists(os.path.abspath(debugpy_path+"/debugpy")):
         self.report({"ERROR"}, "Can't find debugpy at: %r/debugpy." % debugpy_path)
         return {"CANCELLED"}

      if not any(debugpy_path in p for p in sys.path):
         sys.path.append(debugpy_path)

      global debugpy #so we can do check later
      import debugpy

      # can only be attached once, no way to detach (at least not that I understand?)
      try:
         debugpy.listen(("localhost", debugpy_port))
      except:
         print("Server already running.")

      if (self.waitForClient):
         self.report({"INFO"}, "Blender Debugger for VSCode: Awaiting Connection")
         debugpy.wait_for_client()

      # call our confirmation listener
      bpy.ops.debug.check_for_debugger()
      return {"FINISHED"}

classes = (
   DebuggerPanel,
   DebuggerPreferences,
   DebuggerCheck,
   DebugServerStart,
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
   bpy.types.Scene.debug_Path = bpy.props.StringProperty(
         name="Folder to Debug",
         subtype="FILE_PATH",
         # update=update_Debug_Path
      )
   bpy.types.Scene.watch_For_Updates = bpy.props.BoolProperty(
         name='Watch for Updates',
         default=False,
         # update=update_watch_For_Updates
      )

def unregister(): 
   for cls in classes:
      bpy.utils.unregister_class(cls)
   del bpy.types.Scene.debug_Path
   del bpy.types.Scene.watch_For_Updates

if __name__ == "__main__":
   register()
