import importlib
import os
import shutil
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
        # The `importlib.reload()` call is required to force refresh the module. This is important if the user has
        #   changed the add-on name. Without this, the add-on name would never get updated until Blender was closed
        #   then reopened which could lead to unexpected behavior to the end user.
        addon_module = __import__(addon_name)
        importlib.reload(addon_module)
        given_name = addon_module.bl_info['name']
        valid_name = given_name.lower().strip().replace(" ", "-")
        
    except:
        # TODO: Throw error message
        valid_name = ""

    sys.path.remove(addon_directory)    # Cleanup the temporarily added os path directory

    # Track this name for later cleanup efforts.
    # Note: I broke this into two steps:
    #   1) Get a reference to `prefs`
    #   2) Change the preference value
    # I do not know why, but trying to do it all in one command was not retrieving the value, so I just ended up with
    #   an empty string ("") every time. This resolved the issue.
    prefs = bpy.context.preferences.addons["blender-scripting-assistant"].preferences
    prefs.monitor_addon_filename = valid_name
    prefs.monitor_addon_name = given_name

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
        old_addon_name = bpy.context.preferences.addons[__package__].preferences.monitor_addon_filename
        addon_name = create_addon_name(addon_path)

        if addon_path == "":
            message.monitor_path_cannot_be_empty()
            monitor.secure()
            return

        if addon_name == "":
            message.monitored_addon_must_have_valid_name_in_bl_info_single_file()
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

        blender_addon_path = os.path.join(bpy.utils.script_path_user(), "addons")

        # Disable the old add-on
        if old_addon_name in bpy.context.preferences.addons.keys():
            bpy.ops.preferences.addon_disable(module=old_addon_name)
            message.hotswap_omitted_disabled_addon()

            # After disabling within Blender, we have to remove any of the old files. Unfortunately, Python doesn't
            #   make this neat and tidy to do. We first try to remove the add-on assuming it is a single file.
            #   If that doesn't work, try removing it as a folder. If that doesn't work (for example, the name changed),
            #   just move on.
            
            try:
                os.remove(os.path.join(blender_addon_path, old_addon_name + ".py"))
            except:
                try:
                    shutil.rmtree(os.path.join(blender_addon_path, old_addon_name))
                except:
                    pass
        else:
            message.hotswap_omitted_disabling_unfound_addon()

        # Figure out which modules this add-on has loaded. We have to delete them out of the `sys` object to make
        #   hot swap actually work. Otherwise, when we reload the add-on using `bpy.ops.preferences.addon_refresh()`,
        #   the refreshed module will reuse the old modules. This behavior worked perfectly fine for any add-ons that
        #   were self contained within a single file, but not for add-ons that were written as modules that imported
        #   other submodules.
        # Inspiration for this solution taken from here:
        #   https://blender.stackexchange.com/questions/28504/blender-ignores-changes-to-python-scripts
        addon_modules = []
        for key in sys.modules.keys():
            if key.startswith(old_addon_name) and old_addon_name != "":
                # If old_addon_name is an empty string, this will end up deleting all modules and crash Blender.
                addon_modules.append(key)

        for module in addon_modules:    # Split logic from above to prevent issues with modifying an iterating for loop
            del sys.modules[module]

        # Install the current add-on by copying it into the correct Blender add-on directory
        bpy.ops.preferences.addon_refresh()
        if os.path.isfile(addon_path):
            shutil.copy2(addon_path, blender_addon_path)
        else:
            shutil.copytree(addon_path, os.path.join(blender_addon_path, addon_name), dirs_exist_ok=True)

        # Refresh Blender's add-on list to pull in the new files, then enable the add-on
        bpy.ops.preferences.addon_refresh()
        bpy.ops.preferences.addon_enable(module=addon_name)
        message.hotswap_successful()

    except Exception as error:
        # There is no need to capture and print the specifiic error here because Blender does that to the Console anyway
        #   just before this except statement runs.
        # HOWEVER, the monitor DOES NOT STOP. This allows the user to correct whatever problem they introduced and get
        #   it easily reloaded once it works again.
        print("An exception occurred: ", error)
        message.blender_error()
