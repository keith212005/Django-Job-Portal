import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from gtts import gTTS
from playsound import playsound
import playsound

from students.models import StudentInfo
from .forms import LoginForm, SignUpForm
from companies.models import CompanyInfo, JobPosting
from django.conf import settings


def login_view(request):
  form = LoginForm(request.POST or None)
  msg = None
  if request.method == "POST":
    if form.is_valid():
      email = form.cleaned_data.get("email")
      password = form.cleaned_data.get("password")
      user = authenticate(email=email, password=password)
      if user is not None:
        login(request, user)
        if user.user_type == 1:
          # redirect to administration dashboard
          return redirect('adminDashboard')
        elif user.user_type == 2:
          # redirect to student dashboard
          return redirect('studentDashboard')
        elif user.user_type == 3:
          # redirect to company dashboard
          return redirect('companyDashboard')
      else:
        msg = 'Invalid credentials'
    else:
      msg = 'Error validating the form'
  else:
    form = LoginForm()
  return render(request, "accounts/login.html", {"form": form, "msg": msg})


def createVoiceFile(request):
  tts = gTTS(text=" Welcome  " + request.user.username, lang="en")
  tts.save("%s-voice.mp3" % os.path.join("media/voice", (str(request.user.id))))
  return None


def register_user(request):
  msg = None
  success = False

  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      email = form.cleaned_data.get("email")
      raw_password = form.cleaned_data.get("password1")
      user = authenticate(username=email, password=raw_password)
      login(request, user)
      msg = 'User created'
      createVoiceFile(request)

      if user.user_type == 1:
        # redirect to administration dashboard
        return redirect('adminDashboard')
      elif user.user_type == 2:
        # redirect to student dashboard
        return redirect('studentDashboard')
      elif user.user_type == 3:
        # redirect to company dashboard
        return redirect('companyDashboard')
      # success = True
      # context = {'msg': msg, 'success': success}
      # return redirect("/login/", context)
    else:
      msg = 'Form is not valid'
  else:
    form = SignUpForm()

  return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def studentDashboard(request):
  x = settings.VOICE_URL + str(request.user.id) + "-voice.mp3"
  context = {'audio_url': x}
  return render(request, "students/dashboard.html",context)


@login_required(login_url="/login/")
def companyDashboard(request):
  x = settings.VOICE_URL + str(request.user.id) + "-voice.mp3"
  job_info = JobPosting.objects.all()
  total_jobs = len(job_info)
  context = {'job_info': job_info, 'total_jobs': total_jobs, 'audio_url': x}
  return render(request, "companies/dashboard.html", context)


@login_required(login_url="/login/")
def adminDashboard(request):
  # Getting all companies data
  x = settings.VOICE_URL + str(request.user.id) + "-voice.mp3"
  company_info = CompanyInfo.objects.all()
  total_companies = len(company_info)

  # Getting all students data
  student_info = StudentInfo.objects.all()
  total_students = len(student_info)

  job_info = JobPosting.objects.all()
  total_jobs = len(job_info)

  context = {
    'company': company_info,
    'total_companies': total_companies,
    'total_students': total_students,
    'total_jobs': total_jobs,
    'audio_url': x
  }
  return render(request, "administration/dashboard.html", context)
