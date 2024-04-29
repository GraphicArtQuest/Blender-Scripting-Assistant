""" Output messages to the console for hot swapping.

This module provides defines all the console output messages for the hotswap module.
This makes the code in src/hotswap.py easier to read and maintain. 
"""

from .color_control import color

class HotswapMessages:
    """Consolidates and prints formatted console messages for the hotswap module."""

    @staticmethod
    def _ErrorHeader():
        return str(color.FAIL + "Hotswap error: " + color.ENDC)

    def hotswap_successful():
        print(color.OKGREEN + "Hotswap successfully completed." + color.ENDC)

    def monitor_path_cannot_be_empty():
        print(HotswapMessages._ErrorHeader() + "Cannot hotswap when the monitor path is empty."
            + " Please set a valid path.")

    def monitored_addon_must_have_valid_name_in_bl_info_single_file():
        print(HotswapMessages._ErrorHeader() + "Attempted to hotswap a module that is not a valid Blender add-on."
            + " The add-on MUST contain a bl_info object with a 'name' parameter that is not null.")

    def hotswap_omitted_disabled_addon():
        print("Disabled the monitored add-on.")

    def hotswap_omitted_disabling_unfound_addon():
        print("Attempted to disable the monitored add-on, but it was not active. No action taken.")

    def blender_error():
        print(HotswapMessages._ErrorHeader() + "Blender encountered a fatal error while trying to reload the monitored"
            + " add-on. Continuing to monitor.")

    def cannot_hotswap_debugger():
        print(HotswapMessages._ErrorHeader() + "Hotswapping the debugger will cause a fatal error in Blender."
            + " You must change the debug path.")
