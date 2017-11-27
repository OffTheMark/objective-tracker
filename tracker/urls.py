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
    url(r'^$', views.api_root),
    url(r'^objectives/', include([
        url(r'^$', views.ObjectiveList.as_view(), name="api/objective-list"),
        url(r'^(?P<objective_id>[0-9]+)/', include([
            url(r'^$', views.ObjectiveDetail.as_view(), name="api/objective-detail"),
            url(r'^entries/$', views.entry_list_by_objective, name="api/entry-list-by-objective")
        ])),
    ])),
    url(r'^entries/', include([
        url(r'^$', views.EntryList.as_view(), name="api/entry-list"),
        url(r'^(?P<entry_id>[0-9]+)/$', views.EntryDetail.as_view(), name="api/entry-detail"),
    ])),
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
