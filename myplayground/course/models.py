from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from myplayground.home.models import HomePage


class Module(Page):
    parent_page_types = [HomePage]
    show_in_menus_default = True

    description = models.TextField()

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title
