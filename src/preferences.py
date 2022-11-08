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
        default= ""
    )
    
    monitor_addon_name: bpy.props.StringProperty(
        name="Name of Monitored Add-on",
        subtype='FILE_PATH',
        default= "Blender Scripting Assistant"
    )
