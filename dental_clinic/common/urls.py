from django.urls import path
from .views import home_page, about_page, contact_page

urlpatterns = [
    path('', home_page, name='home-page'),
    path('about/', about_page, name='about'),
    path('contacts/', contact_page, name='contact-page')
]
