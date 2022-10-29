import bpy

def update_watch_for_updates(self, context):
    """Runs when the 'Watch for Updates' checkbox changes"""

    bpy.context.preferences.addons[__package__].preferences.watch_for_updates = self.watch_for_updates

    if self.watch_for_updates:
        print ('Commenced polling for updates to the debug folder.')
        #   start_Polling_For_Updates()
    else:
        # You have to stop this timer when turning off update polling, or else
        #     you just accumulate more and more timers until you close Blender.
        #   pollTimer.cancel()
        print ('Secured from polling for updates.')

def update_debugpy_path(self, context):
    """Runs when the 'File or Folder to Debug' changes"""

    print('Watch for updates: ' + str(self.watch_for_updates))
    print(self.debugpy_path)
    bpy.context.preferences.addons[__package__].preferences.debugpy_path = self.debugpy_path

class DebuggerPanel(bpy.types.Panel):
    """The main panel for all the Blender Debugger tools"""
    bl_label = "Blender Debugger for VS Code"
    bl_idname = "OBJECT_PT_DebuggerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=str(bpy.context.preferences.addons[__package__].preferences.monitor_path))
        row = layout.row()
        row.operator('debugger.toggle_terminal', text="Toggle Terminal")
        row = layout.row()
        row.prop(context.scene, 'watch_for_updates')
        row = layout.row()
        row.prop(context.scene, 'debugpy_path')
    
    bpy.types.Scene.watch_for_updates = bpy.props.BoolProperty(
            name='Watch for Updates',
            default=True,
            update=update_watch_for_updates
        )
    
    bpy.types.Scene.debugpy_path = bpy.props.StringProperty(
            name="Folder to Debug",
            subtype="FILE_PATH",
            update=update_debugpy_path
        )

class DebugServerPanel(bpy.types.Panel):
    """This is a sub menu within the N panel that contains the configuration settings for the Debugpy server"""
    bl_label = "Debug Server Settings"
    bl_idname = "OBJECT_PT_DebugSubPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'
    bl_parent_id = "OBJECT_PT_DebuggerPanel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Port to use. Should match port in VS Code's launch.json.")
        portText = str(bpy.context.preferences.addons[__package__].preferences.debugpy_port)
        row.operator('debugger.connect_debugger_vscode', text="Start Debug Server", icon="SCRIPT")
        row.label(text=portText)
        row = layout.row()
        # row.prop(bpy.context.preferences.addons[__package__].preferences.port)
        # row.prop(context.scene, __package__ + "port") # Can't figure out how to make this work
