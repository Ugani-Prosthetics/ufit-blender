from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_circumferences import (
    OTCircumference,
    OTCircumferencesCalc,
    OTCircumferencesDone,
    OTCircumferencesHighlight
)


class OTCircumferenceTT(OTBaseTT, OTCircumference):
    """Tooltip"""
    bl_idname = "tt_operators.add_circumference"
    bl_label = "Add"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='circumference_add')


class OTCircumferencesCalcTT(OTBaseTT, OTCircumferencesCalc):
    """Tooltip"""
    bl_idname = "tt_operators.circumferences_calc"
    bl_label = "Calculate Circumferences"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='circumferences_calc')


class OTCircumferencesDoneTT(OTBaseTT, OTCircumferencesDone):
    """Tooltip"""
    bl_idname = "tt_operators.circumferences_done"
    bl_label = "Done"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='circumferences_done')


class OTCircumferencesHighlightTT(OTBaseTT, OTCircumferencesHighlight):
    """Tooltip"""
    bl_idname = "tt_operators.circumferences_highlight"
    bl_label = "Highlight Circumferences"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='circumferences_highlight')
