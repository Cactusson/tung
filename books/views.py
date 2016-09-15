from operator import itemgetter

from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
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


class LettersNavigationMixin(
    views.LoginRequiredMixin
):

    def get_context_data(self, **kwargs):
        context = super(LettersNavigationMixin, self).get_context_data(
            **kwargs)
        books = models.Book.objects.filter(user=self.request.user)
        authors = models.Author.objects.filter(user=self.request.user)

        book_letters_ru = []
        for letter in RU:
            if books.filter(first_letter=letter):
                book_letters_ru.append(letter)
        context['all_book_letters_ru'] = list(RU)
        context['book_letters_ru'] = book_letters_ru

        numbers = [str(n) for n in range(10)]
        all_book_letters_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        book_letters_en = []
        for letter in all_book_letters_en:
            if books.filter(first_letter=letter):
                book_letters_en.append(letter)
        if books.filter(first_letter__in=numbers):
            book_letters_en.append('0-9')
        context['all_book_letters_en'] = list(all_book_letters_en) + ['0-9']
        context['book_letters_en'] = book_letters_en

        author_letters = []
        for letter in RU:
            if authors.filter(first_letter=letter):
                author_letters.append(letter)
        context['all_author_letters'] = list(RU)
        context['author_letters'] = author_letters

        return context


class IndexView(
    LettersNavigationMixin,
    generic.TemplateView
):
    template_name = 'books/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        books = models.Book.objects.filter(user=self.request.user)

        years = []
        dates = [book.dates for book in books]
        for date_string in dates:
            for date in date_string.split(', '):
                year = int(date.split('-')[0])
                if year not in years:
                    years.append(year)
        years.sort()

        context['years'] = years
        return context


class BookListView(
    generic.TemplateView
):
    template_name = 'books/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        letter = self.request.GET.get('letter', '')
        context['letter'] = letter
        books = models.Book.objects.filter(user=self.request.user)
        if letter:
            if letter == '0-9':
                numbers = [str(num) for num in range(10)]
                books = books.filter(first_letter__in=numbers)
            else:
                books = books.filter(first_letter=letter)
        context['object_list'] = books
        return context


class BookDetailView(
    RestrictToUserMixin,
    generic.DetailView
):
    model = models.Book

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = self.get_object()

        authors = book.authors.all()
        authors_list = []
        for author in book.authors_list.split(', '):
            authors_list.append(authors.get(name=author))
        context['authors_list'] = authors_list

        dates = book.dates.split(', ')
        context['dates_list'] = dates

        return context


class BookCreateView(
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.CreateView
):
    form_class = forms.BookForm
    model = models.Book
    headline = 'Create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(BookCreateView, self).form_valid(form)


class BookUpdateView(
    RestrictToUserMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
):
    form_class = forms.BookForm
    model = models.Book
    headline = 'Update'


class BookDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.Book
    success_url = reverse_lazy('books:index')


class AuthorListView(
    generic.TemplateView
):
    template_name = 'books/author_list.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        letter = self.request.GET.get('letter', '')
        context['letter'] = letter
        people = models.Author.objects.filter(user=self.request.user)
        if letter:
            if letter == '0-9':
                numbers = [str(num) for num in range(10)]
                people = people.filter(first_letter__in=numbers)
            else:
                people = people.filter(first_letter=letter)
        # people = people.order_by('name')
        people = people.annotate(written_count=Count(
            'written', distinct=True))
        context['people'] = people
        return context


class AuthorDetailView(
    RestrictToUserMixin,
    LetterFilterMixin,
    generic.DetailView
):
    model = models.Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        written = self.object.written.order_by('year')
        context['written'] = written
        return context


class AuthorDeleteView(
    RestrictToUserMixin,
    generic.DeleteView
):
    model = models.Author
    success_url = reverse_lazy('books:person_list')


class YearListView(
    generic.TemplateView
):
    template_name = 'books/year_list.html'

    def get_context_data(self, **kwargs):
        context = super(YearListView, self).get_context_data(**kwargs)
        books = models.Book.objects.filter(user=self.request.user)
        years = list(set(book.year for book in books))
        years.sort(reverse=True)

        years_counts = []
        for year in years:
            count = len(list(books.filter(year=year)))
            years_counts.append(count)
        context['years'] = zip(years, years_counts)
        return context


class YearDetailView(
    generic.TemplateView
):
    template_name = 'books/year_detail.html'

    def get_context_data(self, **kwargs):
        context = super(YearDetailView, self).get_context_data(**kwargs)
        year = self.request.GET.get('year', '')
        context['year'] = year
        books = models.Book.objects.filter(user=self.request.user)
        books = books.filter(year=year)
        context['object_list'] = books

        return context


class GenreListView(
    generic.TemplateView
):
    template_name = 'books/genre_list.html'

    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        books = models.Book.objects.filter(user=self.request.user)
        genres = list(set(book.genre for book in books))
        genres.sort()

        genres_counts = []
        for genre in genres:
            count = len(list(books.filter(genre=genre)))
            genres_counts.append(count)
        context['genres'] = zip(genres, genres_counts)
        return context


class GenreDetailView(
    generic.TemplateView
):
    template_name = 'books/genre_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        genre = self.request.GET.get('genre', '')
        context['genre'] = genre
        books = models.Book.objects.filter(user=self.request.user)
        books = books.filter(genre=genre)
        context['object_list'] = books

        return context


class CollView(
    RestrictToUserMixin,
    generic.TemplateView
):
    template_name = 'books/coll.html'

    def get_context_data(self, **kwargs):
        context = super(CollView, self).get_context_data(**kwargs)
        # try this approach in Year and Genre:
        current_year = self.kwargs['year']
        context['year'] = current_year

        months = range(1, 13)
        months_items = {month: [] for month in months}

        books = models.Book.objects.filter(user=self.request.user)
        for book in books:
            for date in book.dates.split(', '):
                year, month, day = [int(n) for n in date.split('-')]
                if year == int(current_year):
                    months_items[month].append((day, book))

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
