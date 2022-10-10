from colorsys import hsv_to_rgb


def get_cls_attr(cls, attr, change_attr=None):

    if hasattr(cls, attr):
        return getattr(cls, attr)
    else:
        return change_attr


def string_to_int(val):
    try:
        val = int(val)
    except ValueError:
        return None

    return val


def string_to_positive_int(val):
    try:
        val = int(val)
    except ValueError:
        return -1

    return val
