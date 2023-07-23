from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic as views
from .models import DentistUserProfile


class ProfileDetailsView(views.DetailView):
    template_name = 'dental_clinic/dentist_profile/dentist-details.html'
    model = DentistUserProfile


class ProfileEditView(views.UpdateView):
    template_name = 'dental_clinic/dentist_profile/dentist-edit.html'
    model = DentistUserProfile
    fields = ['email', 'first_name', 'last_name', 'profile_picture']

    def get_success_url(self):
        profile_details_url = reverse_lazy('profile-details', args=[self.object.pk])
        return profile_details_url


class ProfileDeleteView(views.DeleteView):
    model = DentistUserProfile
    template_name = 'dental_clinic/dentist_profile/dentist-delete.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        self.request.user.delete()
        return HttpResponseRedirect(success_url)
