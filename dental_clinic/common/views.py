from django.shortcuts import render
# from django.views import generic as views


def home_page(request):
    return render(request, 'dental_clinic/common/home-page.html')


def about_page(request):
    return render(request, 'dental_clinic/common/about.html')


def contact_page(request):
    return render(request, 'dental_clinic/common/contacts.html')
