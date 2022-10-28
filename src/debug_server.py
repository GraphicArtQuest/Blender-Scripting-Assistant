import os
import re
import subprocess
import sys

import bpy

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

class DebugServerStart(bpy.types.Operator):
   bl_idname = "debug.connect_debugger_vscode"
   bl_label = "Debug: Start Debug Server for VS Code"
   bl_description = "Starts debugpy server for debugger to attach to"

   waitForClient: bpy.props.BoolProperty(default=False)

   def execute(self, context):
      #get debugpy and import if exists
      prefs = bpy.context.preferences.addons["blender-debugger-for-vscode"].preferences
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