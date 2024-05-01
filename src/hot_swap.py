import importlib
import importlib.util
import os
import shutil
import sys
import bpy

from .console_messages.hotswap import HotswapMessages as message
from .directory_monitor import monitor

def get_most_recent_bl_name_info(addon_path: str) -> str:
    """Returns the current `bl_info.name` for a Blender add-on.

    This function works for both single files and packages. Assuming the add-on has a `bl_info` property with a 
    `name` field, this function will return that value exactly as is.

    If the add-on does NOT have this required property, it is missing `name`, the file or package just does not
    exist, or some other error occurs while reading it, then the function  will return an empty string.

    This function works by using the `importlib.util` library to get a module spec based on the provided `addon_path`,
    and then tries to load that module. It cleans up after itself once done.

    Errors:
    - If the path is to a file or folder that does not exist, it should log an error and return an empty string.

    - If the path is to a file, the name should be the bl_info.name property. If this property is not present, it should
        log an error and return an empty string.

    - If the path is to a folder, the name should be the bl_info.name property from the __init__.py file. If that file
        is not present, it should log an error and return an empty string.
    """

    addon_name = str(os.path.splitext(os.path.basename(addon_path))[0])

    if os.path.isfile(addon_path):
        spec = importlib.util.spec_from_file_location(addon_name, addon_path)
    else:
        spec = importlib.util.spec_from_file_location(addon_name, os.path.join(addon_path, "__init__.py"))

    mod = importlib.util.module_from_spec(spec)

    sys.modules[addon_name] = mod

    try:
        spec.loader.exec_module(mod)
        given_name = mod.bl_info['name']
    except Exception as error:
        message.monitored_addon_must_have_valid_name_in_bl_info_single_file()
        print("Python error message: ", error)
        given_name = ""
    
    del sys.modules[addon_name]

    return given_name

def create_addon_name(addon_given_name: str) -> str:
    """Based on the plain name provided to it, this function derives the required add-on name for hot swap transfer.
    
    The returned file name should be in lower case and with spaces replaced by dashes ("-").
    """

    return str(addon_given_name).lower().strip().replace(" ", "-")

def update_scripting_assistant_preference_addon_name(addon_name: str) -> None:
    """Updates the Scripting Assistant's prefernce for value `monitor_addon_name`.

    Note: This function carries no data validation or error checking logic of any kind.
    """
    prefs = bpy.context.preferences.addons["blender-scripting-assistant"].preferences
    prefs.monitor_addon_name = addon_name

def update_scripting_assistant_preference_addon_filename(addon_filename: str) -> None:
    """Updates the Scripting Assistant's prefernce for value `monitor_addon_filename`.

    Note: This function carries no data validation or error checking logic of any kind.
    """
    prefs = bpy.context.preferences.addons["blender-scripting-assistant"].preferences
    prefs.monitor_addon_filename = addon_filename

def reload_modules() -> None:
    """Reloads a specified add-on back into Blender by disabling, reinstalling, and enabling it again.
    
    Trying to hot swap an empty package or the debugger itself will throw an error message. Because these errors are
        uncorrectable without changing settings, monitoring stops.
    
    An error that occurs within a hot reloaded script will print the error to the console and continue to monitor. This
        allows the user to correct the script and try again.  
    """

    try:
        # Get the required information
        addon_path = bpy.context.preferences.addons[__package__].preferences.monitor_path
        old_addon_name = bpy.context.preferences.addons[__package__].preferences.monitor_addon_filename

        addon_name = get_most_recent_bl_name_info(addon_path)
        addon_filename = create_addon_name(addon_name)

        # Update the preferences for use in other parts of the add-on
        update_scripting_assistant_preference_addon_name(addon_name)
        update_scripting_assistant_preference_addon_filename(addon_filename)

        if addon_path == "":
            # No way to even begin monitoring in this condition, so we can stop here.
            message.monitor_path_cannot_be_empty()
            # monitor.secure()
            return

        if addon_filename == "":
            # This condition can be corrected by the user, so keep monitoring
            message.monitored_addon_must_have_valid_name_in_bl_info_single_file()
            # monitor.secure()
            return
        
        if addon_filename == __package__:
            # Trying to hot swap a module that is actively running the hot swap code will cause a fatal error in
            #   Blender as it tries to find a reference in memory that doesn't exist anymore. Blender will immediately
            #   crash with no warning or indication of what went wrong. This check prevents that while informing the
            #   user why it won't let them do this within the terminal.
            message.cannot_hotswap_debugger()
            bpy.context.preferences.addons[__package__].preferences.monitor_path = ""
            monitor.secure()
            return

        blender_addon_path = os.path.join(bpy.utils.script_path_user(), "addons")

        # Disable the old add-on. MUST make sure to not delete the scripting assistant add-on itself.
        if old_addon_name in bpy.context.preferences.addons.keys() and old_addon_name != __package__:
            bpy.ops.preferences.addon_disable(module=old_addon_name)
            message.hotswap_omitted_disabled_addon()

        # After disabling within Blender, we have to remove any of the old files. Unfortunately, Python doesn't
        #   make this neat and tidy to do. We first try to remove the add-on assuming it is a single file.
        #   If that doesn't work, try removing it as a folder. If that doesn't work (for example, the name changed),
        #   just move on.
        # Also, MUST make sure to not delete the scripting assistant add-on itself.
        if old_addon_name != "" and old_addon_name != __package__:
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
            shutil.copytree(addon_path, os.path.join(blender_addon_path, addon_filename), dirs_exist_ok=True)

        # Refresh Blender's add-on list to pull in the new files, then enable the add-on
        try:
            bpy.ops.preferences.addon_refresh()
            bpy.ops.preferences.addon_enable(module=addon_filename)
        except Exception as error:
            print("An exception occured while reenabling the add-on: ", error)
        message.hotswap_successful()

    except Exception as error:
        # There is no need to capture and print the specific error here because Blender does that to the Console anyway
        #   just before this except statement runs.
        # HOWEVER, the monitor DOES NOT STOP. This allows the user to correct whatever problem they introduced and get
        #   it easily reloaded once it works again.
        print("A general exception occurred during hot swap: ", error)
        message.blender_error()
