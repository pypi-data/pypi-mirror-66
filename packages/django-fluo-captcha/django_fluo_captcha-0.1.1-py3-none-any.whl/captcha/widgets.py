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
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . import settings
from .utils import encode, get_new_values

OPERATORS = list(settings.OPERATIONS)


class CaptchaWidget(forms.MultiWidget):
    values = settings.NUMBERS
    operators = OPERATORS
    question = _("Are you human? What is {x} {operator} {y}? ")
    template_name = "captcha/widgets/captcha.html"

    def __init__(self, values=None, operators=None, question=None, question_class=None, attrs=None):
        self.values = values or self.values
        self.operators = operators or self.operators
        x, y, operator, self.answer = get_new_values(self.values, self.operators)
        self.question = self.render_question(x, y, operator)

        widget_attrs = {"size": "5"}
        widget_attrs.update(attrs or {})
        widgets = [forms.TextInput(attrs=widget_attrs), forms.HiddenInput()]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        return [None, encode(self.answer)]

    def render_question(self, x, y, operator):
        return self.question.format(x=x, operator=operator, y=y)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["question"] = self.question
        return context
