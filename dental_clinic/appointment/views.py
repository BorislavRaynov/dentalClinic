from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from dental_clinic.appointment.forms import AppointmentCreateForm, AppointmentEditForm
from dental_clinic.appointment.models import Appointment
from dental_clinic.patient.models import Patient


class AppointmentCreateView(views.CreateView):
    model = Appointment
    template_name = 'dental_clinic/appointment/create-appointment.html'
    form_class = AppointmentCreateForm
    success_url = reverse_lazy('appointments-catalogue')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered_patients'] = Patient.objects.all()
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['patient'].queryset = Patient.objects.all()
        form.initial['dentist'] = self.request.user
        return form


class AppointmentDetailsView(views.DetailView):
    template_name = 'dental_clinic/appointment/details-appointments.html'
    model = Appointment


class AppointmentUpdateView(views.UpdateView):
    template_name = 'dental_clinic/appointment/edit-appointment.html'
    model = Appointment
    form_class = AppointmentEditForm
    success_url = reverse_lazy('appointments-catalogue')


class AppointmentDeleteView(views.DeleteView):
    model = Appointment
    template_name = 'dental_clinic/appointment/delete-appointment.html'
    success_url = reverse_lazy('appointments-catalogue')


class AppointmentListView(LoginRequiredMixin, views.ListView):
    model = Appointment
    template_name = 'dental_clinic/appointment/appointments-catalogue.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(dentist=user)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['treatments'] =