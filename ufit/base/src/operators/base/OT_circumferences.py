import bpy
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.checkpoints import set_assistance, set_modal_step, close_modal_step
from .....base.src.operators.core.prepare import add_circumference, add_other_circumferences, highlight_circumferences


class OTCircumference(OTBase):
    @classmethod
    def poll(cls, context):
        for obj in bpy.data.objects:
            if obj.name.startswith("Circum_"):
                return False
        return True

    def main_func(self, context):
        add_circumference(context, i=0)


class OTCircumferencesCalc(OTBase):
    @classmethod
    def poll(cls, context):
        if 'Circum_0' in bpy.data.objects and 'Circum_1' not in bpy.data.objects:
            return True
        return False

    def main_func(self, context):
        add_other_circumferences(context)

        set_modal_step(context, modal_func=highlight_circumferences, name='highlight_circumferences')
        set_assistance('highlight_circumferences', self.get_path_consts(), self.get_ui_consts())


class OTCircumferencesDone(OTBase):
    @classmethod
    def poll(cls, context):
        if 'Circum_0' not in bpy.data.objects or \
                ('Circum_0' in bpy.data.objects and 'Circum_1' in bpy.data.objects):
            return True
        return False

    def main_func(self, context):
        pass


class OTCircumferencesHighlight(OTBase):
    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def main_func(self, context):
        if not context.scene.ufit_circums_highlighted:
            set_modal_step(context, modal_func=highlight_circumferences, name='highlight_circumferences')
            set_assistance('highlight_circumferences', self.get_path_consts(), self.get_ui_consts())
        else:
            # we don't have to set the tt_circums_highlighted to false because it is still in
            # the context of the previous file
            close_modal_step(context, self.get_path_consts(), self.get_ui_consts())
