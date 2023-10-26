import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UICleanUpScan(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_clean_up):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_clean_up)


class UIVerifyCleanUp(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_clean_up, ot_highlight_non_manifold, ot_fix_non_manifold, ot_delete_non_manifold):
        scene = context.scene
        layout = self.layout
        ufit_obj = bpy.data.objects['uFit']
        vg_groups = [vg.name for vg in ufit_obj.vertex_groups]
        nr_non_manifold = 0
        for vg in vg_groups:
            if vg.startswith("nm_"):
                nr_non_manifold += 1

        # box0
        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.label(text=f"{nr_non_manifold} Problem(s) Detected")

        box0_row1 = box0.row()
        box0_row1.operator(ot_highlight_non_manifold, text="Next Issue")
        box0_row2 = box0.row()
        box0_row2.operator(ot_fix_non_manifold, text="Fix")
        box0_row2.operator(ot_delete_non_manifold, text="Delete")
        box0_row1.enabled = True if nr_non_manifold else False

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_clean_up)
