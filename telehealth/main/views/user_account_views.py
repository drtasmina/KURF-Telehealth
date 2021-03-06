"""Account related views."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import render, redirect, reverse
from .mixins import LoginProhibitedMixin
from ..forms import *


class ChangePasswordView(LoginRequiredMixin, FormView):
    """View that handles password change requests."""

    template_name = 'password.html'
    form_class = ChangePasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""
        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""
        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Your sign up is successfully!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class PatientSignUpView(SignUpView):
    """View that signs up patient."""
    form_class = PatientSignUpForm
    template_name = "patient_sign_up.html"
    redirect_url = 'home'

    def get(self, request, *args, **kwargs):
        if Patient.objects.count():
            return redirect(self.redirect_url)
        else:
            return super().get(request, *args, **kwargs)


class DoctorSignUpView(SignUpView):
    """View that signs up patient."""
    form_class = DoctorSignUpForm
    template_name = "doctor_sign_up.html"
