"""
Method advisors are effectively function advisors and are covered there.
"""
from ..advisors import filt_block_advisor
from .. import conf
from ..utils import get_nice_str_list, layout_comment as layout

CLASS_XPATH = ('descendant-or-self::Class')

@filt_block_advisor(xpath=CLASS_XPATH, warning=True)
def one_method_classes(block_dets, *, repeated_message=False):
    """
    Look for decorators and explain some options for improving them.
    """
    class_els = block_dets.element.xpath(CLASS_XPATH)
    if not class_els:
        return None
    brief_comment = 'Classy!'
    message = {
        conf.BRIEF: brief_comment,
    }
    return message
