# cutout style free / straight
def cutout_style_free_condition(context):
    return context.scene.ufit_cutout_style == "free"


def cutout_style_straight_condition(context):
    return context.scene.ufit_cutout_style == "straight"


# socket / milling
def socket_condition(context):
    return context.scene.ufit_socket_or_milling == "socket"


def milling_condition(context):
    return context.scene.ufit_socket_or_milling == "milling"


# scale / no scale
def scale_condition(context):
    return context.scene.ufit_liner_scaling != 0


def no_scale_condition(context):
    return context.scene.ufit_liner_scaling == 0
