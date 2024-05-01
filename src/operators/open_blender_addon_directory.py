import os
import subprocess

import bpy

class OpenAddonDirectory(bpy.types.Operator):
    bl_idname = "scriptingassistant.open_addon_directory"
    bl_label = "Debug: Open Add-on Directory"
    bl_description = "Opens the Blender add-on directory in a new file explorer window"

    def execute(self, context):
        blender_addon_path = os.path.join(bpy.utils.script_path_user(), "addons")
        print("Opening the Blender add-on directory in a new file explorer window to:", blender_addon_path)
        subprocess.Popen(f'explorer "{blender_addon_path}"')

        return {'FINISHED'}
