import bpy

class OpenAddonPreferences(bpy.types.Operator):
    bl_idname = "scriptingassistant.open_addon_preferences"
    bl_label = "Debug: Open Add-on Preferences"
    bl_description = "Opens the Blender Preferences window to the Add-on section and filters out the selected add-on"

    def execute(self, context):
        prefs = bpy.context.preferences.addons["blender-scripting-assistant"].preferences

        bpy.ops.screen.userpref_show()
        bpy.data.window_managers["WinMan"].addon_search = prefs.monitor_addon_name
        return {'FINISHED'}
