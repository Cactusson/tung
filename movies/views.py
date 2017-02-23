from operator import itemgetter

from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views import generic

from braces import views

from . import forms, models


RU = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'


class RestrictToUserMixin(
    views.LoginRequiredMixin
):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class LettersNavigationMixin(
    views.LoginRequiredMixin
):

    def get_context_data(self, **kwargs):
        context = super(LettersNavigationMixin, self).get_context_data(
            **kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)
        people = models.Person.objects.filter(user=self.request.user)

        movie_letters_ru = []
        for letter in RU:
            if movies.filter(first_letter=letter):
                movie_letters_ru.append(letter)
        context['all_movie_letters_ru'] = list(RU)
        context['movie_letters_ru'] = movie_letters_ru

        numbers = [str(n) for n in range(10)]
        all_movie_letters_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        movie_letters_en = []
        for letter in all_movie_letters_en:
            if movies.filter(first_letter=letter):
                movie_letters_en.append(letter)
        if movies.filter(first_letter__in=numbers):
            movie_letters_en.append('0-9')
        context['all_movie_letters_en'] = list(all_movie_letters_en) + ['0-9']
        context['movie_letters_en'] = movie_letters_en

        person_letters = []
        for letter in RU:
            if people.filter(first_letter=letter):
                person_letters.append(letter)
        context['all_person_letters'] = list(RU)
        context['person_letters'] = person_letters

        return context


class YearsNavigationMixin(
    views.LoginRequiredMixin
):
    def get_context_data(self, **kwargs):
        context = super(YearsNavigationMixin, self).get_context_data(
            **kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)
        years = []
        dates = [movie.dates for movie in movies]
        for date_string in dates:
            for date in date_string.split(', '):
                year = str(date.split('-')[0])
                if year not in years:
                    years.append(year)
        years.sort()
        context['years'] = years
        return context


class LetterFilterMixin():
    def get_queryset(self):
        queryset = super(LetterFilterMixin, self).get_queryset()
        letter = self.request.GET.get('letter', '')
        if letter:
            if letter == '0-9':
                numbers = [str(num) for num in range(10)]
                queryset = queryset.filter(first_letter__in=numbers)
            else:
                queryset = queryset.filter(first_letter=letter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LetterFilterMixin, self).get_context_data(**kwargs)
        letter = self.request.GET.get('letter', '')
        context['letter'] = letter
        return context


class IndexView(
    RestrictToUserMixin,
    LettersNavigationMixin,
    YearsNavigationMixin,
    generic.ListView
):
    model = models.Movie
    template_name = 'movies/index.html'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        queryset = queryset.order_by('-first_date')[:10]
        return queryset


class MovieListView(
    generic.TemplateView
):
    template_name = 'movies/movie_list.html'

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        letter = self.request.GET.get('letter', '')
        context['letter'] = letter
        movies = models.Movie.objects.filter(user=self.request.user)
        if letter:
            if letter == '0-9':
                numbers = [str(num) for num in range(10)]
                movies = movies.filter(first_letter__in=numbers)
            else:
                movies = movies.filter(first_letter=letter)
        context['movies'] = movies
        return context


class MovieDetailView(
    RestrictToUserMixin,
    generic.DetailView
):
    model = models.Movie

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        movie = self.get_object()

        directors = movie.directors.all()
        directors_list = []
        for director in movie.directors_list.split(', '):
            directors_list.append(directors.get(name=director))
        context['directors_list'] = directors_list

        actors = movie.actors.all()
        actors_list = []
        if movie.actors_list:
            for actor in movie.actors_list.split(', '):
                actors_list.append(actors.get(name=actor))
            context['actors_list'] = actors_list
        else:
            pass

        dates = movie.dates.split(', ')
        context['dates_list'] = dates

        return context


class MovieCreateView(
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.CreateView
):
    form_class = forms.MovieForm
    model = models.Movie
    headline = 'Create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(MovieCreateView, self).form_valid(form)


class MovieUpdateView(
    RestrictToUserMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
):
    form_class = forms.MovieForm
    model = models.Movie
    headline = 'Update'


class MovieDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.Movie
    success_url = reverse_lazy('movies:movie_list')


