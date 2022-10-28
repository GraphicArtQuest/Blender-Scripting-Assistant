import bpy

from ..debug_server import check_done

class DebuggerCheck(bpy.types.Operator):
   bl_idname = "debugger.check_for_debugger"
   bl_label = "Debug: Check if VS Code is Attached"
   bl_description = "Starts modal timer that checks if debugger attached until attached or until timeout"

   _timer = None
   count = 0
   modal_limit = 20*60

   # call check_done
   def modal(self, context, event):
      self.count = self.count + 1
      if event.type == "TIMER":
         prefs = bpy.context.preferences.addons["blender-debugger-for-vscode"].preferences
         return check_done(self.count, self.modal_limit, prefs)
      return {"PASS_THROUGH"}

   def execute(self, context):
      # set initial variables
      self.count = 0
      prefs = bpy.context.preferences.addons["blender-debugger-for-vscode"].preferences
      self.modal_limit = prefs.timeout*60

      wm = context.window_manager
      self._timer = wm.event_timer_add(0.1, window=context.window)
      wm.modal_handler_add(self)
      return {"RUNNING_MODAL"}

   def cancel(self, context):
      print("Debugger Confirmation Cancelled")
      wm = context.window_manager
      wm.event_timer_remove(self._timer)