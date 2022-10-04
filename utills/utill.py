from colorsys import hsv_to_rgb


def get_cls_attr(cls, attr, change_attr=None):

    if hasattr(cls, attr):
        return getattr(cls, attr)
    else:
        return change_attr