class PersonListView(
    generic.TemplateView
):
    template_name = 'movies/person_list.html'

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        letter = self.request.GET.get('letter', '')
        context['letter'] = letter
        people = models.Person.objects.filter(user=self.request.user)
        if letter:
            if letter == '0-9':
                numbers = [str(num) for num in range(10)]
                people = people.filter(first_letter__in=numbers)
            else:
                people = people.filter(first_letter=letter)
        # people = people.order_by('name')
        people = people.annotate(acted_count=Count(
            'starred_in', distinct=True))
        people = people.annotate(directed_count=Count(
            'directed', distinct=True))
        context['people'] = people
        return context


class PersonDetailView(
    RestrictToUserMixin,
    LetterFilterMixin,
    generic.DetailView
):
    model = models.Person

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        directed = self.object.directed.order_by('year')
        context['directed'] = directed
        starred_in = self.object.starred_in.order_by('year')
        context['starred_in'] = starred_in
        created = self.object.created.order_by('name')
        context['created'] = created
        shows = [season.tvshow for season in
                 self.object.tvshowseason_starred_in.all()]
        shows = list(set(shows))
        context['tvshows_starred_in'] = shows
        return context


class PersonDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.Person
    success_url = reverse_lazy('movies:person_list')


class YearListView(
    generic.TemplateView
):
    template_name = 'movies/year_list.html'

    def get_context_data(self, **kwargs):
        context = super(YearListView, self).get_context_data(**kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)
        years = list(set(movie.year for movie in movies))
        years.sort(reverse=True)

        years_counts = []
        for year in years:
            count = len(list(movies.filter(year=year)))
            years_counts.append(count)
        context['years'] = zip(years, years_counts)
        return context


class YearDetailView(
    generic.TemplateView
):
    template_name = 'movies/year_detail.html'

    def get_context_data(self, **kwargs):
        context = super(YearDetailView, self).get_context_data(**kwargs)
        year = self.request.GET.get('year', '')
        context['year'] = year
        movies = models.Movie.objects.filter(user=self.request.user)
        movies = movies.filter(year=year)
        context['movies'] = movies

        return context


class GenreListView(
    generic.TemplateView
):
    template_name = 'movies/genre_list.html'

    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)
        genres = list(set(movie.genre for movie in movies))
        genres.sort()

        genres_counts = []
        for genre in genres:
            count = len(list(movies.filter(genre=genre)))
            genres_counts.append(count)
        context['genres'] = zip(genres, genres_counts)
        return context


class GenreDetailView(
    generic.TemplateView
):
    template_name = 'movies/genre_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        genre = self.request.GET.get('genre', '')
        context['genre'] = genre
        movies = models.Movie.objects.filter(user=self.request.user)
        movies = movies.filter(genre=genre)
        context['movies'] = movies

        return context


class CollView(
    YearsNavigationMixin,
    generic.TemplateView
):
    template_name = 'movies/coll.html'

    def get_context_data(self, **kwargs):
        context = super(CollView, self).get_context_data(**kwargs)
        # try this approach in Year and Genre:
        current_year = self.kwargs['year']
        context['year'] = current_year

        months = range(1, 13)
        months_items = {month: [] for month in months}

        movies = models.Movie.objects.filter(user=self.request.user)
        for movie in movies:
            for date in movie.dates.split(', '):
                year, month, day = [int(n) for n in date.split('-')]
                if year == int(current_year):
                    months_items[month].append((day, movie))

        packed_items = {}
        for month in months:
            items = []
            row = []
            months_items[month].sort(key=itemgetter(0))
            for day, item in months_items[month]:
                row.append(item)
                if len(row) == 5:
                    items.append(row)
                    row = []
            if row:
                items.append(row)
            packed_items[month] = items[:]

        context['packed_items'] = packed_items

        return context


