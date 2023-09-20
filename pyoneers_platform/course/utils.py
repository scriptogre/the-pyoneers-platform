from wagtail.models import Page


def get_current_module(page: Page):
    """
    Returns the current module given a Page object.

    Parameters:
        page (Page): The current Wagtail Page object.

    Returns:
        Module: The current module.
    """
    from pyoneers_platform.course.models import Module

    if isinstance(page.specific, Module):
        return page.specific
    else:
        return page.get_parent().specific


def get_module_chapters(module: "Module"):
    from pyoneers_platform.course.models import Chapter

    """
    Returns a list of chapters for a given module.

    Parameters:
        module (Module): Module to get chapters for.

    Returns:
        list: List of chapters for the given module.
    """
    return Chapter.objects.child_of(module).live().order_by("path")
