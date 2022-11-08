import bpy

from ..directory_monitor import monitor

class MonitorStart(bpy.types.Operator):
    bl_idname = "scriptingassistant.monitor_start"
    bl_label = "Starts monitoring for changes"
    bl_description = "Monitor the debug directory for changes and conduct hot swap when detected"

    def execute(self, context):
        monitor.watch()
        return {'FINISHED'}