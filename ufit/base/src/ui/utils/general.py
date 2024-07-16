import textwrap


class UFitPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'uFit Premium'

    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):  # function almost always overwritten by child class
        return context.object is not None


def get_standard_navbox(layout, prev_operator_name, next_operator_name, back_text="Back", next_text="Next"):
    nav_box = layout.box().row()
    nav_box.operator(prev_operator_name, text=back_text)
    nav_box.operator(next_operator_name, text=next_text)

    return nav_box


def get_label_multiline(context, text, parent):
    chars = int(context.region.width / 7) + 1   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)