class CollStatsView(
    YearsNavigationMixin,
    generic.TemplateView
):
    template_name = 'movies/coll_stats.html'

    def get_context_data(self, **kwargs):
        context = super(CollStatsView, self).get_context_data(**kwargs)
        current_year = self.kwargs['year']
        context['year'] = current_year

        movies = models.Movie.objects.filter(user=self.request.user)
        all_movies = []
        total_movies = 0
        new_movies = 0
        for movie in movies:
            for date in movie.dates.split(', '):
                year, month, day = [int(n) for n in date.split('-')]
                if year == int(current_year):
                    total_movies += 1
            first_year = movie.first_date.year
            if first_year == int(current_year):
                new_movies += 1
                all_movies.append(movie)
        context['total_movies'] = total_movies
        context['new_movies'] = new_movies
        context['old_movies'] = total_movies - new_movies

        years = {}
        for movie in all_movies:
            if movie.year not in years:
                years[movie.year] = 1
            else:
                years[movie.year] += 1
        years = [(years[yr], yr) for yr in years]
        years.sort(reverse=True)
        context['top_years'] = years[:5]

        genres = {}
        for movie in all_movies:
            if movie.genre not in genres:
                genres[movie.genre] = 1
            else:
                genres[movie.genre] += 1
        genres = [(genres[genre], genre) for genre in genres]
        genres.sort(reverse=True)
        context['top_genres'] = genres[:5]

        min_grade = 9
        top_movies = []
        for movie in all_movies:
            if movie.grade >= min_grade:
                top_movies.append(movie)
        top_movies.sort(reverse=True, key=lambda m: m.grade)
        context['top_movies'] = top_movies

        return context


class GradeDetailView(
    RestrictToUserMixin,
    generic.ListView
):
    template_name = 'movies/grade_detail.html'
    model = models.Movie

    def get_queryset(self):
        queryset = super(GradeDetailView, self).get_queryset()
        grade = self.kwargs['grade']
        queryset = queryset.filter(grade=grade)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GradeDetailView, self).get_context_data(**kwargs)
        grade = self.kwargs['grade']
        context['grade'] = grade
        return context


class StatsView(
    YearsNavigationMixin,
    generic.TemplateView
):
    template_name = 'movies/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)
        total_movies = len(movies)
        context['total_movies'] = total_movies

        rewatched_movies = 0
        rewatched_max_amount = 1
        rewatched_max_movies = []
        for movie in movies:
            watches = len(movie.dates.split(', '))
            if watches > 1:
                rewatched_movies += 1
                if watches > rewatched_max_amount:
                    rewatched_max_amount = watches
                    rewatched_max_movies = [movie]
                elif watches == rewatched_max_amount:
                    rewatched_max_movies.append(movie)
        context['rewatched_movies'] = rewatched_movies
        context['rewatched_max_amount'] = rewatched_max_amount
        context['rewatched_max_movies'] = rewatched_max_movies

        years = {}
        for movie in movies:
            if movie.year not in years:
                years[movie.year] = 1
            else:
                years[movie.year] += 1
        years = [(years[yr], yr) for yr in years]
        years.sort(reverse=True)
        context['top_years'] = years[:5]

        genres = {}
        for movie in movies:
            if movie.genre not in genres:
                genres[movie.genre] = 1
            else:
                genres[movie.genre] += 1
        genres = [(genres[genre], genre) for genre in genres]
        genres.sort(reverse=True)
        context['top_genres'] = genres[:5]

        min_grade = 10
        top_movies = []
        for movie in movies:
            if movie.grade >= min_grade:
                top_movies.append(movie)
        top_movies.sort(reverse=True, key=lambda m: m.grade)
        context['top_movies'] = top_movies

        counts = [0 for _ in range(10)]
        for movie in movies:
            counts[movie.grade - 1] += 1
        counts.reverse()
        grades = range(10, 0, -1)
        grades_counts = zip(grades, counts)

        context['grades_counts'] = grades_counts
        return context


class TVShowListView(
    generic.TemplateView
):
    template_name = 'movies/tvshow_list.html'

    def get_context_data(self, **kwargs):
        context = super(TVShowListView, self).get_context_data(**kwargs)
        shows = models.TVShow.objects.filter(user=self.request.user)
        genres = ['drama', 'comedy', 'animated', 'fantastic', 'doc', 'other']
        genres_dict = {}
        for genre in genres:
            genre_shows = shows.filter(genre_family=genre)
            row = []
            genres_dict[genre] = []
            for num in range(len(genre_shows)):
                if num % 3 == 0:
                    if row:
                        genres_dict[genre].append(row)
                        row = []
                row.append(genre_shows[num])
            if row:
                genres_dict[genre].append(row)
        context['genres_dict'] = genres_dict

        years = []
        seasons = models.TVShowSeason.objects.filter(user=self.request.user)
        dates = [season.dates for season in seasons]
        for date_string in dates:
            for date in date_string.split(', '):
                year = int(date.split('-')[0])
                if year not in years:
                    years.append(year)
        years.sort()
        context['years'] = years

        return context


