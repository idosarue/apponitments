from django.db import models
from django.http import request
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from patient.models import Appointment, AppointmentResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from patient.forms import  AppointmentResponseForm, AppointmentForm
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from datetime import datetime
from django.contrib.auth.models import User
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from .forms import CalendarForm
from send_emails import send_response_email_to_user, send_success_message_email_to_user, send_success_message_email_to_therapist

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_superuser 

class AllUsersList(SuperUserRequiredMixin, ListView):
    model = Profile
    template_name = 'therapist/all_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(is_superuser = True)
        context['user_list'] = Profile.objects.exclude(user= user)
        return context

class AppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/apt_requests.html'
    context_object_name = 'appointments'
    ordering = 'timestamp'

class AcceptedAppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/accepted_apt.html'
    ordering = 'timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(is_approved=True)
        context['appointments_response'] = AppointmentResponse.objects.filter(is_approved=True)
        return context

class PendingAppointmentListView(SuperUserRequiredMixin, ListView):
    model = AppointmentResponse
    template_name = 'therapist/pending_apts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = AppointmentResponse.objects.exclude(is_approved=True)
        return context

class AppointmentResponseView(SuperUserRequiredMixin, CreateView):
    form_class = AppointmentResponseForm
    template_name = 'patient/appointment_response.html'
    success_url = reverse_lazy('home')
    
    def get_appointment(self):
        appoint_id = self.kwargs['pk']
        return get_object_or_404(Appointment, id=appoint_id)

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.original_request = self.get_appointment()
        appoint.user = appoint.original_request.user
        appoint.choice = 'P'
        appoint.save()
        therapist_email = self.request.user.email
        send_response_email_to_user(appoint.original_request.user.user, appoint ,therapist_email)
        return super().form_valid(form)


@user_passes_test(lambda u: u.is_superuser)
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment_date = appointment.appointment_date
    start_time = appointment.start_time
    therapist_email = 'testdjangosaru@gmail.com'
    if status == 'accept':
        if not Appointment.objects.filter(start_time=start_time,appointment_date=appointment_date, is_approved=True).exists():
            appointment.choice = 'A'
            appointment.is_approved = True
            appointment.save()
            send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date, therapist_email)
            send_success_message_email_to_therapist(appointment.user.user, appointment.start_time, appointment.appointment_date, therapist_email)
        else:
            messages.error(request, 'you cannot have meetings on the same time, send the user an update request')
            return redirect('appointment_response', pk)
    else:
        appointment.choice = 'P'
        appointment.save()
        return redirect('appointment_response', pk)
    return redirect('home')

@login_required
def update_appointment_response_status(request, pk, status):
    appointment = get_object_or_404(AppointmentResponse, id=pk)
    therapist_email = 'testdjangosaru@gmail.com'
    if request.user.profile == appointment.original_request.user:
        if status == 'accept':
            print(request.user.profile)
            print(appointment.id)
            appointment.is_approved = True
            appointment.save()
            send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date, therapist_email)
            send_success_message_email_to_therapist(appointment.user.user, appointment.start_time, appointment.appointment_date, therapist_email)
        else:
            return redirect('query_appointment')
    return redirect('home')



class UserAppointments(SuperUserRequiredMixin, ListView):
    model = Profile
    template_name = 'therapist/user_appointments.html'

    def get_profile(self):
        profile_id = self.kwargs['pk']
        return get_object_or_404(Profile, id=profile_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['past_appointments'] = self.get_profile().appointment_set.filter(appointment_date__lt=datetime.today(), is_approved=True)
        context['future_appointments'] = self.get_profile().appointment_set.filter(appointment_date__gte=datetime.today(),is_approved=True)
        context['future_appointments_response'] = self.get_profile().appointmentresponse_set.filter(appointment_date__gte=datetime.today(),is_approved=True)
        context['past_appointments_response'] = self.get_profile().appointmentresponse_set.filter(appointment_date__lt=datetime.today(), is_approved=True)
        return context

class CalendarView(SuperUserRequiredMixin,ListView):
    model = Appointment
    template_name = 'therapist/calendar.html'

    def get_date(self):
        form = CalendarForm(self.request.GET)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            print(year)
            return {'year' : year, 'month' : month}
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.get_date():
            cal = Calendar(year=datetime.now().year, month=datetime.now().month)
        else:
            year = self.get_date()['year']
            month = self.get_date()['month']
            cal = Calendar(year=int(year), month=int(month))
        html_cal = cal.formatmonth(withyear=True)
        context['form'] = CalendarForm
        context['calendar'] = mark_safe(html_cal)
        return context

class AppointmentUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Appointment
    fields = ['start_time', 'appointment_date']
    success_url = reverse_lazy('calendar')
    template_name = 'therapist/edit_appoint'

    def get_appoint(self):
        appoint = self.kwargs['pk']
        return appoint

class AppointmentUpdateView(SuperUserRequiredMixin, UpdateView):
    success_url = reverse_lazy('calendar')
    form_class = AppointmentForm
    template_name = 'therapist/edit_appoint.html'

    def get_appoint(self):
        appoint_id = self.kwargs['pk']
        appoint = Appointment.objects.filter(id=appoint_id, is_approved=True).first()
        return appoint

    def get_object(self, queryset=None):
        return self.get_appoint()

class AppointmentResponseUpdateView(SuperUserRequiredMixin, UpdateView):
    success_url = reverse_lazy('calendar')
    template_name = 'therapist/edit_appoint.html'
    form_class = AppointmentResponseForm

    def get_appoint(self):
        appoint_id = self.kwargs['pk']
        appoint = AppointmentResponse.objects.filter(id=appoint_id, is_approved=True).first()
        return appoint

    def get_object(self, queryset=None):
        return self.get_appoint()


