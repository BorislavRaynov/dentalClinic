from django.shortcuts import render, redirect
from django.views import generic as views
from .models import Invoice
from .forms import GenerateInvoiceForm
from dental_clinic.patient.models import Patient
from dental_clinic.appointment.models import Appointment


def get_invoice_number():
    try:
        invoice = Invoice.objects.last()
        return int(invoice.invoice_number) + 1
    except AttributeError:
        return 1

def generate_invoice(request,appointment_pk, patient_pk):
    patient = Patient.objects.filter(pk=patient_pk).get()
    appointment = Appointment.objects.filter(pk=appointment_pk).get()
    treatments = patient.treatment.all()
    amount = sum([treatment.cost for treatment in treatments])
    invoice_number = get_invoice_number()

    initial_data = {
        'patient': patient,
        'amount': f"{amount:.2f}",
        'invoice_number': invoice_number
    }

    form = GenerateInvoiceForm(initial=initial_data)

    if request.method == 'POST':
        form = GenerateInvoiceForm(request.POST, initial=initial_data)
        if form.is_valid():
            form.save()
            for treatment in treatments:
                patient.treatment.remove(treatment)
            appointment.delete()
            return redirect('appointments-catalogue')

    context = {
        'form': form,
        'patient_pk': patient_pk,
        'appointment_pk': appointment_pk,
        'invoice_number': invoice_number
    }

    return render(request, template_name='dental_clinic/invoice/generate-invoice.html', context=context)