class TVShowDetailView(
    RestrictToUserMixin,
    generic.DetailView
):
    model = models.TVShow

    def get_context_data(self, **kwargs):
        context = super(TVShowDetailView, self).get_context_data(**kwargs)
        show = self.get_object()

        creators = show.creators.all()
        creators_list = []
        for creator in show.creators_list.split(', '):
            creators_list.append(creators.get(name=creator))
        context['creators_list'] = creators_list

        seasons = show.seasons.order_by('number')
        context['seasons'] = seasons

        return context


class TVShowCreateView(
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.CreateView
):
    form_class = forms.TVShowForm
    model = models.TVShow
    headline = 'Create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TVShowCreateView, self).form_valid(form)


class TVShowUpdateView(
    RestrictToUserMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
):
    form_class = forms.TVShowForm
    model = models.TVShow
    headline = 'Update'


class TVShowDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.TVShow
    success_url = reverse_lazy('movies:tvshow_list')


class TVShowSeasonDetailView(
    RestrictToUserMixin,
    generic.DetailView
):
    model = models.TVShowSeason

    def get_object(self):
        tvshow = get_object_or_404(models.TVShow, pk=self.kwargs['pk'])
        number = self.kwargs['url_number']
        season = get_object_or_404(models.TVShowSeason, tvshow=tvshow,
                                   url_number=number)
        return season

    def get_context_data(self, **kwargs):
        context = super(
            TVShowSeasonDetailView, self).get_context_data(**kwargs)
        season = self.get_object()

        actors = season.actors.all()
        actors_list = []
        if season.actors_list:
            for actor in season.actors_list.split(', '):
                actors_list.append(actors.get(name=actor))
            context['actors_list'] = actors_list
        else:
            pass

        dates = season.dates.split(', ')
        context['dates_list'] = dates

        return context


class TVShowSeasonCreateView(
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.CreateView
):
    form_class = forms.TVShowSeasonForm
    model = models.TVShowSeason
    headline = 'Create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.tvshow = get_object_or_404(models.TVShow,
                                               pk=self.kwargs['pk'])
        self.object.save()
        return super(TVShowSeasonCreateView, self).form_valid(form)


class TVShowSeasonUpdateView(
    RestrictToUserMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
):
    form_class = forms.TVShowSeasonForm
    model = models.TVShowSeason
    headline = 'Update'

    def get_object(self):
        tvshow = get_object_or_404(models.TVShow, pk=self.kwargs['pk'])
        number = self.kwargs['url_number']
        season = get_object_or_404(models.TVShowSeason, tvshow=tvshow,
                                   url_number=number)
        return season


class TVShowSeasonDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.TVShowSeason
    # think how to change this to movies:tvshow_detail
    success_url = reverse_lazy('movies:tvshow_list')

    def get_object(self):
        tvshow = get_object_or_404(models.TVShow, pk=self.kwargs['pk'])
        number = self.kwargs['url_number']
        season = get_object_or_404(models.TVShowSeason, tvshow=tvshow,
                                   url_number=number)
        return season


class TVCollView(
    RestrictToUserMixin,
    generic.TemplateView
):
    template_name = 'movies/tv_coll.html'

    def get_context_data(self, **kwargs):
        context = super(TVCollView, self).get_context_data(**kwargs)
        current_year = self.kwargs['year']
        context['year'] = current_year

        months = range(1, 13)
        months_items = {month: [] for month in months}

        seasons = models.TVShowSeason.objects.filter(user=self.request.user)
        for season in seasons:
            for date in season.dates.split(', '):
                year, month, day = [int(n) for n in date.split('-')]
                if year == int(current_year):
                    months_items[month].append((day, season))

        packed_items = {}
        for month in months:
            items = []
            row = []
            months_items[month].sort(key=itemgetter(0))
            for day, item in months_items[month]:
                row.append(item)
                if len(row) == 5:
                    items.append(row)
                    row = []
            if row:
                items.append(row)
            packed_items[month] = items[:]

        context['packed_items'] = packed_items

        return context
