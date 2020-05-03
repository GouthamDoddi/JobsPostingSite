from django.urls import path
from .views import Joblistview, jobs_home

urlpatterns = [
    path('list/', Joblistview.as_view(), name='jobs_list'),
]
