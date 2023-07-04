import bpy
from .....base.src.ui.utils.general import UFitPanel
from ...transfemoral_constants import tf_ui_consts
from .....base.src.ui.utils.general import get_standard_navbox


class UIMoveConnectorTF(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_tf_move_connector"
    bl_label = tf_ui_consts['workflow']['align']['ui_name']

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        active_object = context.active_object

        # row.label(text="Move and scale until precisely located:")
        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, 'ufit_x_ray')

        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row1 = box1.row()
        box1_row2 = box1.row()
        box1_row1.prop(scene, 'ufit_alignment_object', expand=True)

        if context.scene.ufit_alignment_object == 'uFit':
            box1_row0.prop(scene, 'ufit_show_connector')
            box1_row2.prop(scene, 'ufit_alignment_tool', expand=True)

            box2 = layout.box()
            box2_row0 = box2.row()
            box2_row1 = box2.row()
            box2_row2 = box2.row()
            box2_row3 = box2.row()
            box2_row0.label(text='Rotate')
            box2_row1.prop(active_object, 'rotation_euler', index=2, text="Baseline")
            box2_row2.prop(active_object, 'rotation_euler', index=0, text="Flexion/Extension")
            box2_row3.prop(active_object, 'rotation_euler', index=1, text="Adduction/Abduction")

        box3 = layout.box()
        box3_row0 = box3.row()
        box3_row1 = box3.row()
        box3_row2 = box3.row()
        box3_row3 = box3.row()
        box3_row0.label(text='Translate')
        if context.scene.ufit_alignment_object == 'uFit':
            box3_row1.prop(active_object, 'location', index=2, text="Patella - Ground")
        else:
            box3_row1.prop(active_object, 'location', index=2, text="Connector - Ground")
        box3_row2.prop(active_object, 'location', index=0, text="Lateral/Medial")
        box3_row3.prop(active_object, 'location', index=1, text="Posterior/Anterior")

        get_standard_navbox(self.layout, "ufit_operators.prev_step", "tf_operators.save_alignment")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'align'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
