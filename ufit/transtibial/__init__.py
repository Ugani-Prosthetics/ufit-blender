from .src.properties import properties
from .src.workflow import operators as wf_operators
from .src.workflow import ui as wf_ui


def register():
    properties.register()
    wf_operators.register()
    wf_ui.register()


def unregister():
    properties.unregister()
    wf_operators.unregister()
    wf_ui.unregister()
