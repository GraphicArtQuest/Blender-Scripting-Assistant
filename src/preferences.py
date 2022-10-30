import os

import bpy

from .debug_server import check_for_debugpy

class DebuggerPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    debugpy_path: bpy.props.StringProperty(
        name="Location of debugpy (site-packages folder)",
        subtype='DIR_PATH',
        default=check_for_debugpy()
    )

    debugpy_timeout: bpy.props.IntProperty(
        name="Timeout",
        min=0,
        default=20
    )

    debugpy_port: bpy.props.IntProperty(
        name="Port",
        min=0,
        max=65535,
        default=5678
    )

    monitor_path: bpy.props.StringProperty(
        name="File or Folder to Debug",
        subtype="FILE_PATH",
        default= os.path.dirname(__file__)
    )
    
    monitor_addon_name: bpy.props.StringProperty(
        name="Name of Monitored Add-on",
        subtype='FILE_PATH',
        default= "Debugger for VS Code"
    )

    watch_for_updates: bpy.props.BoolProperty(
        name="Watch for Updates",
        default=True
    )

    # def draw(self, context):
    #     layout = self.layout
        # row_path.label(text="The addon will try to auto-find the location of debugpy. If no path is found or you would like to use a different path, set it here.")

        # row_timeout.label(text="Timeout in seconds for the attach confirmation listener.")

        # row_port.label(text="Port to use. Should match port in VS Code's launch.json.")