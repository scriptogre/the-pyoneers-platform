from django.conf import settings
from django.shortcuts import redirect
from django.utils.html import format_html
from wagtail import hooks


@hooks.register("insert_global_admin_css")
def import_fontawesome_stylesheet():
    elem = f'<link rel="stylesheet" href="{settings.STATIC_URL}css/font-awesome.min.css">'
    return format_html(elem)


@hooks.register("after_edit_page")
def redirect_after_page_edit(request, page):
    """
    Redirects to the admin page edit view after editing a page.

    This makes it easier during development to edit a page and see the changes.
    The default Wagtail behaviour is to redirect to the explorer.
    """
    return redirect("/admin/pages/" + str(page.id) + "/edit/")
