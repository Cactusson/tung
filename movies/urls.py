from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.MovieListView.as_view(), name='movie_list'),
    url(r'^movie(?P<pk>\d+)/$', views.MovieDetailView.as_view(),
        name='movie_detail'),
    url(r'^add/$', views.MovieCreateView.as_view(), name='movie_create'),
    url(r'^movie(?P<pk>\d+)/edit$', views.MovieUpdateView.as_view(),
        name='movie_update'),
    url(r'^movie(?P<pk>\d+)/delete$', views.MovieDeleteView.as_view(),
        name='movie_delete'),

    url(r'^people/$', views.PersonListView.as_view(), name='person_list'),
    url(r'^person(?P<pk>\d+)/$', views.PersonDetailView.as_view(),
        name='person_detail'),
    url(r'^person(?P<pk>\d+)/delete$', views.PersonDeleteView.as_view(),
        name='person_delete'),

    url(r'^years/$', views.YearListView.as_view(), name='year_list'),
    url(r'^year/$', views.YearDetailView.as_view(), name='year_detail'),

    url(r'^genres/$', views.GenreListView.as_view(), name='genre_list'),
    url(r'^genre/$', views.GenreDetailView.as_view(), name='genre_detail'),

    url(r'^colls/(?P<year>\d+)/$', views.CollView.as_view(), name='coll'),

    url(r'^grade/(?P<grade>\d+)', views.GradeDetailView.as_view(),
        name='grade_detail'),

    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
]
