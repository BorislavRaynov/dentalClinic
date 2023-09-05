from django.views import generic as views


class HomePageView(views.TemplateView):
    template_name = "dental_clinic/common/home-page.html"


class AboutPageView(views.TemplateView):
    template_name = "dental_clinic/common/about.html"


class ContactPageView(views.TemplateView):
    template_name = "dental_clinic/common/contacts.html"
