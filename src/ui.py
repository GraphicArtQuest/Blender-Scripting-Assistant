import os

import bpy

def update_watch_for_updates(self, context):
    """Runs when the 'Watch for Updates' checkbox changes"""

    bpy.context.preferences.addons[__package__].preferences.watch_for_updates = self.watch_for_updates

    if self.watch_for_updates:
        print ("Commenced polling for updates to the debug folder.")
        #   start_Polling_For_Updates()
    else:
        # You have to stop this timer when turning off update polling, or else
        #     you just accumulate more and more timers until you close Blender.
        #   pollTimer.cancel()
        print ("Secured from polling for updates.")

def update_monitor_path(self, context):
    """Runs when the 'File or Folder to Debug' changes"""

    print("Watch for updates: " + str(self.watch_for_updates))
    print(self.debugpy_path)
    bpy.context.preferences.addons[__package__].preferences.debugpy_path = self.debugpy_path

def get_debugpy_port_value(self):
    return bpy.context.preferences.addons[__package__].preferences.debugpy_port

def set_debugpy_port_value(self, value):
    # Because this extends the IntProperty, no additional error handling required
    bpy.context.preferences.addons[__package__].preferences.debugpy_port = value
    print("Updated Debugpy Port to " + str(value))

def get_debugpy_timeout_value(self):
    return bpy.context.preferences.addons[__package__].preferences.debugpy_timeout

def set_debugpy_timeout_value(self, value):
    # Because this extends the IntProperty, no additional error handling required
    bpy.context.preferences.addons[__package__].preferences.debugpy_timeout = value
    print("Updated Debugpy Timeout to " + str(value) + " seconds.")

def get_debugpy_path_value(self):
    return bpy.context.preferences.addons[__package__].preferences.debugpy_path

def set_debugpy_path_value(self, value):
    if os.path.exists(value):
        bpy.context.preferences.addons[__package__].preferences.debugpy_path = value
        print("Updated Debugpy Path to " + str(value))
    else:
        print("DebuggerError: The path " + str(value) + " does not exist. No changes made.")

class DebuggerPanel(bpy.types.Panel):
    """The main panel for all the Blender Debugger tools"""
    bl_label = "Blender Debugger for VS Code"
    bl_idname = "OBJECT_PT_DebuggerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'
    
    bpy.types.Scene.watch_for_updates = bpy.props.BoolProperty(
        name='Watch for Updates',
        default=True,
        update=update_watch_for_updates
    )
    
    bpy.types.Scene.monitor_path = bpy.props.StringProperty(
        name="Folder to Debug",
        subtype='FILE_PATH',
        update=update_monitor_path
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=str(bpy.context.preferences.addons[__package__].preferences.monitor_path))
        row = layout.row()
        row.operator('debugger.toggle_terminal', text="Toggle Terminal")
        row = layout.row()
        row.operator('debugger.open_addon_preferences', text="Open Add-on Preferences")
        row = layout.row()
        row.prop(context.scene, 'watch_for_updates')
        row = layout.row()
        row.prop(context.scene, 'debugpy_path')

class DebugServerPanel(bpy.types.Panel):
    """This is a sub menu within the N panel that contains the configuration settings for the Debugpy server"""
    bl_label = "Debug Server Settings"
    bl_idname = "OBJECT_PT_DebugSubPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'
    bl_parent_id = "OBJECT_PT_DebuggerPanel"
    bl_options = {'DEFAULT_CLOSED'}

    bpy.types.Scene.debugpy_port = bpy.props.IntProperty(
        name="Debug Server Port",
        min=0,
        max=65535,
        get=get_debugpy_port_value,
        set=set_debugpy_port_value
    )

    bpy.types.Scene.debugpy_path = bpy.props.StringProperty(
            name="Path to Debugpy",
            subtype='FILE_PATH',
        get=get_debugpy_path_value,
        set=set_debugpy_path_value
    )

    bpy.types.Scene.debugpy_timeout = bpy.props.IntProperty(
        name="Attach Timeout",
        min=0,
        default=20,
        get=get_debugpy_timeout_value,
        set=set_debugpy_timeout_value
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Port to use. Should match port in VS Code's launch.json.")
        row = layout.separator()
        row = layout.row()
        row.prop(context.scene, "debugpy_path")
        row = layout.row()
        row.prop(context.scene, "debugpy_port")
        row = layout.row()
        row.prop(context.scene, "debugpy_timeout")
        row = layout.row()
        row.operator("debugger.connect_debugger_vscode", text="Start Debug Server", icon='SCRIPT')
