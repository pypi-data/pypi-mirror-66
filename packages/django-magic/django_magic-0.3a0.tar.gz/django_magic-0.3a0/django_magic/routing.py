from django.urls import path
from django.views.generic.base import TemplateView


class RoutingManager():
    def __init__(self, views):
        self.views = views


    # 'foo_bar' to 'foo-bar/'
    def get_url_from_name(name):
        return name.replace("_", "-") + "/"


    # 'foo_bar' to 'FooBarView'
    def get_view_from_name(name):
        word_array = name.split("_")
        upper_camel_cased = "".join(x.title() for x in word_array)
        return upper_camel_cased + "View"


    def get_view(self, name, view=None, url=None):
        return path(
            url if url or url == "" else get_url_from_name(name),
            view if view else getattr(self.views, get_view_from_name(name)),
            name=name
        )


    def get_class_view(self, name, view=None, url=None):
        view_function = view if view else getattr(self.views, get_view_from_name(name))
        return path(
            url if url or url == "" else get_url_from_name(name),
            view_function.as_view(),
            name=name
        )


    def get_template_view(name):
        return path(
            get_url_from_name(name),
            TemplateView.as_view(template_name=name + ".html"),
            name=name
        )

