from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces import views

from . import forms


class HomePageView(
    generic.TemplateView
):
    template_name = 'home.html'


class SignUpView(
    views.AnonymousRequiredMixin,
    generic.CreateView
):
    form_class = forms.RegistrationForm
    model = User
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')


class LogInView(
    views.AnonymousRequiredMixin,
    generic.FormView
):
    form_class = forms.LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(LogInView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(
    views.LoginRequiredMixin,
    generic.RedirectView
):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)
