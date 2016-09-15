import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models


class Person(models.Model):
    user = models.ForeignKey(User, related_name='persons')
    name = models.CharField(max_length=255)
    first_letter = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        self.set_first_letter()
        super(Person, self).save(*args, **kwargs)

    def set_first_letter(self):
        if ' ' in self.name:
            self.first_letter = self.name.split()[1][0]
        else:
            self.first_letter = self.name[0]


class Movie(models.Model):
    user = models.ForeignKey(User, related_name='movies')
    name = models.CharField(max_length=255)
    first_letter = models.CharField(max_length=1, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=100, blank=True)
    directors_list = models.CharField(max_length=3000, blank=True)
    actors_list = models.TextField(blank=True)
    directors = models.ManyToManyField(
        Person, related_name='directed', blank=True)
    actors = models.ManyToManyField(
        Person, related_name='starred_in', blank=True)
    dates = models.TextField(blank=True)
    first_date = models.DateField()
    review = models.TextField(blank=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:movie_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.set_first_letter()
        self.set_first_date()

        super(Movie, self).save(*args, **kwargs)

        if self.directors:
            for director in self.directors.all():
                director.directed.remove(self)

        if self.actors:
            for actor in self.actors.all():
                actor.starred_in.remove(self)

        if self.directors_list:
            for director_name in self.directors_list.split(', '):
                try:
                    director = Person.objects.get(
                        name=director_name, user=self.user)
                except ObjectDoesNotExist:
                    director = Person(name=director_name, user=self.user)
                    director.save()
                director.directed.add(self)

        if self.actors_list:
            for actor_name in self.actors_list.split(', '):
                try:
                    actor = Person.objects.get(
                        name=actor_name, user=self.user)
                except ObjectDoesNotExist:
                    actor = Person(name=actor_name, user=self.user)
                    actor.save()
                actor.starred_in.add(self)

    def set_first_letter(self):
        if self.name[:3] == 'The':
            self.first_letter = self.name[4]
        else:
            self.first_letter = self.name[0]

    def set_first_date(self):
        date = self.dates.split(', ')[0]
        year, month, day = [int(elem) for elem in date.split('-')]
        self.first_date = datetime.date(year, month, day)


class TVShow(models.Model):
    GENRE_CHOICES = (
        ('drama', 'драма'),
        ('comedy', 'комедия'),
        ('animated', 'анимационный'),
        ('fantastic', 'фантастический'),
        ('doc', 'документальный'),
        ('other', 'другое'),
    )
    user = models.ForeignKey(User, related_name='tvshows')
    name = models.CharField(max_length=255)
    # first_letter = models.CharField(max_length=1, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    # year = models.CharField(max_length=4)
    genre = models.CharField(max_length=100, blank=True)
    # add "Other" field in the genres list in TVShowListView for those with
    # blank genre_family
    genre_family = models.CharField(max_length=100, choices=GENRE_CHOICES)
    creators_list = models.CharField(max_length=3000, blank=True)
    creators = models.ManyToManyField(
        Person, related_name='created', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:tvshow_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(TVShow, self).save(*args, **kwargs)

        if self.creators:
            for creator in self.creators.all():
                creator.created.remove(self)

        if self.creators_list:
            for creator_name in self.creators_list.split(', '):
                try:
                    creator = Person.objects.get(
                        name=creator_name, user=self.user)
                except ObjectDoesNotExist:
                    creator = Person(name=creator_name, user=self.user)
                    creator.save()
                creator.created.add(self)


class TVShowSeason(models.Model):
    user = models.ForeignKey(User, related_name='tvshowseasons')
    tvshow = models.ForeignKey(TVShow, related_name='seasons')
    number = models.IntegerField()
    url_number = models.CharField(max_length=3)
    name = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    year = models.CharField(max_length=10)
    actors_list = models.TextField(blank=True)
    actors = models.ManyToManyField(
        Person, related_name='tvshowseason_starred_in', blank=True)
    dates = models.TextField(blank=True)
    first_date = models.DateField()
    review = models.TextField(blank=True)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return "{} — Сезон {}".format(self.tvshow.name, self.number)

    def get_absolute_url(self):
        return reverse('movies:tvshowseason_detail',
                       kwargs={'pk': self.tvshow.pk,
                               'url_number': self.url_number})

    def save(self, *args, **kwargs):
        self.set_first_date()
        self.set_url_number()

        super(TVShowSeason, self).save(*args, **kwargs)

        if self.actors:
            for actor in self.actors.all():
                actor.tvshowseason_starred_in.remove(self)

        if self.actors_list:
            for actor_name in self.actors_list.split(', '):
                try:
                    actor = Person.objects.get(
                        name=actor_name, user=self.user)
                except ObjectDoesNotExist:
                    actor = Person(name=actor_name, user=self.user)
                    actor.save()
                actor.tvshowseason_starred_in.add(self)

    def set_first_date(self):
        date = self.dates.split(', ')[0]
        year, month, day = [int(elem) for elem in date.split('-')]
        self.first_date = datetime.date(year, month, day)

    def set_url_number(self):
        if len(str(self.number)) == 1:
            self.url_number = '0' + str(self.number)
        else:
            self.url_number = str(self.number)
