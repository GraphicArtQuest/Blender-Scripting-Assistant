import debugpy
import os
import re
import subprocess
import sys

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
      print("Waiting... (on port "+str(prefs.debugpy_port)+")")
   if i > modal_limit:
      print("Attach Confirmation Listener Timed Out")
      return {"CANCELLED"}
   if not debugpy.is_client_connected():
      return {"PASS_THROUGH"}
   print('Debugger is Attached')
   return {"FINISHED"}
