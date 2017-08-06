__authors__ = "Zach Mott, David Fox, Jason Dunn"

from django.http import HttpResponse

def submit_code(request, code):
    try:
        assignment = Assignment.get(code)
    except (KeyError):
        return