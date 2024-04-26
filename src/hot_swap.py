import os
import sys

import bpy

from .console_messages.hotswap import HotswapMessages as message
from .directory_monitor import monitor

def create_addon_name(addon_path: str) -> str:
    """Based on the path provided to it, this function derives the required Blender add-on name for hot swap transfer.

    If the path is to a file or folder that does not exist, it should log an error and return an empty string.

    If the path is to a file, the name should be the bl_info.name property. If this property is not present, it should
        log an error and return an empty string.

    If the path is to a folder, the name should be the bl_info.name property from the __init__.py file. If that file
        is not present, it should log an error and return an empty string.

    In all cases, the returned file name should be in lower case and with spaces replaced by dashes ("-").
    """
      
    # Safely format the name as a string in case something other than a string passed
    addon_name = str(os.path.splitext(os.path.basename(addon_path))[0])
    addon_directory = os.path.dirname(addon_path)   # Temporarily adds this directory to the os path to try importing it

    sys.path.append(addon_directory)

    try:
        # Using the `__import__` function here will successfully work for `.py` files or for folders that have an
        #   `__init__.py` file, in which case it imports as module.
        addon_module = __import__(addon_name)
        valid_name = addon_module.bl_info['name'].lower().strip().replace(" ", "-")
        
    except:
        # Throw error message
        valid_name = ""

    sys.path.remove(addon_directory)    # Cleanup the temporarily added os path directory
    return valid_name

def reload_modules() -> None:
    """Reloads a specified add-on back into Blender by disabling, reinstalling, and enabling it again.
    
    Trying to hot swap an empty package or the debugger itself will throw an error message. Because these errors are
        uncorrectable without changing settings, monitoring stops.
    
    An error that occurs within a hot reloaded script will print the error to the console and continue to monitor. This
        allows the user to correct the script and try again.  
    """

    try:
        addon_path = bpy.context.preferences.addons[__package__].preferences.monitor_path
        addon_name = os.path.splitext(os.path.basename(addon_path))[0]

        if addon_path == "" or addon_name == "":
            monitor.secure()
            return
        
        if addon_name == __package__:
            # Trying to hot swap a module that is actively running the hot swap code will cause a fatal error in
            #   Blender as it tries to find a reference in memory that doesn't exist anymore. Blender will immediately
            #   crash with no warning or indication of what went wrong. This check prevents that while informing the
            #   user why it won't let them do this within the terminal.
            message.cannot_hotswap_debugger()
            bpy.context.preferences.addons[__package__].preferences.monitor_path = ""
            monitor.secure()
            return

        bpy.ops.preferences.addon_disable(module=addon_name)
        bpy.ops.preferences.addon_install(overwrite=True, filepath=addon_path)
        bpy.ops.preferences.addon_enable(module=addon_name)

        message.hotswap_successful()
    except:
        # There is no need to capture and print the specifiic error here because Blender does that to the Console anyway
        #   just before this except statement runs.
        # HOWEVER, the monitor DOES NOT STOP. This allows the user to correct whatever problem they introduced and get
        #   it easily reloaded once it works again.
        message.blender_error()
