__authors__ = "Zach Mott, David Fox, Jason Dunn"

from django.http import HttpResponse
from django.shortcuts import render

from quizard.forms.AssignmentSearchForm import AssignmentSearchForm
from quizard.forms.CodeForm import CodeForm

def main(request):

    codeform = CodeForm()
    searchform = AssignmentSearchForm()

    return render(request, "main.html",
                  {'code': codeform, 'search': searchform})