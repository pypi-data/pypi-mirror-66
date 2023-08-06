import sys
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, Regexp
from projects_base.base import conf


class FormManager:
    forms = {}

    def __init__(self, default_class=None, default_module=None, custom_key=None):
        # Add the package config form class if defined
        if default_class and default_module:
            self.add_module_class(default_module, default_class, custom_key=custom_key)

    def add_module_class(self, module_name, class_name, custom_key=None):
        if custom_key:
            self.forms[custom_key] = [module_name, class_name]
        else:
            self.forms[class_name] = [module_name, class_name]

    def get_form_class(self, key):
        module_, class_ = self.forms[key]
        imported_module_ = __import__(module_)
        form_class = getattr(imported_module_, class_)
        return form_class


class TagsSearchForm(FlaskForm):
    tag = StringField(
        "Tags Search",
        validators=[
            Optional(),
            Regexp(
                r"^[\w,:_\-* ]*$",
                message="Allowed tag characters "
                "include letters spaces and"
                ", : _ - *",
            ),
        ],
    )
