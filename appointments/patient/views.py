from accounts.models import Profile
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import AppointmentForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')


class CreateBookingView(CreateView):
    form_class = AppointmentForm
    template_name = 'patient/query_appointment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.user = self.request.user.profile
        appoint.save()
        email_message_user = f'''
        Hello {self.request.user.username}, your request for an appointment at: {form.cleaned_data['start_time']} , {form.cleaned_data['appointment_date']}
        is being reviewed, we will get back to you soon.
        '''
        email_message_therapist = f'''
        {self.request.user.first_name} {self.request.user.last_name}, requested an appointment at: {form.cleaned_data['start_time']} , {form.cleaned_data['appointment_date']}
        '''
        send_mail(
            'Appointment Request',
            email_message_user,
            'testdjangosar@gmail.com',
            ['djangoreciever@gmail.com'],
            fail_silently=False,
        )

        send_mail(
            'Your appointment',
            email_message_therapist,
            'testdjangosar@gmail.com',
            ['testdjangosar@gmail.com'],
            fail_silently=False,
        )
        return super().form_valid(form)
