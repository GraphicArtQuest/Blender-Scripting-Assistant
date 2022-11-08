import bpy

class ToggleBlenderTerminal(bpy.types.Operator):
    bl_idname = "scriptingassistant.toggle_terminal"
    bl_label = "Toggle: show or hide the system terminal"
    bl_description = "Toggles the system terminal on or off"

    def execute(self, context):
        bpy.ops.wm.console_toggle()
        return {'FINISHED'}