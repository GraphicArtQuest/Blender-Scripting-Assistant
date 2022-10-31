import os

import bpy

from .console_messages.hotswap import HotswapMessages as message
from .directory_monitor import monitor

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
