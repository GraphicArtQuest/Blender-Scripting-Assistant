import debugpy
import os
import sys

import bpy

class DebugServerStart(bpy.types.Operator):
   bl_idname = "debugger.connect_debugger_vscode"
   bl_label = "Debug: Start Debug Server for VS Code"
   bl_description = "Starts debugpy server for debugger to attach to"

   waitForClient: bpy.props.BoolProperty(default=False)

   def execute(self, context):
      #get debugpy and import if exists
      prefs = bpy.context.preferences.addons["blender-debugger-for-vscode"].preferences
      debugpy_path = prefs.debugpy_path.rstrip("/")
      debugpy_port = prefs.debugpy_port

      #actually check debugpy is still available
      if debugpy_path == "debugpy not found":
         self.report({"ERROR"}, "Couldn't detect debugpy, please specify the path manually in the addon preferences or reload the addon if you installed debugpy after enabling it.")
         return {"CANCELLED"}

      if not os.path.exists(os.path.abspath(debugpy_path+"/debugpy")):
         self.report({"ERROR"}, "Can't find debugpy at: %r/debugpy." % debugpy_path)
         return {"CANCELLED"}

      if not any(debugpy_path in p for p in sys.path):
         sys.path.append(debugpy_path)

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