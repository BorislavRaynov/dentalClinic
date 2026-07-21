from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from dental_clinic.treatment.models import Treatment
from .models import Patient, MedicalCondition, Allergy, MedicalHistoryEntry
from .forms import AddTreatmentForm, PatientForm, MedicalConditionForm, AllergyForm, MedicalHistoryEntryForm


class PatientListView(LoginRequiredMixin, views.ListView):
    template_name = 'dental_clinic/patient/patients-catalogue.html'
    model = Patient
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')

        search = self.request.GET.get('search', '')
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(patient_id__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class PatientCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'dental_clinic/patient/create-patient.html'
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('appointment-create')


class PatientEditView(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/patient/edit-patient.html'
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('patients-catalogue')


class PatientAddTreatment(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/patient/patient-add-treatment.html'
    model = Patient
    form_class = AddTreatmentForm
    success_url = reverse_lazy('appointments-catalogue')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered_treatments'] = Treatment.objects.all()
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['treatment'].queryset = Treatment.objects.all()
        return form


class PatientMedicalRecordView(LoginRequiredMixin, views.DetailView):
    template_name = 'dental_clinic/patient/patient-medical-record.html'
    model = Patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_conditions'] = self.object.medical_conditions.all()
        context['allergies'] = self.object.allergies.all()
        context['medical_history_entries'] = self.object.medical_history_entries.all()
        return context


class MedicalConditionCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'dental_clinic/patient/add-condition.html'
    model = MedicalCondition
    form_class = MedicalConditionForm

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.kwargs['patient_pk']})


class MedicalConditionUpdateView(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/patient/edit-condition.html'
    model = MedicalCondition
    form_class = MedicalConditionForm

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.object.patient_id})


class MedicalConditionDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = 'dental_clinic/patient/delete-condition.html'
    model = MedicalCondition

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.object.patient_id})


class AllergyCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'dental_clinic/patient/add-allergy.html'
    model = Allergy
    form_class = AllergyForm

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.kwargs['patient_pk']})


class AllergyUpdateView(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/patient/edit-allergy.html'
    model = Allergy
    form_class = AllergyForm

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.object.patient_id})


class AllergyDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = 'dental_clinic/patient/delete-allergy.html'
    model = Allergy

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.object.patient_id})


class MedicalHistoryEntryCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'dental_clinic/patient/add-history-entry.html'
    model = MedicalHistoryEntry
    form_class = MedicalHistoryEntryForm

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.kwargs['patient_pk']})


class MedicalHistoryEntryUpdateView(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/patient/edit-history-entry.html'
    model = MedicalHistoryEntry
    form_class = MedicalHistoryEntryForm

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.object.patient_id})


class MedicalHistoryEntryDeleteView(LoginRequiredMixin, views.DeleteView):
    template_name = 'dental_clinic/patient/delete-history-entry.html'
    model = MedicalHistoryEntry

    def get_success_url(self):
        return reverse_lazy('patient-medical-record', kwargs={'pk': self.object.patient_id})
