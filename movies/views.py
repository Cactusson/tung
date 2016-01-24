from operator import itemgetter

from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.views import generic

from braces import views

from . import forms, models


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

        all_movie_letters_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
        movie_letters_ru = []
        for letter in all_movie_letters_ru:
            if movies.filter(first_letter=letter):
                movie_letters_ru.append(letter)
        context['all_movie_letters_ru'] = list(all_movie_letters_ru)
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

        all_person_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
        person_letters = []
        for letter in all_person_letters:
            if people.filter(first_letter=letter):
                person_letters.append(letter)
        context['all_person_letters'] = list(all_person_letters)
        context['person_letters'] = person_letters

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
    generic.ListView
):
    model = models.Movie
    template_name = 'movies/index.html'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        queryset = queryset.order_by('-first_date')[:10]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)

        years = []
        dates = [movie.dates for movie in movies]
        for date_string in dates:
            for date in date_string.split(', '):
                year = date.split('-')[0]
                if year not in years:
                    years.append(year)

        context['years'] = years
        return context


class MovieListView(
    LettersNavigationMixin,
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
    LettersNavigationMixin,
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
        for actor in movie.actors_list.split(', '):
            actors_list.append(actors.get(name=actor))
        context['actors_list'] = actors_list

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
    LettersNavigationMixin,
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
        people = people.annotate(acted_count=Count('starred_in'))
        people = people.annotate(directed_count=Count('directed'))
        context['people'] = people
        return context


class PersonDetailView(
    RestrictToUserMixin,
    LettersNavigationMixin,
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
        return context


class PersonDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.Person
    success_url = reverse_lazy('movies:person_list')


class YearListView(
    LettersNavigationMixin,
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
    LettersNavigationMixin,
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
    LettersNavigationMixin,
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
    LettersNavigationMixin,
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
    RestrictToUserMixin,
    LettersNavigationMixin,
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


class GradeDetailView(
    RestrictToUserMixin,
    LettersNavigationMixin,
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
    RestrictToUserMixin,
    LettersNavigationMixin,
    generic.TemplateView
):
    template_name = 'movies/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        movies = models.Movie.objects.filter(user=self.request.user)
        total_movies = len(movies)
        context['total_movies'] = total_movies
        counts = [0 for _ in range(10)]
        for movie in movies:
            counts[movie.grade - 1] += 1
        counts.reverse()
        grades = range(10, 0, -1)
        grades_counts = zip(grades, counts)

        context['grades_counts'] = grades_counts
        return context
