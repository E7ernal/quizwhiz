__authors__ = "Zach Mott, David Fox, Jason Dunn"

from django import forms

class CodeForm(forms.Form):
    assignment_code = forms.CharField(max_length=16)