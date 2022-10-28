import bpy

def update_watch_For_Updates(self, context):
    """Runs when the "Watch for Updates" checkbox changes"""

    bpy.context.preferences.addons[__package__].preferences.watch_For_Updates = self.watch_For_Updates

    if self.watch_For_Updates:
        print ('Commenced polling for updates to the debug folder.')
        #   start_Polling_For_Updates()
    else:
        # bpy.context.preferences.addons['BlenderDebugger'].preferences.watch_For_Updates = False
        # You have to stop this timer when turning off update polling, or else
        #     you just accumulate more and more timers until you close Blender.
        #   pollTimer.cancel()
        print ('Secured from polling for updates.')

def update_Debug_Path(self, context):
    """Runs when the "File or Folder to Debug" changes"""

    print('Watch for updates: ' + str(self.watch_For_Updates))
    print(self.debug_Path)
    bpy.context.preferences.addons[__package__].preferences.debugpath = self.debug_Path

class DebuggerPanel(bpy.types.Panel):
    """The main panel for all the Blender Debugger tools"""
    bl_label = "Blender Debugger for VS Code 2"
    bl_idname = "OBJECT_PT_DebugPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Debugger'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=str(bpy.context.preferences.addons[__package__].preferences.debugpath))
        row = layout.row()
        row.operator('debugger.toggle_terminal', text="Toggle Terminal")
        row = layout.row()
        row.prop(context.scene, 'watch_For_Updates')
        row = layout.row()
        row.prop(context.scene, 'debug_Path')
    
    bpy.types.Scene.watch_For_Updates = bpy.props.BoolProperty(
            name='Watch for Updates',
            default=True,
            update=update_watch_For_Updates
        )
    
    bpy.types.Scene.debug_Path = bpy.props.StringProperty(
            name="Folder to Debug",
            subtype="FILE_PATH",
            update=update_Debug_Path
        )

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
        row.operator('debugger.connect_debugger_vscode', text="Start Debug Server", icon="SCRIPT")
        row.label(text=portText)
        row = layout.row()
        # row.prop(bpy.context.preferences.addons[__package__].preferences.port)
        # row.prop(context.scene, __package__ + "port") # Can't figure out how to make this work
