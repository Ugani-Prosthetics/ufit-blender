import bpy


class PFuFit(bpy.types.AddonPreferences):
    bl_idname = 'ufit'  # must be small letters

    username: bpy.props.StringProperty(
        name="Username",
        description="Your uFit username",
        default=""
    )

    password: bpy.props.StringProperty(
        name="Password",
        description="Your uFit password",
        default="",
        subtype="PASSWORD"
    )

    last_authentication: bpy.props.StringProperty(
        name="Last Authentication",
        description="Last Authentication",
        default="",
        subtype="PASSWORD"
    )

    offline_transtibial_count: bpy.props.IntProperty(
        name="Transtibial Count",
        description="Transtibial Count",
        default=0,
    )

    offline_transfemoral_count: bpy.props.IntProperty(
        name="Transfemoral Count",
        description="Transfemoral Count",
        default=0,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Platform Authentication")
        layout.prop(self, "username")
        layout.prop(self, "password")
