from django.conf.urls import url, include

from . import views

app_name = 'tracker'

dashboard_patterns = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
    url(r'^objectives/$', views.dashboard_objectives, name="dashboard/objectives"),
    url(r'^time-entries/$', views.dashboard_time_entries, name="dashboard/time-entries"),
]

objective_patterns = [
    url(r'^$', views.ObjectiveView.as_view(), name="objective"),
    url(r'^entry/$', views.TimeEntryObjectiveFormView.as_view(), name="objective/entry"),
]

api_patterns = [
    url(r'^objectives/$', views.json_get_objectives, name='api/objectives'),
    url(r'^entry/$', views.json_create_entry, name='api/add_entry'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signin/', views.SigninView.as_view(), name='signin'),
    url(r'^entry/$', views.TimeEntryFormView.as_view(), name="entry"),
    url(r'^dashboard/', include(dashboard_patterns)),
    url(r'^objective/(?P<objective>[0-9]+)/', include(objective_patterns)),
    url(r'^api/', include(api_patterns)),
]
