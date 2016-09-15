import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models


class Author(models.Model):
    user = models.ForeignKey(User, related_name='authors')
    name = models.CharField(max_length=255)
    first_letter = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        self.set_first_letter()
        super(Author, self).save(*args, **kwargs)

    def set_first_letter(self):
        if ' ' in self.name:
            self.first_letter = self.name.split()[1][0]
        else:
            self.first_letter = self.name[0]


class Book(models.Model):
    user = models.ForeignKey(User, related_name='books')
    name = models.CharField(max_length=255)
    first_letter = models.CharField(max_length=1, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=100, blank=True)
    authors_list = models.CharField(max_length=3000, blank=True)
    authors = models.ManyToManyField(
        Author, related_name='written', blank=True)
    dates = models.TextField(blank=True)
    first_date = models.DateField()
    review = models.TextField(blank=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.set_first_letter()
        self.set_first_date()

        super(Book, self).save(*args, **kwargs)

        if self.authors:
            for author in self.authors.all():
                author.written.remove(self)

        if self.authors_list:
            for author_name in self.authors_list.split(', '):
                try:
                    author = Author.objects.get(
                        name=author_name, user=self.user)
                except ObjectDoesNotExist:
                    author = Author(name=author_name, user=self.user)
                    author.save()
                author.written.add(self)

    def set_first_letter(self):
        if self.name[:3] == 'The':
            self.first_letter = self.name[4]
        else:
            self.first_letter = self.name[0]

    def set_first_date(self):
        date = self.dates.split(', ')[0]
        year, month, day = [int(elem) for elem in date.split('-')]
        self.first_date = datetime.date(year, month, day)
