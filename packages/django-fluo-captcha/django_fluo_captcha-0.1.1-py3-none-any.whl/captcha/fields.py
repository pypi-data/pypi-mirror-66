# Copyright (C) 2007-2020, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .utils import encode
from .widgets import CaptchaWidget


class CaptchaField(forms.MultiValueField):
    widget = CaptchaWidget
    widget_params = ["values", "operators", "question", "question_class"]
    default_error_messages = {
        "invalid": _("Please check your math and try again."),
        "invalid_number": _("Enter a whole number."),
    }

    def __init__(self, *args, **kwargs):
        widget = self.get_widget(kwargs)
        super().__init__(fields=(), widget=widget, *args, **kwargs)

        error_messages = {
            "invalid": self.error_messages["invalid_number"],
        }
        self.fields = [
            forms.IntegerField(required=False, error_messages=error_messages, localize=self.localize),
            forms.CharField(required=False),
        ]

    def compress(self, data_list):
        if data_list:
            answer, hashed = data_list
            hashed_answer = encode(answer)
            if hashed_answer != hashed:
                raise ValidationError(self.error_messages["invalid"])
        return None

    def get_widget_params(self, kwargs):
        params = {}
        for key in self.widget_params:
            if key in kwargs:
                params[key] = kwargs.pop(key)
        return params

    def get_widget(self, kwargs):
        params = self.get_widget_params(kwargs)
        widget = kwargs.pop("widget", None)
        if widget and params:
            msg = "{} must be omitted when widget is provided for {}.".format(
                " and ".join(list(params)), self.__class__.__name__,
            )
            raise TypeError(msg)
        elif not widget:
            widget = self.widget(**params)
        return widget
