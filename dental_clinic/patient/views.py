from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from dental_clinic.treatment.models import Treatment
from .models import Patient
from .forms import AddTreatmentForm


class PatientListView(LoginRequiredMixin, views.ListView):
    template_name = 'dental_clinic/patient/patients-catalogue.html'
    model = Patient
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', '')
        queryset = queryset.filter(last_name__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class PatientCreateView(LoginRequiredMixin, views.CreateView):
    template_name = 'dental_clinic/patient/create-patient.html'
    model = Patient
    fields = ('email', 'first_name', 'last_name', 'phone_number')
    success_url = reverse_lazy('appointment-create')


class PatientEditView(LoginRequiredMixin, views.UpdateView):
    template_name = 'dental_clinic/patient/edit-patient.html'
    model = Patient
    fields = ['email', 'first_name', 'last_name', 'phone_number']
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
