__authors__ = "Zach Mott, David Fox, Jason Dunn"

from django import forms

class AssignmentSearchForm(forms.Form):
    teacher = forms.CharField(max_length=64)
    school = forms.CharField(max_length=64)