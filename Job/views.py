from django.shortcuts import render
from .models import Job
from django.views.generic import ListView


def jobs_home(request):
    return render(request, 'job/jobs_home.html')


class Joblistview(ListView):
    model = Job
    template_name = 'job/job_.html'
    context_object_name = 'jobs'
    ordering = ['-created_on']


