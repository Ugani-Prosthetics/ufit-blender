import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox, get_label_multiline


class UIExportDevice(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_export_device):
        ufit_obj = bpy.data.objects['uFit']
        scene = context.scene
        layout = self.layout

        if context.scene.ufit_socket_or_milling == 'socket':
            box0 = layout.box()
            box0_row0 = box0.row()
            box0_row0.prop(scene, 'ufit_show_original', text="Show Scan")

            if context.scene.ufit_device_type not in ('transtibial', 'transfemoral'):
                box1 = layout.box()
                box1_row0 = box1.row()
                box1_row1 = box1.row()
                box1_row1.enabled = context.scene.ufit_smooth_borders
                box1_row0.prop(scene, 'ufit_smooth_borders', text="Smooth Borders")
                box1_row1.prop(ufit_obj.modifiers['Corrective Smooth'], 'iterations', text='Smooth Factor')

            if context.scene.ufit_total_contact_socket:
                box2 = layout.box()
                box2_row0 = box2.row()
                box2_row0.prop(scene, 'ufit_show_inner_part', text="Show Inner Part")

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_export_device, next_text="Export")


class UIFinished(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_restart):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        get_label_multiline(
            context=context,
            text=f'Your model is ready for printing. Go to your patient folder to find the exported stl file.',
            parent=box0
        )

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_restart, next_text="Finish")
