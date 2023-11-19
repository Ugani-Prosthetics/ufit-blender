# cutout style
def cutout_style_free_condition(context):
    return context.scene.ufit_cutout_style == "free"


def cutout_style_straight_condition(context):
    return context.scene.ufit_cutout_style == "straight"


# socket or milling
def socket_condition(context):
    return context.scene.ufit_socket_or_milling == "socket"


def milling_condition(context):
    return context.scene.ufit_socket_or_milling == "milling"
