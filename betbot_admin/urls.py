from django.conf.urls import url
from django.contrib import admin
from app.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main, name='main'),
    url(r'^authorization/', authorization, name='authorization'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^users', UsersView.as_view(), name='users'),
    url(r'^user/(?P<id>\d+)', UserView.as_view(), name='user'),
    url(r'^edit_user/', edit_user, name='edit_user'),
    url(r'^events', EventsView.as_view(), name='events'),
    url(r'^event/(?P<id>\d+)', EventView.as_view(), name='event'),
    url(r'^edit_event/', edit_event, name='edit_event'),
    url(r'^add_event/', add_event, name='add_event'),
    url(r'^set_crore/', set_score, name='set_score'),
    url(r'^delete_event/', delete_event, name='delete_event'),
    url(r'^close_event/', close_event, name='close_event'),
    url(r'^requests', RequestsView.as_view(), name='requests'),
    url(r'^teams', TeamsView.as_view(), name='teams'),
    url(r'^add_team/', add_team, name='add_team'),
    url(r'^delete_team/', delete_team, name='delete_team'),
    url(r'^team/(?P<id>\d+)', TeamView.as_view(), name='team'),
]
