from wagtail import hooks
from django.conf import settings
from django.utils.html import format_html


@hooks.register("insert_global_admin_css")
def import_fontawesome_stylesheet():
    elem = f'<link rel="stylesheet" href="{settings.STATIC_URL}css/font-awesome.min.css">'
    return format_html(elem)
