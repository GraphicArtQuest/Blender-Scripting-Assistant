import os

import bpy

from .console_messages.hotswap import HotswapMessages as message
from .directory_monitor import monitor

def reload_modules():
    try:
        addon_path = bpy.context.preferences.addons[__package__].preferences.monitor_path
        addon_name = os.path.splitext(os.path.basename(addon_path))[0]

        if addon_path == "" or addon_name == "":
            monitor.secure()
            return
        
        if addon_name == __package__:
            message.cannot_hotswap_debugger()
            bpy.context.preferences.addons[__package__].preferences.monitor_path = ""
            monitor.secure()
            return

        bpy.ops.preferences.addon_disable(module=addon_name)
        bpy.ops.preferences.addon_install(overwrite=True, filepath=addon_path)
        bpy.ops.preferences.addon_enable(module=addon_name)

        message.hotswap_successful()
    except:
        message.blender_error()
