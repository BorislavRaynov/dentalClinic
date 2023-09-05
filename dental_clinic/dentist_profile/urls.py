from django.urls import path
from .views import ProfileDeleteView, ProfileDetailsView, ProfileEditView


urlpatterns = [
    path('details/<int:pk>', ProfileDetailsView.as_view(), name='profile-details'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name='profile-edit'),
    path('delete/<int:pk>', ProfileDeleteView.as_view(), name='profile-delete')
]
