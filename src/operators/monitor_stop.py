import bpy

from ..directory_monitor import monitor

class MonitorStop(bpy.types.Operator):
    bl_idname = "scriptingassistant.monitor_stop"
    bl_label = "Stop monitoring for changes"
    bl_description = "Stops monitoring the debug directory for changes and makes no more hot swaps"

    def execute(self, context):
        monitor.secure()
        return {'FINISHED'}