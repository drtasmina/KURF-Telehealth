"""Static views of the app."""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from .mixins import LoginProhibitedMixin
from django.shortcuts import redirect
from django.urls import reverse
from ..models import *


class Home(LoginProhibitedMixin, TemplateView): # THE ORDER OF THESE SUPERCLASSES MATTERS
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        kwargs['patient_count'] = Patient.objects.count()
        return kwargs


class DashboardView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        kwargs['current_user'] = request.user
        if request.user.is_patient():
            return render(request, 'patient_dashboard.html', context=kwargs)
        elif request.user.is_doctor():
            return render(request, 'doctor_dashboard.html', context=kwargs)
        else:
            return render(request, 'dashboard.html', context=kwargs)
