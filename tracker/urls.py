from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signin/', views.SigninView.as_view(), name='signin'),
    url(r'^entry/$', views.TimeEntryView.as_view(), name="entry"),
    url(r'^dashboard/$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^dashboard/objectives/$', views.objectives, name="dashboard/objectives"),
    url(r'^dashboard/time-entries/$', views.time_entries, name="dashboard/time-entries"),
]
