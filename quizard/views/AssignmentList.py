# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django.views import generic

from quizard.models import Assignment


class AssignmentList(generic.ListView):
    model = Assignment
    context_object_name = 'assignments'
    template_name = 'quizard/assignment_list.html'

    def get_context_data(self, **kw):
        context = super(AssignmentList, self).get_context_data(**kw)
        context.update(self.kwargs)
        return context

    def get_queryset(self):
        queryset = super(AssignmentList, self).get_queryset()

        return queryset.filter(
            school__name__iexact=self.kwargs['school'],
            created_by__last_name__iexact=self.kwargs['teacher']
        )
