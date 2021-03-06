from django import forms
from django.db import models
from django.core.validators import RegexValidator

from .constants import *


class TextareaField(forms.CharField):
    """
    A textarea with support for GitHub-Flavored Markdown. Exists mostly just to
    add a standard help_text.
    """

    widget = forms.Textarea

    def __init__(self, *args, **kwargs):
        required = kwargs.pop("required", False)
        super().__init__(required=required, *args, **kwargs)


class ColorSelect(forms.Select):
    """
    Colorize each <option> inside a select widget.
    """

    option_template_name = "widgets/colorselect_option.html"

    def __init__(self, *args, **kwargs):
        from .forms import add_blank_choice

        kwargs["choices"] = add_blank_choice(COLOR_CHOICES)
        super().__init__(*args, **kwargs)
        self.attrs["class"] = "custom-select2-color-picker"


class ColorField(models.CharField):
    default_validators = [
        RegexValidator(
            regex="^[0-9a-f]{6}$",
            message="Enter a valid hexadecimal RGB color code.",
            code="invalid",
        )
    ]
    description = "A hexadecimal RGB color code"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = ColorSelect
        return super().formfield(**kwargs)


class CommentField(TextareaField):
    """
    A textarea with support for GitHub-Flavored Markdown. Note that it does not
    actually do anything special. It just here to add a help text.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            label="Comments",
            help_text='Styling with <a href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet" target="_blank"><i class="fab fa-markdown"></i> Markdown</a> is supported',
            *args,
            **kwargs
        )


class PasswordField(forms.CharField):
    """
    A field used to enter password. The field will hide the password unless the
    reveal button is clicked.
    """

    def __init__(self, password_source="password", render_value=False, *args, **kwargs):
        widget = kwargs.pop("widget", forms.PasswordInput(render_value=render_value))
        label = kwargs.pop("label", "Password")
        help_text = kwargs.pop(
            "help_text",
            "It can be a clear text password or an "
            "encrypted one. It really depends on how you "
            "want to use it. Be aware that it is stored "
            "without encryption in the database.",
        )
        super().__init__(
            widget=widget, label=label, help_text=help_text, *args, **kwargs
        )
        self.widget.attrs["password-source"] = password_source


class SlugField(forms.SlugField):
    """
    An improved SlugField that allows to be automatically generated based on a
    field used as source.
    """

    def __init__(self, slug_source="name", *args, **kwargs):
        label = kwargs.pop("label", "Slug")
        help_text = kwargs.pop(
            "help_text", "Friendly unique shorthand used for URL and config"
        )
        super().__init__(label=label, help_text=help_text, *args, **kwargs)
        self.widget.attrs["slug-source"] = slug_source
