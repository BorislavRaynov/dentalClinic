from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Treatment


class TreatmentCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'dental_clinic/treatment/create-treatment.html'
    model = Treatment
    fields = ('clinical_code', 'name', 'cost', 'description', 'notes')
    success_url = reverse_lazy('appointments-catalogue')


class TreatmentEditView(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/treatment/edit-treatment.html'
    model = Treatment
    fields = ('clinical_code', 'name', 'cost', 'description', 'notes')
    success_url = reverse_lazy('appointments-catalogue')
