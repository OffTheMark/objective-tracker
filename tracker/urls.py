from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signin/', views.SigninView.as_view(), name='signin'),
    url(r'^entry/$', views.TimeEntryFormView.as_view(), name="entry"),
    url(r'^dashboard/$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^dashboard/objectives/$', views.dashboard_objectives, name="dashboard/objectives"),
    url(r'^dashboard/time-entries/$', views.dashboard_time_entries, name="dashboard/time-entries"),
    url(r'^objective/(?P<pk>[0-9]+)/$', views.ObjectiveView.as_view(), name="objective"),
    url(r'^objective/(?P<objective>[0-9]+)/entry/$', views.TimeEntryObjectiveFormView.as_view(), name="objective/entry"),
    url(r'^json/objectives/$', views.json_get_objectives, name="json/objectives"),
]
