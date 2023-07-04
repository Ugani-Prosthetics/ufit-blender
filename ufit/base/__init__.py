from .src.preferences import preferences
from .src.properties import properties
from .src.operators import operators
from .src.ui import ui


def register():
    preferences.register()
    properties.register()
    operators.register()
    ui.register()


def unregister():
    preferences.unregister()
    properties.unregister()
    operators.unregister()
    ui.unregister()
