from django.shortcuts import render
from django.views import generic as views
from dental_clinic.dentist_profile.models import DentistUserProfile

# class HomePage(views.TemplateView):
#     template_name = 'home-page'

def home_page(request):
    return render(request, 'dental_clinic/common/home-page.html')


def about_page(request):
    return render(request, 'dental_clinic/common/about.html')
