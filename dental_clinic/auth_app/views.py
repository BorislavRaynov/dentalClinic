from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login
from django.views import generic as views
from .forms import RegisterUserForm


class RegisterUserView(views.CreateView):
    template_name = 'dental_clinic/auth_app/register-user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'dental_clinic/auth_app/login-user.html'


class LogoutUserView(auth_views.LogoutView):
    pass
