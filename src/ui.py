import bpy

class DebuggerPanel(bpy.types.Panel):
    """The main panel for all the Blender Debugger tools"""
    bl_label = "Blender Debugger for VS Code"
    bl_idname = "OBJECT_PT_DebugPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Port to use. Should match port in VS Code's launch.json.")
        portText = str(bpy.context.preferences.addons[__package__].preferences.port)
        row.label(text=portText)
        row = layout.row()
        row.label(text=str(bpy.context.preferences.addons[__package__].preferences.debugpath))
        row = layout.row()
        row.operator('debugger.toggle_terminal', text="Toggle Terminal")
        row = layout.row()
        row.prop(context.scene, 'watch_For_Updates')

class DebugServerPanel(bpy.types.Panel):
    """This is a sub menu within the N panel that contains the configuration settings for the Debugpy server"""
    bl_label = "Debug Server Settings"
    bl_idname = "OBJECT_PT_DebugSubPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'
    bl_parent_id = "OBJECT_PT_DebugPanel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Port to use. Should match port in VS Code's launch.json.")
        portText = str(bpy.context.preferences.addons[__package__].preferences.port)
        row.operator('debug.connect_debugger_vscode', text="Start Debug Server", icon="SCRIPT")
        row.label(text=portText)
        row = layout.row()
        # row.prop(bpy.context.preferences.addons[__package__].preferences.port)
        # row.prop(context.scene, __package__ + "port") # Can't figure out how to make this work
