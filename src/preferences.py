import os

import bpy

from .debug_server import check_for_debugpy

class DebuggerPreferences(bpy.types.AddonPreferences):
    """This class holds all debugger preferences for the add-on."""
    
    bl_idname = __package__

    debugpy_path: bpy.props.StringProperty(
        name="Location of debugpy (site-packages folder)",
        subtype='DIR_PATH',
        default=check_for_debugpy()
    ) # type: ignore

    debugpy_timeout: bpy.props.IntProperty(
        name="Timeout",
        min=0,
        default=20
    ) # type: ignore

    debugpy_port: bpy.props.IntProperty(
        name="Port",
        min=0,
        max=65535,
        default=5678
    ) # type: ignore

    monitor_path: bpy.props.StringProperty(
        name="File or Folder to Debug",
        subtype="FILE_PATH",
        default= ""
    ) # type: ignore
    
    monitor_addon_name: bpy.props.StringProperty(
        name="Name of Monitored Add-on",
        subtype='FILE_PATH',
        default= "Blender Scripting Assistant"
    ) # type: ignore

    monitor_addon_filename: bpy.props.StringProperty(
        name="File Name of Monitored Add-on",
        default= "blender-scripting-assistant",
        subtype='FILE_PATH',
    ) # type: ignore
