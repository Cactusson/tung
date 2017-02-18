from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.BookListView.as_view(), name='book_list'),
    url(r'^book(?P<pk>\d+)/$', views.BookDetailView.as_view(),
        name='book_detail'),
    url(r'^create/$', views.BookCreateView.as_view(), name='book_create'),
    url(r'^book(?P<pk>\d+)/edit$', views.BookUpdateView.as_view(),
        name='book_update'),
    url(r'^book(?P<pk>\d+)/delete$', views.BookDeleteView.as_view(),
        name='book_delete'),

    url(r'^people/$', views.AuthorListView.as_view(), name='author_list'),
    url(r'^author(?P<pk>\d+)/$', views.AuthorDetailView.as_view(),
        name='author_detail'),
    url(r'^author(?P<pk>\d+)/delete$', views.AuthorDeleteView.as_view(),
        name='author_delete'),

    url(r'^years/$', views.YearListView.as_view(), name='year_list'),
    url(r'^year/$', views.YearDetailView.as_view(), name='year_detail'),

    url(r'^genres/$', views.GenreListView.as_view(), name='genre_list'),
    url(r'^genre/$', views.GenreDetailView.as_view(), name='genre_detail'),

    url(r'^coll/(?P<year>\d+)/$', views.CollView.as_view(), name='coll'),
    url(r'^coll/(?P<year>\d+)/stats$', views.CollStatsView.as_view(),
        name='coll_stats'),
]
