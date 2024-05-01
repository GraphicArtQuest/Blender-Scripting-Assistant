import os
import subprocess

import bpy

class OpenMonitoredSourceDirectory(bpy.types.Operator):
    bl_idname = "scriptingassistant.open_monitor_source_directory"
    bl_label = "Debug: Open Monitored Source Directory"
    bl_description = "Opens the monitored source file directory in a new file explorer window"

    def execute(self, context):
        prefs = bpy.context.preferences.addons["blender-scripting-assistant"].preferences

        print("Opening the monitored source file directory in a new file explorer window to:", prefs.monitor_path)
        subprocess.Popen(f'explorer "{prefs.monitor_path}"')

        return {'FINISHED'}
