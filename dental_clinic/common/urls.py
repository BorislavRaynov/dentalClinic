from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactPageView.as_view(), name='contact-page')
]
