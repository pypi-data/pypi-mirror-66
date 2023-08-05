from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, Regexp
from projects_base.base import conf


class FormManager:
    forms = {}

    def __init__(self, default_class=None, default_module=None, custom_key=None):
        # Add the package config form class if defined

        if default_class and default_module:
            self.register_form_class(
                default_class, module=default_module, custom_key=custom_key
            )

    def register_form_class(self, class_name, module=None, custom_key=None):
        # Look in external module if provided
        if module:
            module_ = __import__(module)
            class_ = getattr(module_, class_name)
        else:
            module_ = __import__("base")
            class_ = getattr(module_, class_name)

        if custom_key:
            self.forms[custom_key] = class_
        else:
            self.forms[class_] = class_

    def get_form_class(self, cls_key):
        if self.forms and cls_key in self.forms:
            return self.forms[cls_key]


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
