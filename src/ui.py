import os

import bpy

from .directory_monitor import monitor

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
        print("ScriptingAssistantError: The path " + str(value) + " does not exist. No changes made.")

def get_monitor_path_value(self):
    return bpy.context.preferences.addons[__package__].preferences.monitor_path

def set_monitor_path_value(self, value):
    monitor.directory = value
    if monitor.directory == value:
        bpy.context.preferences.addons[__package__].preferences.monitor_path = value


class ScriptingAssistantPanel(bpy.types.Panel):
    """The main panel for all the Blender Scripting Assistant tools"""
    bl_label = "Blender Scripting Assistant"
    bl_idname = "OBJECT_PT_ScriptingAssistantPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scripting Assistant'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("scriptingassistant.toggle_terminal", text="Toggle Terminal")
        row = layout.row()
        row.operator("scriptingassistant.open_addon_preferences", text="Open Add-on Preferences")

class DebugServerPanel(bpy.types.Panel):
    """This is a sub menu within the N panel that contains the configuration settings for the Debugpy server"""
    bl_label = "Debugging"
    bl_idname = "OBJECT_PT_DebugSubPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scripting Assistant'
    bl_parent_id = "OBJECT_PT_ScriptingAssistantPanel"
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
        row = layout.box()
        row.prop(context.scene, "debugpy_path") # The addon will try to auto-find the location of debugpy. If no path is found or you would like to use a different path, set it here
        row.prop(context.scene, "debugpy_port") # Port to use. Should match port in VS Code's launch.json
        row.prop(context.scene, "debugpy_timeout") # Timeout in seconds for the attach confirmation listener
        row = layout.row()
        row.operator("scriptingassistant.start_debugpy_server", text="Start Debug Server", icon='SCRIPT')

class HotSwapPanel(bpy.types.Panel):
    """This is a sub menu within the N panel that contains the configuration settings for the Debugpy server"""
    bl_label = "Hot Swap"
    bl_idname = "OBJECT_PT_HotSwapPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scripting Assistant'
    bl_parent_id = "OBJECT_PT_ScriptingAssistantPanel"
    bl_options = {'DEFAULT_CLOSED'}
    
    bpy.types.Scene.monitor_path = bpy.props.StringProperty(
        name="Add-on File Path",
        subtype='FILE_PATH',
        get=get_monitor_path_value,
        set=set_monitor_path_value
    )
    
    def draw(self, context):
        layout = self.layout
        row = layout.box()
        row.prop(context.scene, "monitor_path")
        row = layout.row()
        if monitor.active:
            row.operator("scriptingassistant.monitor_stop", text="Stop Monitoring", icon='PAUSE')
        else:
            row.operator("scriptingassistant.monitor_start", text="Start Monitoring", icon='PLAY')
