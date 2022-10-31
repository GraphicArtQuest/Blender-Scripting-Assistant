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

    def blender_error():
        print(HotswapMessages._ErrorHeader() + "Blender encountered a fatal error while trying to reload the monitored"
            + " add-on. Continuing to monitor.")
    
    def cannot_hotswap_debugger():
        print(HotswapMessages._ErrorHeader() + "Hotswapping the debugger will cause a fatal error in Blender."
            + " You must change the debug path.")
