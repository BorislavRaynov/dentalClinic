from django.urls import path
from .views import home_page, about_page, contacts_page

urlpatterns = [
    path('', home_page, name='home-page'),
    path('about/', about_page, name='about'),
    path('contacts/', contacts_page, name='contacts-page')
]